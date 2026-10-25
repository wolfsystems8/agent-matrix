"""Objetivo de demostración DELIBERADAMENTE VULNERABLE.

Solo debe ejecutarse dentro de la red interna del sandbox de sec-agent-matrix
(core/sandbox/docker-compose.sandbox.yml). No usar como base de nada real.

Vulnerabilidades sembradas a propósito para que los agentes de Fase 2 tengan
material verificable:
  - SQLi en POST /login (concatenación de la consulta)
  - XSS reflejado en GET /search?q=
  - IDOR en GET /orders/<id> (sin comprobar propiedad)
  - Fuga de configuración en GET /debug/config
  - Errores verbosos (traceback al cliente)
  - Ausencia de cabeceras de seguridad y cabecera Server de Werkzeug
"""

import os
import sys
import time
import traceback

import psycopg2
from flask import Flask, Response, jsonify, request

if os.environ.get("DEMO_TARGET_ACK") != "1":
    sys.exit(
        "demo-target: abortado. Es una aplicación DELIBERADAMENTE VULNERABLE; "
        "arráncala solo mediante core/sandbox/docker-compose.sandbox.yml."
    )

DSN = os.environ.get(
    "DATABASE_URL", "postgres://test_user:test_pass@target-db:5432/test_db"
)

app = Flask(__name__)


def connect():
    last = None
    for _ in range(30):
        try:
            return psycopg2.connect(DSN)
        except psycopg2.OperationalError as exc:  # postgres aún arrancando
            last = exc
            time.sleep(2)
    raise SystemExit("demo-target: no se pudo conectar a la base: %s" % last)


def seed():
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY,
                username text UNIQUE NOT NULL,
                password text NOT NULL,
                role text NOT NULL,
                email text NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id serial PRIMARY KEY,
                user_id integer NOT NULL,
                item text NOT NULL,
                total numeric(10, 2) NOT NULL,
                notes text
            )
            """
        )
        cur.execute("SELECT count(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO users (username, password, role, email) "
                "VALUES (%s, %s, %s, %s)",
                [
                    ("alice", "secret123", "user", "alice@example.test"),
                    ("bob", "hunter2", "user", "bob@example.test"),
                    ("admin", "admin123", "admin", "admin@example.test"),
                ],
            )
            cur.executemany(
                "INSERT INTO orders (user_id, item, total, notes) "
                "VALUES (%s, %s, %s, %s)",
                [
                    (1, "Teclado", 49.90, "Enviar a casa"),
                    (1, "Monitor", 199.00, "Sin notas"),
                    (2, "Raton", 19.50, "tarjeta 4111-1111-1111-1111"),
                    (3, "Servidor", 1499.00, "pedido interno"),
                ],
            )


@app.get("/")
def index():
    return Response(
        """<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Demo Shop</title></head><body>
<h1>Demo Shop</h1>
<p>Aplicación de demostración para el sandbox de sec-agent-matrix.</p>
<ul>
  <li><a href="/search?q=teclado">Buscar</a></li>
  <li><a href="/orders/1">Pedido 1</a></li>
  <li><a href="/debug/config">Config</a></li>
</ul>
<form method="post" action="/login">
  <input name="username" placeholder="usuario">
  <input name="password" type="password" placeholder="contraseña">
  <button>Entrar</button>
</form>
</body></html>""",
        mimetype="text/html",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return Response(
            '<form method="post"><input name="username">'
            '<input name="password"><button>Entrar</button></form>',
            mimetype="text/html",
        )

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = connect()
    with conn, conn.cursor() as cur:
        # VULNERABLE A PROPÓSITO: concatenación directa (SQLi).
        query = (
            "SELECT id, username, role FROM users "
            "WHERE username = '%s' AND password = '%s'" % (username, password)
        )
        cur.execute(query)
        row = cur.fetchone()

    if not row:
        return Response("Credenciales inválidas", status=401, mimetype="text/plain")

    return jsonify({"id": row[0], "username": row[1], "role": row[2]})


@app.get("/search")
def search():
    q = request.args.get("q", "")
    # VULNERABLE A PROPÓSITO: q se refleja sin escapar (XSS reflejado).
    return Response(
        "<!doctype html><html><body><h1>Resultados para %s</h1>"
        "<p>Sin coincidencias.</p></body></html>" % q,
        mimetype="text/html",
    )


@app.get("/orders/<int:order_id>")
def order(order_id):
    conn = connect()
    with conn, conn.cursor() as cur:
        # VULNERABLE A PROPÓSITO: no se comprueba el propietario (IDOR).
        cur.execute(
            "SELECT id, user_id, item, total, notes FROM orders WHERE id = %s",
            (order_id,),
        )
        row = cur.fetchone()

    if not row:
        return jsonify({"error": "not found"}), 404

    return jsonify(
        {"id": row[0], "user_id": row[1], "item": row[2], "total": str(row[3]), "notes": row[4]}
    )


@app.get("/debug/config")
def debug_config():
    # VULNERABLE A PROPÓSITO: expone variables de entorno.
    return jsonify({k: v for k, v in sorted(os.environ.items())})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(Exception)
def verbose_error(exc):
    # VULNERABLE A PROPÓSITO: devuelve el traceback completo al cliente.
    return Response(
        "<pre>%s</pre>" % traceback.format_exc(), status=500, mimetype="text/html"
    )


if __name__ == "__main__":
    seed()
    app.run(host="0.0.0.0", port=8080, threaded=True)
