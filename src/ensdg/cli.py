from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Optional

from .boundary import Boundary
from .example_governance import ExampleGovernance
from .replay import replay_normative, to_replay_view
from .example_rules import AcceptAll
from .runner import AdmissionRejected, DblRunner

RC_OK = 0
RC_USAGE = 2
RC_PARSE = 3
RC_INVARIANT = 4
RC_REPLAY = 5
RC_ADMISSION = 6


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="ensdg")
    p.add_argument("--policy-version", type=int, default=1)
    p.add_argument("--mode", choices=("demo", "replay", "validate"), default="demo")
    p.add_argument("--input", default="-")
    p.add_argument("--digest", action="store_true")
    args = p.parse_args(argv)

    if args.mode == "demo":
        boundary = Boundary(boundary_version=1, rules=AcceptAll())
        gov = ExampleGovernance()
        r = DblRunner(boundary=boundary, governance=gov, policy_version=args.policy_version)

        try:
            raw = _read_json(args.input)
        except Exception as exc:
            sys.stderr.write(f"parse error: {exc}\n")
            return RC_PARSE
        cid = raw.get("correlation_id", "c-1")
        inp = raw.get("input", raw)

        try:
            r.submit_intent(cid, inp, source="cli")
            r.decide(cid, source="cli")
            r.record_execution(cid, {"ok": True}, source="cli")
            r.record_proof(cid, {"evidence": "demo"}, source="cli")
        except AdmissionRejected:
            return RC_ADMISSION

        for e in r.V.events():
            sys.stdout.write(json.dumps(_event_to_obj(e), ensure_ascii=True, sort_keys=True, separators=(",", ":")))
            sys.stdout.write("\n")
        return RC_OK

    if args.mode == "replay":
        from .replay import ReplayError, normative_digest

        try:
            rows = _read_jsonl(args.input)
            events = [_obj_to_event(x) for x in rows]
        except Exception as exc:
            sys.stderr.write(f"parse error: {exc}\n")
            return RC_PARSE
        try:
            if args.digest:
                digest = normative_digest(to_replay_view(events))
            else:
                st = replay_normative(to_replay_view(events))
        except ReplayError as exc:
            sys.stderr.write(f"replay error: {exc}\n")
            return RC_REPLAY
        if args.digest:
            sys.stdout.write(digest)
            sys.stdout.write("\n")
            return RC_OK
        sys.stdout.write(
            json.dumps(
                {"decisions": {k: v.decision.value for k, v in st.decisions_by_correlation.items()}},
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        sys.stdout.write("\n")
        return RC_OK

    if args.mode == "validate":
        from .invariants import InvariantError, validate_stream
        from .replay import ReplayError, normative_digest

        try:
            rows = _read_jsonl(args.input)
            events = [_obj_to_event(x) for x in rows]
        except Exception as exc:
            sys.stderr.write(f"parse error: {exc}\n")
            return RC_PARSE
        try:
            validate_stream(events)
        except InvariantError as exc:
            sys.stderr.write(f"invariant error: {exc}\n")
            return RC_INVARIANT
        try:
            digest = normative_digest(to_replay_view(events))
        except ReplayError as exc:
            sys.stderr.write(f"replay error: {exc}\n")
            return RC_REPLAY
        if args.digest:
            sys.stdout.write(digest)
            sys.stdout.write("\n")
        return RC_OK

    return RC_USAGE


def _read_json(path: str) -> Any:
    if path == "-":
        return json.loads(sys.stdin.read() or "{}")
    with open(path, "r", encoding="utf-8") as f:
        return json.loads(f.read() or "{}")


def _read_jsonl(path: str) -> list[dict]:
    data: list[dict] = []
    stream = sys.stdin if path == "-" else open(path, "r", encoding="utf-8")
    try:
        for line in stream:
            s = line.strip()
            if not s:
                continue
            obj = json.loads(s)
            if not isinstance(obj, dict):
                raise ValueError("expected object per line")
            data.append(obj)
    finally:
        if path != "-":
            stream.close()
    return data


def _event_to_obj(e):
    return {
        "event_id": e.event_id,
        "kind": e.kind.value,
        "correlation_id": e.correlation_id,
        "payload": e.payload,
        "observed_at": e.observed_at,
        "source": e.source,
    }


def _obj_to_event(obj: dict):
    from .model import DblEvent, EventKind

    return DblEvent(
        event_id=int(obj["event_id"]),
        kind=EventKind(obj["kind"]),
        correlation_id=str(obj["correlation_id"]),
        payload=obj["payload"],
        observed_at=obj.get("observed_at"),
        source=obj.get("source"),
    )


if __name__ == "__main__":
    raise SystemExit(main())
