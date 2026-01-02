import json
import os
import subprocess
import sys
from pathlib import Path


def _env_with_src_path() -> dict[str, str]:
    env = dict(os.environ)
    src_path = str(Path(__file__).resolve().parents[1] / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing else f"{src_path}{os.pathsep}{existing}"
    return env


def _assert_single_line(s: str) -> None:
    lines = [line for line in s.splitlines() if line != ""]
    assert len(lines) == 1


def test_validate_mode_reports_ok(tmp_path: Path) -> None:
    rows = [
        {
            "event_id": 1,
            "kind": "INTENT",
            "correlation_id": "c-1",
            "payload": {"authoritative_input": {"x": 1}, "boundary": {"boundary_version": 1, "boundary_config_hash": "sha256:" + "0" * 64}},
        },
        {
            "event_id": 2,
            "kind": "DECISION",
            "correlation_id": "c-1",
            "payload": {"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}},
        },
    ]
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=True) for r in rows) + "\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "ensdg.cli", "--mode", "validate", "--input", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env_with_src_path(),
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0


def test_validate_mode_errors_on_invariant(tmp_path: Path) -> None:
    rows = [
        {
            "event_id": 1,
            "kind": "EXECUTION",
            "correlation_id": "c-1",
            "payload": {"result": {"ok": True}},
        },
    ]
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=True) for r in rows) + "\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "ensdg.cli", "--mode", "validate", "--input", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env_with_src_path(),
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 4
    assert result.stdout == ""
    assert result.stderr.startswith("invariant error:")
    _assert_single_line(result.stderr)


def test_validate_mode_errors_on_replay(tmp_path: Path) -> None:
    rows = [
        {
            "event_id": 1,
            "kind": "INTENT",
            "correlation_id": "c-1",
            "payload": {
                "authoritative_input": {"x": 1},
                "boundary": {"boundary_version": 1, "boundary_config_hash": "sha256:" + "0" * 64},
            },
        },
        {
            "event_id": 2,
            "kind": "DECISION",
            "correlation_id": "c-1",
            "payload": {
                "decision": "ALLOW",
                "policy_version": True,
                "authoritative_digest": "sha256:" + "0" * 64,
                "rationale": {},
            },
        },
    ]
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=True) for r in rows) + "\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "ensdg.cli", "--mode", "validate", "--input", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env_with_src_path(),
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 4
    assert result.stdout == ""
    assert result.stderr.startswith("invariant error:")
    _assert_single_line(result.stderr)


def test_validate_mode_can_emit_digest(tmp_path: Path) -> None:
    rows = [
        {
            "event_id": 1,
            "kind": "INTENT",
            "correlation_id": "c-1",
            "payload": {"authoritative_input": {"x": 1}, "boundary": {"boundary_version": 1, "boundary_config_hash": "sha256:" + "0" * 64}},
        },
        {
            "event_id": 2,
            "kind": "DECISION",
            "correlation_id": "c-1",
            "payload": {"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}},
        },
    ]
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=True) for r in rows) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ensdg.cli",
            "--mode",
            "validate",
            "--input",
            str(path),
            "--digest",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env_with_src_path(),
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    assert result.stdout.strip().startswith("sha256:")
