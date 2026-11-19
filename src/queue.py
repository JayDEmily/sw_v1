"""Auditable, single-writer SW2021 research queue. Python 3.8+ stdlib."""
import contextlib
import copy
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import uuid

PILOTS = (("shell", "Shell", "parts"), ("spline-3d", "3D spline", "parts"),
          ("mate-concentric", "Concentric mate", "mates"))
ROOTS = (("parts", "Part modelling"), ("assemblies", "Assembly modelling"),
         ("mates", "Mate families and subtypes"))
PHASES = ("card", "discover", "review")
STATES = ("todo", "review", "done", "blocked")
SCHEMA = 2
VALID_MODES = ("read_only_api", "disposable_copy", "ui_only", "unknown")
ID = re.compile(r"[a-z0-9][a-z0-9-]*\Z")


def new_job(ident, kind, title, family, url=""):
    return dict(id=ident, kind=kind, title=title, family=family, url=url,
                state="todo", token=uuid.uuid4().hex, history=[],
                attempts=0, runtime_status="not_tested")


def initial():
    jobs = {}
    for ident, title, family in PILOTS:
        jobs[ident] = new_job(ident, "card", title, family)
    for ident, title in ROOTS:
        jobs[ident] = new_job(ident, "discover", title, ident)
    return dict(schema=SCHEMA, pilot_ids=[p[0] for p in PILOTS], jobs=jobs,
                owner_gate=dict(status="pending", decision=None),
                exceptions=[], events=[])


def check_state(state):
    if not isinstance(state, dict) or state.get("schema") != SCHEMA:
        raise ValueError("unsupported or corrupted ledger schema: no automatic migration")
    if not set(p[0] for p in PILOTS).issubset(set(state.get("jobs", {}))):
        raise ValueError("missing pilot jobs")
    for ident, job in state["jobs"].items():
        if not ID.fullmatch(ident) or job["id"] != ident or job["state"] not in STATES:
            raise ValueError("invalid job identity or state: " + ident)
        if job["kind"] not in ("card", "discover"):
            raise ValueError("invalid job kind: " + ident)
        if not job.get("token") or not isinstance(job.get("history"), list):
            raise ValueError("incomplete job: " + ident)
    if state.get("owner_gate", {}).get("status") not in ("pending", "proceed", "revise", "stop"):
        raise ValueError("invalid owner gate state")
    return state


class Store:
    def __init__(self, folder):
        self.folder = Path(folder).resolve()
        self.path = self.folder / "ledger.json"
        self.lock = self.folder / ".ledger.lock"
        self.backup = self.folder / "ledger.json.bak"

    @contextlib.contextmanager
    def exclusive(self):
        try:
            self.lock.mkdir()
        except FileExistsError:
            raise RuntimeError("ledger locked: another coordinator or stale lock; inspect before any recovery")
        try:
            (self.lock / "owner.json").write_text(json.dumps(dict(pid=os.getpid(),
                host=socket.gethostname(), started=time.time())), encoding="utf8")
            yield
        finally:
            shutil.rmtree(str(self.lock))

    def load(self):
        if not self.path.exists():
            return initial()
        try:
            return check_state(json.loads(self.path.read_text(encoding="utf8")))
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as err:
            raise ValueError("ledger unreadable; inspect ledger.json.bak, do not auto-overwrite: " + str(err))

    def save(self, state):
        check_state(state)
        data = json.dumps(state, indent=2, ensure_ascii=False) + "\n"
        fd, scratch = tempfile.mkstemp(prefix=".ledger-", suffix=".tmp", dir=str(self.folder))
        try:
            with os.fdopen(fd, "w", encoding="utf8") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            if self.path.exists():
                fd2, scratch_backup = tempfile.mkstemp(prefix=".ledger-bak-", dir=str(self.folder))
                os.close(fd2)
                try:
                    shutil.copyfile(str(self.path), scratch_backup)
                    os.replace(scratch_backup, str(self.backup))
                finally:
                    if os.path.exists(scratch_backup):
                        os.unlink(scratch_backup)
            os.replace(scratch, str(self.path))
        finally:
            if os.path.exists(scratch):
                os.unlink(scratch)


def require(cond, msg):
    if not cond:
        raise ValueError(msg)


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), "missing/empty " + label)


def valid_source(src):
    require(isinstance(src, dict), "source must be object")
    for key in ("url", "section", "fact", "status"):
        nonempty(src.get(key), "source." + key)
    require(src["url"].lower().startswith("https://help.solidworks.com/2021/"),
            "2021 primary-source URL required")
    require(src["status"] in ("source-indexed", "directly-opened", "offline-chm"),
            "source accessibility/status must be explicit")


def validate_card(data):
    for k in ("sources", "symptoms", "rivals", "probes", "limitations"):
        require(isinstance(data.get(k), list) and data[k], "card needs nonempty " + k)
    for src in data["sources"]:
        valid_source(src)
    for symptom in data["symptoms"]:
        nonempty(symptom, "symptom")
    for rival in data["rivals"]:
        nonempty(rival, "rival")
    for limit in data["limitations"]:
        nonempty(limit, "limitation")
    for probe in data["probes"]:
        require(isinstance(probe, dict), "probe must be object")
        for k in ("id", "test", "mode", "conditions", "rivals", "basis", "member"):
            nonempty(probe.get(k), "probe." + k)
        require(ID.fullmatch(probe["id"]) is not None, "invalid probe ID")
        require(probe["mode"] in VALID_MODES, "invalid probe mode")
        require(isinstance(probe.get("outcomes"), list) and len(probe["outcomes"]) >= 2,
                "probe must have at least two possible outcomes")
        for outcome in probe["outcomes"]:
            require(isinstance(outcome, dict), "outcome must be object")
            for k in ("observation", "meaning", "limits", "next_step"):
                nonempty(outcome.get(k), "outcome." + k)
        require(any("inconclusive" in x["observation"].lower() for x in probe["outcomes"]),
                "probe must describe an explicitly inconclusive outcome")


def validate_discover(data):
    require(isinstance(data.get("sources"), list) and data["sources"], "discovery sources required")
    for src in data["sources"]:
        valid_source(src)
    for k in ("children", "exclusions"):
        require(isinstance(data.get(k), list), "discovery " + k + " must be list")
    require(isinstance(data.get("reconciliation"), dict), "discovery reconciliation required")
    for k in ("secondary_sources", "findings", "unresolved"):
        require(isinstance(data["reconciliation"].get(k), list), "reconciliation needs " + k)
    for c in data["children"]:
        require(isinstance(c, dict), "child object required")
        for k in ("id", "kind", "title", "url"):
            nonempty(c.get(k), "child." + k)
        require(ID.fullmatch(c["id"]) is not None, "invalid child ID")
        require(c["kind"] in ("card", "discover"), "invalid child kind")
        require(c["url"].lower().startswith("https://help.solidworks.com/2021/"), "2021 child URL")
    require(len(set(c["id"] for c in data["children"])) == len(data["children"]),
            "duplicate canonical child in same discovery")


def validate_review(data, actor, prior_actor, prior_data):
    require(data.get("verdict") in ("approve", "revise"), "review verdict must be approve/revise")
    require(isinstance(data.get("checks"), list) and data["checks"], "review checks required")
    nonempty(data.get("reason"), "review reason")
    for check in data["checks"]:
        nonempty(check, "review check")
    require(actor["worker_id"] != prior_actor["worker_id"], "self-review worker ID forbidden")
    require(actor["session_id"] != prior_actor["session_id"], "self-review session forbidden")
    require(data.get("independence") == "distinct-worker-and-context",
            "independence must be explicitly attested; do not fake this")
    reopened = data.get("reopened_sources")
    require(isinstance(reopened, list) and reopened, "review must reopen primary evidence")
    orig_urls = {s["url"] for s in prior_data["sources"]}
    for src in reopened:
        require(isinstance(src, dict), "reopened source must be object")
        for k in ("url", "section", "finding", "access_mode"):
            nonempty(src.get(k), "reopened_source." + k)
        require(src["url"] in orig_urls, "review source not in research evidence")
        require(src["access_mode"] in ("directly-opened", "offline-chm"),
                "search index alone is insufficient for independent source reopening")
    require(len({x["url"] for x in reopened}) >= 1, "no reopened sources")


def validate_actor(actor):
    require(isinstance(actor, dict), "actor object required")
    for k in ("worker_id", "session_id", "method"):
        nonempty(actor.get(k), "actor." + k)


def can_scale(state):
    return state["owner_gate"]["status"] == "proceed"


def pilot_complete(state):
    return all(state["jobs"][x]["state"] == "done" for x in state["pilot_ids"])


def current(state):
    if not can_scale(state):
        # Author all three pilots first so an independent reviewer can assess the set.
        for desired in ("todo", "review"):
            for key in state["pilot_ids"]:
                if state["jobs"][key]["state"] == desired:
                    return state["jobs"][key]
        return None
    return next((j for j in state["jobs"].values()
                 if j["state"] in ("todo", "review")), None)


def contract(job):
    if job["state"] == "review":
        return {"verdict": "approve|revise", "checks": ["specific findings"],
                "reason": "reason", "independence": "distinct-worker-and-context",
                "reopened_sources": [{"url": "same as research source", "section": "...",
                                      "finding": "...", "access_mode": "directly-opened|offline-chm"}]}
    if job["kind"] == "card":
        return {"sources": [{"url": "2021 official URL", "section": "...", "fact": "paraphrase",
                              "status": "source-indexed|directly-opened|offline-chm"}],
                "symptoms": ["..."], "rivals": ["..."], "probes": [{"id": "...",
                    "test": "...", "mode": "read_only_api|disposable_copy|ui_only|unknown",
                    "conditions": "...", "rivals": "...", "basis": "...", "member": "...",
                    "outcomes": [{"observation": "including inconclusive", "meaning": "...",
                                  "limits": "...", "next_step": "..."}]}], "limitations": ["..."]}
    return {"sources": [], "children": [], "exclusions": [],
            "reconciliation": {"secondary_sources": [], "findings": [], "unresolved": []}}


def prompt(job, work_order):
    phase = "review" if job["state"] == "review" else job["kind"]
    return (work_order + "\n\nJOB ENVELOPE\n" + json.dumps(dict(
        id=job["id"], kind=job["kind"], title=job["title"], phase=phase,
        token=job["token"], history=job["history"], contract=contract(job))) +
        "\nReply with one JSON object containing id, phase, token, actor(worker_id,session_id,method), data.\n")


def accept(state, response):
    job = current(state)
    require(job is not None, "no eligible job: pilot/owner gate or queue stopped")
    require(isinstance(response, dict), "reply object required")
    phase = "review" if job["state"] == "review" else job["kind"]
    require((response.get("id"), response.get("phase"), response.get("token")) ==
            (job["id"], phase, job["token"]), "stale or incorrect reply/token")
    actor = response.get("actor")
    validate_actor(actor)
    data = response.get("data")
    require(isinstance(data, dict), "reply data object required")
    if data.get("blocked"):
        nonempty(data["blocked"], "block reason")
        job["state"] = "blocked"
        state["exceptions"].append(dict(job=job["id"], phase=phase, reason=data["blocked"],
                                        timestamp=time.time(), status="open"))
    elif phase == "card":
        validate_card(data)
        job["state"] = "review"
    elif phase == "discover":
        validate_discover(data)
        job["state"] = "review"
    else:
        prior = next((h for h in reversed(job["history"]) if h["phase"] == job["kind"]), None)
        require(prior is not None, "review without research")
        validate_review(data, actor, prior["actor"], prior["data"])
        if data["verdict"] == "approve":
            job["state"] = "done"
            if job["kind"] == "discover":
                for child in prior["data"]["children"]:
                    previous = state["jobs"].get(child["id"])
                    if previous:
                        require((previous["kind"], previous["title"], previous["url"]) ==
                                (child["kind"], child["title"], child["url"]),
                                "discovery canonical ID collision; reconcile before approval")
                    else:
                        state["jobs"][child["id"]] = new_job(child["id"], child["kind"],
                                                                child["title"], job["family"], child["url"])
        else:
            job["attempts"] += 1
            job["state"] = "blocked" if job["attempts"] >= 3 else "todo"
            if job["state"] == "blocked":
                state["exceptions"].append(dict(job=job["id"], phase=phase,
                    reason="review revision limit: " + data["reason"],
                    timestamp=time.time(), status="open"))
    job["history"].append(copy.deepcopy(response))
    job["token"] = uuid.uuid4().hex
    state["events"].append(dict(event="accept", job=job["id"], phase=phase,
                                result=job["state"], timestamp=time.time()))


def owner_decision(state, payload):
    require(isinstance(payload, dict), "owner decision must be object")
    require(state["owner_gate"]["status"] == "pending", "owner gate already recorded")
    require(pilot_complete(state), "cannot decide gate before three approved pilots")
    require(payload.get("decision") in ("proceed", "revise", "stop"), "invalid owner decision")
    for field in ("owner_verbatim", "origin", "recorded_at"):
        nonempty(payload.get(field), "owner_decision." + field)
    state["owner_gate"] = dict(status=payload["decision"], decision=payload)
    state["events"].append(dict(event="owner_gate", decision=payload["decision"],
                                timestamp=time.time()))


def retry(state, ident, explanation):
    require(ident in state["jobs"] and state["jobs"][ident]["state"] == "blocked",
            "only blocked tasks can be reopened")
    nonempty(explanation, "retry rationale")
    job = state["jobs"][ident]
    job["state"] = "todo"
    job["token"] = uuid.uuid4().hex
    state["events"].append(dict(event="retry", job=ident, rationale=explanation,
                                timestamp=time.time()))
    for item in state["exceptions"]:
        if item["job"] == ident and item["status"] == "open":
            item["status"] = "reopened"


def report(state):
    from collections import Counter
    by_family = {}
    for family in ("parts", "assemblies", "mates"):
        selected = [j for j in state["jobs"].values() if j["family"] == family]
        counts = Counter(j["state"] for j in selected)
        cards = [j for j in selected if j["kind"] == "card"]
        by_family[family] = dict(total_jobs=len(selected), states=dict(counts),
            cards=len(cards), cards_evidence_reviewed=sum(j["state"] == "done" for j in cards),
            cards_runtime_untested=sum(j["runtime_status"] == "not_tested" for j in cards),
            blocked=sum(j["state"] == "blocked" for j in selected),
            unreviewed=sum(j["state"] in ("todo", "review", "blocked") for j in selected),
            inventory_complete=False)  # Only L05 reconciliation can establish completeness.
    return dict(schema=SCHEMA, pilot_states={x:state["jobs"][x]["state"] for x in state["pilot_ids"]},
        owner_gate=state["owner_gate"]["status"], by_family=by_family,
        unresolved_exceptions=[x for x in state["exceptions"] if x["status"] == "open"],
        next_job=current(state)["id"] if current(state) else None)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    cmd = argv[0] if argv else "status"
    store = Store(Path.cwd())
    with store.exclusive():
        state = store.load()
        if cmd == "status":
            print(json.dumps(report(state), indent=2))
            if not store.path.exists():
                store.save(state)
        elif cmd == "next":
            job = current(state)
            if job:
                print(prompt(job, (Path(__file__).resolve().parent.parent / "WORK_ORDER.md").read_text(encoding="utf8")))
            else:
                print(json.dumps(dict(message="No eligible job; check pilot/owner gate and blocked records", status=report(state))))
            if not store.path.exists():
                store.save(state)
        elif cmd == "accept":
            require(len(argv) == 2, "accept RESPONSE.json")
            accept(state, json.loads(Path(argv[1]).read_text(encoding="utf8")))
            store.save(state)
            print(json.dumps(report(state), indent=2))
        elif cmd == "owner-decision":
            require(len(argv) == 2, "owner-decision OWNER.json (owner instruction required)")
            owner_decision(state, json.loads(Path(argv[1]).read_text(encoding="utf8")))
            store.save(state)
            print(json.dumps(report(state), indent=2))
        elif cmd == "retry":
            require(len(argv) >= 3, "retry ID REASON...")
            retry(state, argv[1], " ".join(argv[2:]))
            store.save(state)
            print(json.dumps(report(state), indent=2))
        elif cmd == "run":
            require(len(argv) >= 3, "run MAX_CALLS EXTERNAL_WORKER [ARGS...]")
            calls = int(argv[1]); require(0 < calls <= 1000, "invalid call budget")
            work_order = (Path(__file__).resolve().parent.parent / "WORK_ORDER.md").read_text(encoding="utf8")
            if not store.path.exists():
                store.save(state)
            for _ in range(calls):
                job = current(state)
                if not job:
                    break
                result = subprocess.run(argv[2:], input=prompt(job, work_order),
                                        text=True, encoding="utf8", capture_output=True,
                                        timeout=1800, check=True)
                accept(state, json.loads(result.stdout))
                store.save(state)
            print(json.dumps(report(state), indent=2))
        else:
            raise ValueError("status | next | accept file.json | retry id reason | owner-decision file.json | run MAX_CALLS WORKER")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, FileNotFoundError, subprocess.SubprocessError) as err:
        print("ERROR: " + str(err), file=sys.stderr)
        sys.exit(2)
