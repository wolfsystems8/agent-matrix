"""Tests del toolchain y de la integridad de los adaptadores."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import tomllib
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("secmatrix", ROOT / "tools" / "secmatrix.py")
secmatrix = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = secmatrix
SPEC.loader.exec_module(secmatrix)


class TestCore(unittest.TestCase):
    def test_agents_load(self) -> None:
        agents = secmatrix.load_agents()
        self.assertEqual(len(agents), 9)
        self.assertEqual(len({a.id for a in agents}), 9)
        phases = {a.phase for a in agents}
        self.assertEqual(phases, {1, 2, 3})
        expected = {
            "threat-modeler",
            "sast-auditor",
            "triage-master",
            "sandbox-manager",
            "network-auditor",
            "web-dast-tester",
            "exploit-tester",
            "secfix-patcher",
            "regression-qa",
        }
        self.assertEqual({a.id for a in agents}, expected)

    def test_agent_authority_matches_tools(self) -> None:
        for agent in secmatrix.load_agents():
            if agent.authority == "write":
                self.assertIn("edit", agent.tools, agent.id)
            else:
                self.assertNotIn("edit", agent.tools, agent.id)

    def test_read_only_agents_without_shell(self) -> None:
        # Excepción documentada: sast-auditor ejecuta scanners (semgrep/bandit).
        shell_agents = {
            a.id
            for a in secmatrix.load_agents()
            if a.authority == "read-only" and "shell" in a.tools
        }
        self.assertEqual(shell_agents, {"sast-auditor"})

    def test_skills_load(self) -> None:
        skills = secmatrix.load_skills()
        self.assertEqual(len(skills), 9)
        for skill in skills:
            self.assertEqual(skill.id, skill.name)
            self.assertTrue(skill.description)
            self.assertTrue(skill.body.strip())

    def test_commands_load(self) -> None:
        commands = secmatrix.load_commands()
        self.assertEqual({c.name for c in commands}, {"sec-audit", "sec-pentest", "sec-fix", "sec-pipeline"})

    def test_frontmatter_parser(self) -> None:
        meta, body = secmatrix.parse_frontmatter(
            '---\nid: demo\ntools: [read, write]\nphase: 1\n---\n\n# Body\n'
        )
        self.assertEqual(meta["id"], "demo")
        self.assertEqual(meta["tools"], ["read", "write"])
        self.assertEqual(meta["phase"], "1")
        self.assertEqual(body.strip(), "# Body")


class TestBuild(unittest.TestCase):
    def test_generated_files_in_sync(self) -> None:
        files = secmatrix.build_files("core", secmatrix.TOOLS)
        self.assertEqual(len(files), 85)
        for path, content in files.items():
            target = ROOT / path
            self.assertTrue(target.exists(), f"falta {path}")
            self.assertEqual(target.read_text(encoding="utf-8"), content, f"desincronizado {path}")

    def test_no_unresolved_tokens(self) -> None:
        for path, content in secmatrix.build_files("core", secmatrix.TOOLS).items():
            self.assertNotIn(secmatrix.CORE_TOKEN, content, path)

    def test_build_is_deterministic(self) -> None:
        first = secmatrix.build_files("core", secmatrix.TOOLS)
        second = secmatrix.build_files("core", secmatrix.TOOLS)
        self.assertEqual(first, second)

    def test_manifest_matches_disk(self) -> None:
        manifest = json.loads((ROOT / secmatrix.MANIFEST_NAME).read_text(encoding="utf-8"))
        for path, digest in manifest["files"].items():
            data = (ROOT / path).read_text(encoding="utf-8")
            self.assertEqual(secmatrix.sha256(data), digest, path)

    def test_codex_toml_is_valid(self) -> None:
        for path in (ROOT / ".codex" / "agents").glob("*.toml"):
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(data["name"], path)
            self.assertTrue(data["description"], path)
            self.assertTrue(data["developer_instructions"].strip(), path)

    def test_opencode_permissions(self) -> None:
        read_only = (ROOT / ".opencode/agents/threat-modeler.md").read_text(encoding="utf-8")
        sandbox = (ROOT / ".opencode/agents/network-auditor.md").read_text(encoding="utf-8")
        writer = (ROOT / ".opencode/agents/secfix-patcher.md").read_text(encoding="utf-8")
        self.assertIn("mode: subagent", read_only)
        self.assertIn("reports/**", read_only)
        # V-03: los agentes de solo lectura no tienen shell libre.
        self.assertIn('action: shell\n    resource: "*"\n    effect: deny', read_only)
        self.assertIn('resource: "git log *"', read_only)
        self.assertIn('action: shell\n    resource: "*"\n    effect: allow', sandbox)
        self.assertIn('action: edit\n    resource: "*"\n    effect: allow', writer)

    def test_validate_passes(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            code = secmatrix.cmd_validate(Namespace())
        self.assertEqual(code, 0)


class TestInstall(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="secmatrix-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_install_layout_and_idempotency(self) -> None:
        args = Namespace(
            target=str(self.tmp),
            tools="",
            force=False,
            dry_run=False,
            prune=False,
            no_rules=False,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_install(args), 0)

        self.assertTrue((self.tmp / ".sec-agent-matrix/core/ethics/ETHICAL_DIRECTIVE.md").exists())
        self.assertTrue((self.tmp / ".claude/agents/threat-modeler.md").exists())
        self.assertTrue((self.tmp / ".cursor/agents/threat-modeler.md").exists())
        self.assertTrue((self.tmp / ".codex/agents/threat-modeler.toml").exists())
        self.assertTrue((self.tmp / ".agents/skills/security-audit-pipeline/SKILL.md").exists())
        self.assertTrue((self.tmp / ".opencode/skills/security-audit-pipeline/SKILL.md").exists())
        self.assertTrue((self.tmp / ".opencode/commands/sec-audit.md").exists())
        self.assertTrue((self.tmp / "reports/README.md").exists())
        self.assertTrue((self.tmp / ".sec-agent-matrix/core/sandbox/.env").exists())
        env = (self.tmp / ".sec-agent-matrix/core/sandbox/.env").read_text(encoding="utf-8")
        # Sin Dockerfile en la raíz se conserva el objetivo de demo del sandbox.
        self.assertFalse(
            any(line.startswith("TARGET_CONTEXT=") for line in env.splitlines())
        )
        self.assertIn("REPORTS_DIR=../../../reports", env)
        self.assertTrue((self.tmp / "AGENTS.md").exists())
        self.assertTrue((self.tmp / "CLAUDE.md").exists())

        agent = (self.tmp / ".claude/agents/threat-modeler.md").read_text(encoding="utf-8")
        self.assertIn(".sec-agent-matrix/core/ethics/ETHICAL_DIRECTIVE.md", agent)
        self.assertNotIn(secmatrix.CORE_TOKEN, agent)

        agents_md = (self.tmp / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(agents_md.count("<!-- sec-agent-matrix:begin -->"), 1)

        before = (self.tmp / ".claude/agents/threat-modeler.md").read_text(encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_install(args), 0)
        after = (self.tmp / ".claude/agents/threat-modeler.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertEqual(
            (self.tmp / "AGENTS.md").read_text(encoding="utf-8").count("<!-- sec-agent-matrix:begin -->"),
            1,
        )

    def test_install_env_targets_project_root_when_dockerfile_exists(self) -> None:
        (self.tmp / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
        args = Namespace(
            target=str(self.tmp),
            tools="",
            force=False,
            dry_run=False,
            prune=False,
            no_rules=True,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_install(args), 0)

        env = (self.tmp / ".sec-agent-matrix/core/sandbox/.env").read_text(encoding="utf-8")
        lines = env.splitlines()
        self.assertIn("TARGET_CONTEXT=../../..", lines)
        self.assertIn("REPORTS_DIR=../../../reports", lines)

    def test_install_respects_conflicting_file(self) -> None:
        target_file = self.tmp / ".claude/agents/threat-modeler.md"
        target_file.parent.mkdir(parents=True)
        target_file.write_text("contenido propio del usuario\n", encoding="utf-8")

        args = Namespace(
            target=str(self.tmp),
            tools="claude",
            force=False,
            dry_run=False,
            prune=False,
            no_rules=True,
        )
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = secmatrix.cmd_install(args)
        self.assertEqual(code, 1)
        self.assertEqual(target_file.read_text(encoding="utf-8"), "contenido propio del usuario\n")

        args.force = True
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_install(args), 0)
        self.assertIn("threat-modeler", target_file.read_text(encoding="utf-8"))

    def test_dry_run_does_not_write(self) -> None:
        args = Namespace(
            target=str(self.tmp),
            tools="claude",
            force=False,
            dry_run=True,
            prune=False,
            no_rules=True,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_install(args), 0)
        self.assertFalse((self.tmp / ".claude").exists())

    def test_prune_ignores_manifest_paths_outside_project(self) -> None:
        out = self.tmp / "proj"
        out.mkdir()
        victim = self.tmp / "victima.txt"
        victim.write_text("importante\n", encoding="utf-8")
        (out / secmatrix.MANIFEST_NAME).write_text(
            json.dumps({"name": "x", "files": {"../victima.txt": "h"}}),
            encoding="utf-8",
        )
        with contextlib.redirect_stdout(io.StringIO()):
            secmatrix.write_files(out, {}, prune=True)
        self.assertTrue(victim.exists())


class TestClean(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="secmatrix-clean-"))
        self.original_root = secmatrix.ROOT
        secmatrix.ROOT = self.tmp
        (self.tmp / secmatrix.MANIFEST_NAME).write_text(
            json.dumps({"name": "x", "files": {".claude/agents/a.md": "h"}}),
            encoding="utf-8",
        )
        (self.tmp / ".claude/agents").mkdir(parents=True)
        (self.tmp / ".claude/agents/a.md").write_text("generado\n", encoding="utf-8")
        (self.tmp / ".claude/agents/mio.md").write_text("propio\n", encoding="utf-8")

    def tearDown(self) -> None:
        secmatrix.ROOT = self.original_root
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_clean_only_removes_manifest_files(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_clean(Namespace()), 0)
        self.assertFalse((self.tmp / ".claude/agents/a.md").exists())
        self.assertTrue((self.tmp / ".claude/agents/mio.md").exists())

    def test_clean_without_manifest_is_noop(self) -> None:
        (self.tmp / secmatrix.MANIFEST_NAME).unlink()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_clean(Namespace()), 0)
        self.assertTrue((self.tmp / ".claude/agents/a.md").exists())

    def test_clean_ignores_paths_outside_project(self) -> None:
        victim = self.tmp.parent / f"victima-clean-{self.tmp.name}.txt"
        victim.write_text("importante\n", encoding="utf-8")
        self.addCleanup(victim.unlink, missing_ok=True)
        manifest = json.loads((self.tmp / secmatrix.MANIFEST_NAME).read_text(encoding="utf-8"))
        manifest["files"]["../" + victim.name] = "h"
        (self.tmp / secmatrix.MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(secmatrix.cmd_clean(Namespace()), 0)
        self.assertTrue(victim.exists())


if __name__ == "__main__":
    unittest.main()
