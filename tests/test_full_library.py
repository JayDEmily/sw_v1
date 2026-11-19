"""Integration tests for the local SW2021 Help catalogue and search API."""
import gzip
import json
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/"scripts"))
from search_library import find

class FullLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/"library/SOURCE_CATALOGUE_MANIFEST.json").read_text())
        cls.report=json.loads((ROOT/"library/SEARCH_BUILD_REPORT.json").read_text())
        cls.dossiers=json.loads((ROOT/"library/DOSSIER_REPORT.json").read_text())
        cls.db=ROOT/".cache/sw2021_search.sqlite"

    def test_all_archives_recorded(self):
        self.assertEqual(len(self.manifest["source_archives"]),14)
        self.assertGreater(self.manifest["unique_entries"],17000)
        self.assertGreater(self.manifest["counts_by_scope"]["in_scope"],4000)

    def test_source_text_and_no_false_claims(self):
        self.assertGreater(self.report["with_source_text"]/self.report["indexed_records"],0.95)
        self.assertEqual(self.report["integrity_check"],"ok")
        self.assertEqual(self.dossiers["reviewed_diagnostic_cards_generated"],0)
        self.assertEqual(self.dossiers["runtime_validated_diagnostic_cards_generated"],0)

    def test_dossier_count_and_evidence(self):
        n=0
        with gzip.open(ROOT/"library/topic_dossiers.jsonl.gz","rt") as f:
            for line in f:
                row=json.loads(line);n+=1
                self.assertEqual(row["review_status"],"unreviewed")
                self.assertEqual(row["runtime_status"],"untested")
                self.assertEqual(row["hypotheses"],[])
                self.assertEqual(row["diagnostic_tests"],[])
        self.assertEqual(n,self.manifest["unique_entries"])

    def test_search_shell_failure(self):
        rows=find("shell fails",limit=20,db=self.db)
        self.assertTrue(any(x["source"]=="core" and "Shell" in x["title"] for x in rows))

    def test_search_concentric_mate(self):
        rows=find("concentric mate",limit=20,db=self.db)
        self.assertTrue(any(x["source"]=="core" and "Concentric Mate" in x["title"] for x in rows))

    def test_search_flow_cam_plastics(self):
        self.assertTrue(find("turbulent flow",limit=10,source="flow",db=self.db))
        self.assertTrue(find("milling toolpath",limit=10,source="cam_milling",db=self.db))
        self.assertTrue(find("mesh quality",limit=10,source="plastics",db=self.db))

    def test_negative_search(self):
        self.assertEqual(find("qzxvunarbitraryxyz",db=self.db),[])

    def test_in_scope_local_pages_resolved(self):
        c=sqlite3.connect("file:"+str(self.db)+"?mode=ro",uri=True)
        try:
            missing=c.execute("SELECT COUNT(*) FROM topics WHERE scope='in_scope' AND text_status='toc_only' AND length(trim(coalesce(slug,'')))>0").fetchone()[0]
            self.assertEqual(missing,0)
            linked=c.execute("SELECT COUNT(*) FROM topics WHERE scope='in_scope' AND length(trim(coalesce(slug,'')))>0").fetchone()[0]
            self.assertGreater(linked,4300)
        finally:
            c.close()

    def test_source_content_and_review_distinct(self):
        c=sqlite3.connect("file:"+str(self.db)+"?mode=ro",uri=True)
        try:
            self.assertEqual(c.execute("PRAGMA integrity_check").fetchone()[0],"ok")
            self.assertEqual(c.execute("SELECT COUNT(*) FROM topics WHERE review_status != 'unreviewed'").fetchone()[0],0)
            self.assertEqual(c.execute("SELECT COUNT(*) FROM topics WHERE runtime_status != 'untested'").fetchone()[0],0)
            self.assertEqual(c.execute("SELECT COUNT(*) FROM topics").fetchone()[0],self.manifest["unique_entries"])
        finally:
            c.close()

if __name__=="__main__":
    unittest.main()
