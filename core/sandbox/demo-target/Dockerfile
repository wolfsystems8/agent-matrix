# Objetivo de demostración para el sandbox de la Fase 2.
# Contiene vulnerabilidades intencionadas: no reutilizar fuera del sandbox.
# Digest fijado (V-06): el tag `3.11-slim` puede moverse, el digest no.
FROM python:3.11-slim@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

RUN pip install --no-cache-dir \
      flask==3.1.3 \
      psycopg2-binary==2.9.9

# V-07: la aplicación no corre como root.
RUN groupadd --gid 10001 demo \
    && useradd --uid 10001 --gid 10001 --no-create-home \
       --shell /usr/sbin/nologin demo

COPY app.py /app/app.py

ENV HOME=/tmp

USER 10001:10001

EXPOSE 8080

CMD ["python", "/app/app.py"]
