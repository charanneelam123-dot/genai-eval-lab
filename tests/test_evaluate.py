import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from evaluate import grade, run, save

class EvalTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(Path('data/cases.json').read_text())
    def test_forbidden_term_fails(self):
        self.assertFalse(grade('7 BANANA', self.cases[2])['passed'])
    def test_case_insensitive(self):
        self.assertTrue(grade('insufficient EVIDENCE', self.cases[1])['passed'])
    def test_fixture_results(self):
        report = run(self.cases)
        self.assertEqual(len(report['rows']), 12)
        self.assertEqual(report['mode'], 'fixture')
        self.assertEqual(report['summary']['grounded']['pass_rate'], 1)
    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            run([self.cases[0], self.cases[0]])
    def test_exports(self):
        with tempfile.TemporaryDirectory() as folder:
            save(run(self.cases), folder)
            self.assertTrue((Path(folder)/'report.md').exists())
            self.assertEqual(len((Path(folder)/'results.csv').read_text().splitlines()), 13)
    @patch('evaluate.complete', side_effect=RuntimeError('unavailable'))
    def test_provider_errors_recorded(self, mock):
        report = run(self.cases[:1], live=True)
        self.assertEqual(report['summary']['baseline']['errors'], 1)
        self.assertEqual(report['summary']['baseline']['pass_rate'], 0)

if __name__ == '__main__':
    unittest.main()
