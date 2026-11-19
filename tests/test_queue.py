"""Pure synthetic checks. Nothing invokes SOLIDWORKS or an external model."""
import copy
import json
import tempfile
from pathlib import Path
import unittest
from src.queue import (Store, initial, accept, current, owner_decision, retry, report,
                       validate_card, validate_discover, new_job)

URL = "https://help.solidworks.com/2021/english/SolidWorks/sldworks/t_Shell_Feature_Diagnostics.htm"

def source(url=URL, status="directly-opened"):
    return dict(url=url, section="Shell diagnostics", fact="Diagnostic tool is present", status=status)

def outcome(observation):
    return dict(observation=observation, meaning="Observation narrows one hypothesis",
                limits="Other possible causes remain", next_step="Examine the next condition")

def card():
    return dict(sources=[source()], symptoms=["Feature fails"],
                rivals=["A fault", "B fault"],
                probes=[dict(id="probe-synth", test="Inspect diagnostic output",
                    mode="ui_only", conditions="Disposable part, 1 mm, no side effects",
                    rivals="A versus B", basis="2021 documented; source 1",
                    member="not applicable", outcomes=[outcome("Pass"), outcome("Inconclusive: no output")])],
                limitations=["Cannot infer full feature success"])

def reply(state, data, actor="researcher", session="research-session"):
    j = current(state)
    return dict(id=j["id"], phase="review" if j["state"] == "review" else j["kind"],
                token=j["token"], data=data,
                actor=dict(worker_id=actor, session_id=session, method="synthetic-fixture"))

def review(verdict="approve", reopened_status="directly-opened"):
    return dict(verdict=verdict, checks=["Confirmed exact 2021 text and compared rivals"],
                reason="Source evidence maps to claims", independence="distinct-worker-and-context",
                reopened_sources=[dict(url=URL, section="Shell diagnostics", finding="Text supports narrower claim",
                                      access_mode=reopened_status)])


class QueueTests(unittest.TestCase):
    def test_initial_gate_prevents_discovery(self):
        s=initial()
        self.assertEqual(current(s)["id"], "shell")
        self.assertEqual(report(s)["owner_gate"], "pending")
        self.assertEqual(len(s["jobs"]), 6)
        s["jobs"]["shell"]["state"]="blocked"
        self.assertEqual(current(s)["id"], "spline-3d")
        for x in s["pilot_ids"]:
            s["jobs"][x]["state"]="blocked"
        self.assertIsNone(current(s))
        self.assertEqual(s["jobs"]["parts"]["state"], "todo")

    def test_owner_cannot_approve_early(self):
        s=initial()
        with self.assertRaisesRegex(ValueError,"three approved pilots"):
            owner_decision(s,dict(decision="proceed",owner_verbatim="Go", origin="chat", recorded_at="2026-11-19"))

    def test_reject_empty_sources_or_inconclusive_missing(self):
        x=card();x["sources"]=[]
        with self.assertRaises(ValueError):validate_card(x)
        x=card();x["probes"][0]["outcomes"]= [outcome("Pass"), outcome("Fail")]
        with self.assertRaisesRegex(ValueError,"inconclusive"):validate_card(x)

    def test_reject_invalid_release_url(self):
        x=card();x["sources"][0]["url"]="https://help.solidworks.com/2024/english/no"
        with self.assertRaisesRegex(ValueError,"2021"):validate_card(x)

    def test_reject_bad_discovery_and_alias_collision(self):
        x=dict(sources=[source()],children=[dict(id="abc", kind="card", title="A", url=URL),
                                               dict(id="abc", kind="card", title="B", url=URL)],
               exclusions=[], reconciliation=dict(secondary_sources=[],findings=[],unresolved=[]))
        with self.assertRaisesRegex(ValueError,"duplicate canonical"):validate_discover(x)

    def test_reject_stale_token_without_mutating(self):
        s=initial();r=reply(s,card());r["token"]="wrong"
        snapshot=copy.deepcopy(s)
        with self.assertRaisesRegex(ValueError,"stale"):accept(s,r)
        self.assertEqual(s,snapshot)

    def test_reject_self_review_and_index_only_review(self):
        s=initial();accept(s,reply(s,card()))
        for ident in ["spline-3d", "mate-concentric"]:
            accept(s,reply(s,card()))
        self.assertEqual(current(s)["state"],"review")
        with self.assertRaisesRegex(ValueError,"self-review"):
            accept(s,reply(s,review(),"researcher","review-session"))
        with self.assertRaisesRegex(ValueError,"search index alone"):
            accept(s,reply(s,review(reopened_status="source-indexed"),"reviewer","review-session"))
        self.assertEqual(current(s)["state"],"review")

    def test_approved_first_pilot_still_holds_discovery(self):
        s=initial()
        for ident in ["shell", "spline-3d", "mate-concentric"]:
            accept(s,reply(s,card()))
        accept(s,reply(s,review(),"reviewer","review-session"))
        self.assertEqual(s["jobs"]["shell"]["state"],"done")
        self.assertEqual(current(s)["id"],"spline-3d")
        self.assertEqual(s["jobs"]["parts"]["state"],"todo")

    def test_explicit_block_continues_pilots_only(self):
        s=initial()
        for ident in ["shell", "spline-3d", "mate-concentric"]:
            accept(s,reply(s,card()))
        accept(s,reply(s,{"blocked":"2021 Help body not accessible"},"reviewer","review-session"))
        self.assertEqual(s["jobs"]["shell"]["state"],"blocked")
        self.assertEqual(len(s["exceptions"]),1)
        self.assertEqual(current(s)["id"],"spline-3d")
        retry(s,"shell","New offline CHM evidence available")
        self.assertEqual(s["exceptions"][0]["status"],"reopened")

    def test_full_review_then_explicit_owner_decision(self):
        s=initial()
        for ident in ["shell","spline-3d","mate-concentric"]:
            self.assertEqual(current(s)["id"],ident)
            accept(s,reply(s,card()))
        for ident in ["shell","spline-3d","mate-concentric"]:
            self.assertEqual(current(s)["id"],ident)
            accept(s,reply(s,review(),"reviewer-"+ident,"review-session-"+ident))
        self.assertIsNone(current(s))
        with self.assertRaisesRegex(ValueError,"missing/empty"):
            owner_decision(s,dict(decision="proceed",owner_verbatim="",origin="chat",recorded_at="2026-11-19"))
        owner_decision(s,dict(decision="proceed",owner_verbatim="Approved",origin="user-chat-19-nov",recorded_at="2026-11-19"))
        self.assertEqual(current(s)["id"],"parts")

    def test_revisions_limit_and_history_kept(self):
        s=initial()
        for ident in ["shell", "spline-3d", "mate-concentric"]:
            accept(s,reply(s,card()))
        for i in range(3):
            self.assertEqual(current(s)["id"],"shell")
            accept(s,reply(s,review(verdict="revise"),"reviewer-"+str(i),"review-session-"+str(i)))
            if i<2:
                # Retry is prioritised only after other pilot drafts exist.
                accept(s,reply(s,card()))
        self.assertEqual(s["jobs"]["shell"]["state"],"blocked")
        self.assertEqual(len(s["jobs"]["shell"]["history"]),6)

    def test_persistence_backup_hash_and_corruption_halts(self):
        with tempfile.TemporaryDirectory() as tmp:
            st=Store(tmp)
            with st.exclusive():
                s=st.load();st.save(s)
            with st.exclusive():
                ss=st.load();accept(ss,reply(ss,card()));st.save(ss)
            self.assertTrue((Path(tmp)/"ledger.json.bak").exists())
            self.assertEqual(st.load()["jobs"]["shell"]["state"],"review")
            (Path(tmp)/"ledger.json").write_text("not json")
            with self.assertRaisesRegex(ValueError,"do not auto-overwrite"):st.load()
            self.assertTrue((Path(tmp)/"ledger.json.bak").exists())

    def test_lock_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            st=Store(tmp)
            with st.exclusive():
                with self.assertRaisesRegex(RuntimeError,"locked"):
                    with st.exclusive():pass
            self.assertFalse(st.lock.exists())

    def test_coverage_never_claims_complete(self):
        s=initial();r=report(s)
        self.assertFalse(r["by_family"]["parts"]["inventory_complete"])
        self.assertEqual(r["by_family"]["parts"]["cards_runtime_untested"],2)


if __name__ == "__main__":
    unittest.main()
