"""Admit authored pilot drafts to a fresh local ledger; never submit reviews."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.queue import Store, PILOTS, current, accept

def main():
    store = Store(ROOT)
    with store.exclusive():
        state = store.load()
        for ident, _title, _family in PILOTS:
            job = state["jobs"][ident]
            if job["state"] == "review":
                if not any(h.get("phase") == "card" for h in job["history"]):
                    raise RuntimeError("review state without a research record: " + ident)
                print(ident + ": already authored; no change")
                continue
            if job["state"] != "todo" or job["history"]:
                raise RuntimeError("refusing to import into non-fresh job: " + ident)
            eligible = current(state)
            if eligible is None or eligible["id"] != ident:
                raise RuntimeError("unexpected queue order; inspect ledger manually")
            card = json.loads((ROOT / "research" / "pilots" / (ident + ".json")).read_text(encoding="utf8"))
            if card["status"] != "AUTHORED_NOT_INDEPENDENTLY_REVIEWED" or card["runtime_status"] != "NOT_TESTED":
                raise RuntimeError("pilot has unexpected research status: " + ident)
            accept(state, dict(id=ident, phase="card", token=job["token"],
                actor=dict(worker_id="offline-pilot-author", session_id="chat-20261119-pilots",
                           method="directly-read-installed-2021-help"),
                data=card["data"]))
            store.save(state)
            print(ident + ": admitted as research; awaiting independent review")
        assert all(state["jobs"][x]["state"] == "review" for x,_,_ in PILOTS)
        assert state["owner_gate"]["status"] == "pending"
        assert all(state["jobs"][x]["state"] == "todo" for x in ("parts","assemblies","mates"))
        print("Three research submissions recorded. L04 review and G1 owner gate remain CLOSED.")

if __name__ == "__main__":
    main()
