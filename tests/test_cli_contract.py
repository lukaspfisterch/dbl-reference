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


def test_replay_parse_error_has_rc_and_no_stdout(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text("{not json}\n", encoding="utf-8")

    r = subprocess.run(
        [sys.executable, "-m", "ensdg.cli", "--mode", "replay", "--input", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env_with_src_path(),
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert r.returncode == 3
    assert r.stdout == ""
    assert r.stderr.startswith("parse error:")
    _assert_single_line(r.stderr)


def test_replay_replay_error_has_rc_and_no_stdout(tmp_path: Path) -> None:
    rows = [
        {
            "event_id": 1,
            "kind": "DECISION",
            "correlation_id": "c-1",
            "payload": {
                "decision": "ALLOW",
                "policy_version": True,
                "authoritative_digest": "sha256:" + "0" * 64,
                "rationale": {},
            },
        }
    ]
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(x, ensure_ascii=True) for x in rows) + "\n", encoding="utf-8")

    r = subprocess.run(
        [sys.executable, "-m", "ensdg.cli", "--mode", "replay", "--input", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env_with_src_path(),
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert r.returncode == 5
    assert r.stdout == ""
    assert r.stderr.startswith("replay error:")
    _assert_single_line(r.stderr)


def test_replay_digest_emits_sha256_label(tmp_path: Path) -> None:
    rows = [
        {
            "event_id": 1,
            "kind": "DECISION",
            "correlation_id": "c-1",
            "payload": {
                "decision": "ALLOW",
                "policy_version": 1,
                "authoritative_digest": "sha256:" + "0" * 64,
                "rationale": {},
            },
        }
    ]
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(x, ensure_ascii=True) for x in rows) + "\n", encoding="utf-8")

    r = subprocess.run(
        [sys.executable, "-m", "ensdg.cli", "--mode", "replay", "--input", str(path), "--digest"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env_with_src_path(),
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert r.returncode == 0
    assert r.stderr == ""
    assert r.stdout.strip().startswith("sha256:")
