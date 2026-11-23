#!/usr/bin/env python3
"""Unit tests for scripts/analyze_labels.py."""

import csv
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_labels as al  # noqa: E402


SAMPLE_ISSUES = [
    {
        "number": 1,
        "state": "open",
        "labels": [{"name": "jetty"}, {"name": "os: Ubuntu Noble"}, {"name": "easy"}],
    },
    {
        "number": 2,
        "state": "closed",
        "labels": [{"name": "jetty"}, {"name": "os: Ubuntu Noble"}, {"name": "hard"}],
    },
    {
        "number": 3,
        "state": "closed",
        "labels": [{"name": "jetty"}, {"name": "os: Windows"}, {"name": "easy"}],
    },
    {
        "number": 4,
        "state": "OPEN",  # `gh issue list --json` uppercase style
        "labels": ["jetty", "os: Windows"],  # string label style
    },
    {
        "number": 5,
        "state": "closed",
        "labels": [{"name": "ionic"}, {"name": "os: Ubuntu Noble"}],
    },
    {
        "number": 6,
        "state": "open",
        "labels": [{"name": "jetty"}, {"name": "os: MacOS"}],
        "pull_request": {"url": "https://api.github.com/repos/o/r/pulls/6"},
    },
]


class AnalyzeLabelsTest(unittest.TestCase):
    def test_jetty_subset_excludes_prs_and_computes_percentages(self):
        result = al.analyze_issues(
            SAMPLE_ISSUES,
            repository="gazebosim/gazebo_test_cases",
            include_labels=["jetty"],
        )

        self.assertEqual(result.summary.total_issues, 4)
        self.assertEqual(result.summary.open_issues, 2)
        self.assertEqual(result.summary.closed_issues, 2)
        self.assertAlmostEqual(result.summary.open_pct, 50.0)
        self.assertAlmostEqual(result.summary.closed_pct, 50.0)

        by_label = {row.label: row for row in result.labels}
        self.assertNotIn("ionic", by_label)
        self.assertNotIn("os: MacOS", by_label)  # PR #6 excluded

        self.assertEqual(by_label["jetty"].open, 2)
        self.assertEqual(by_label["jetty"].closed, 2)
        self.assertEqual(by_label["jetty"].total, 4)
        self.assertAlmostEqual(by_label["jetty"].open_pct, 50.0)
        self.assertAlmostEqual(by_label["jetty"].closed_pct, 50.0)
        self.assertAlmostEqual(by_label["jetty"].subset_pct, 100.0)

        self.assertEqual(by_label["os: Ubuntu Noble"].open, 1)
        self.assertEqual(by_label["os: Ubuntu Noble"].closed, 1)
        self.assertAlmostEqual(by_label["os: Ubuntu Noble"].open_pct, 50.0)
        self.assertAlmostEqual(by_label["os: Ubuntu Noble"].closed_pct, 50.0)
        self.assertAlmostEqual(by_label["os: Ubuntu Noble"].subset_pct, 50.0)

        self.assertEqual(by_label["hard"].open, 0)
        self.assertEqual(by_label["hard"].closed, 1)
        self.assertAlmostEqual(by_label["hard"].open_pct, 0.0)
        self.assertAlmostEqual(by_label["hard"].closed_pct, 100.0)

    def test_include_prs_and_exclude_labels(self):
        result = al.analyze_issues(
            SAMPLE_ISSUES,
            repository="gazebosim/gazebo_test_cases",
            include_labels=["jetty"],
            exclude_labels=["hard"],
            include_prs=True,
            exclude_filter_labels=True,
        )

        # Issues #1, #3, #4, #6 (#2 excluded due to 'hard')
        self.assertEqual(result.summary.total_issues, 4)
        by_label = {row.label: row for row in result.labels}
        self.assertNotIn("jetty", by_label)
        self.assertNotIn("hard", by_label)
        self.assertIn("os: MacOS", by_label)
        self.assertAlmostEqual(by_label["os: MacOS"].open_pct, 100.0)

    def test_target_labels_includes_zero_count_labels(self):
        result = al.analyze_issues(
            SAMPLE_ISSUES,
            repository="gazebosim/gazebo_test_cases",
            include_labels=["jetty"],
            target_labels=["easy", "nonexistent"],
        )

        self.assertEqual([r.label for r in result.labels], ["easy", "nonexistent"])
        zero = result.labels[1]
        self.assertEqual(zero.total, 0)
        self.assertEqual(zero.open_pct, 0.0)
        self.assertEqual(zero.closed_pct, 0.0)

    def test_sorting_options(self):
        result = al.analyze_issues(
            SAMPLE_ISSUES,
            repository="gazebosim/gazebo_test_cases",
            include_labels=["jetty"],
            exclude_filter_labels=True,
            sort_by="closed-pct",
            order="desc",
        )
        self.assertEqual(result.labels[0].label, "hard")
        self.assertAlmostEqual(result.labels[0].closed_pct, 100.0)

        by_name = al.analyze_issues(
            SAMPLE_ISSUES,
            repository="gazebosim/gazebo_test_cases",
            include_labels=["jetty"],
            exclude_filter_labels=True,
            sort_by="name",
        )
        names = [r.label for r in by_name.labels]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_output_formats(self):
        result = al.analyze_issues(
            SAMPLE_ISSUES,
            repository="gazebosim/gazebo_test_cases",
            include_labels=["jetty"],
        )

        table_out = al.format_result(result, "table")
        self.assertIn("Repository: gazebosim/gazebo_test_cases", table_out)
        self.assertIn("Filter labels: jetty", table_out)
        self.assertIn("os: Ubuntu Noble", table_out)

        md_out = al.format_result(result, "markdown")
        self.assertIn("| Label | Open | Closed | Total | Open % | Closed % | Subset % |", md_out)
        self.assertIn("| `jetty` | 2 | 2 | 4 | 50.0% | 50.0% | 100.0% |", md_out)

        csv_out = al.format_result(result, "csv")
        rows = list(csv.DictReader(io.StringIO(csv_out)))
        self.assertEqual(rows[0]["label"], "jetty")
        self.assertEqual(rows[0]["open_pct"], "50.00")

        json_out = json.loads(al.format_result(result, "json"))
        self.assertEqual(json_out["summary"]["total_issues"], 4)
        self.assertEqual(len(json_out["labels"]), 5)

    def test_parse_next_link(self):
        header = (
            '<https://api.github.com/repos/o/r/issues?page=2>; rel="next", '
            '<https://api.github.com/repos/o/r/issues?page=5>; rel="last"'
        )
        self.assertEqual(
            al.parse_next_link(header),
            "https://api.github.com/repos/o/r/issues?page=2",
        )
        self.assertIsNone(
            al.parse_next_link('<https://api.github.com/repos/o/r/issues?page=1>; rel="prev"')
        )
        self.assertIsNone(al.parse_next_link(None))

    def test_fetch_issues_pagination(self):
        page1 = [{"number": 1, "state": "open", "labels": [{"name": "jetty"}]}]
        page2 = [{"number": 2, "state": "closed", "labels": [{"name": "jetty"}]}]

        class FakeResponse:
            def __init__(self, body, link=None):
                self._body = json.dumps(body).encode("utf-8")
                self.headers = {"Link": link} if link else {}

            def read(self):
                return self._body

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        responses = [
            FakeResponse(
                page1,
                link='<https://api.github.com/repos/gazebosim/gazebo_test_cases/issues?page=2>; rel="next"',
            ),
            FakeResponse(page2),
        ]

        with mock.patch("urllib.request.urlopen", side_effect=responses) as mock_open:
            issues = al.fetch_issues(
                owner="gazebosim",
                repo="gazebo_test_cases",
                include_labels=["jetty"],
                token="test-token",
            )

        self.assertEqual(len(issues), 2)
        self.assertEqual(mock_open.call_count, 2)
        first_req = mock_open.call_args_list[0].args[0]
        self.assertIn("labels=jetty", first_req.full_url)
        self.assertEqual(first_req.get_header("Authorization"), "Bearer test-token")

    def test_cli_with_input_json(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(SAMPLE_ISSUES, tmp)
            tmp_path = tmp.name

        try:
            buf = io.StringIO()
            with mock.patch("sys.stdout", buf):
                exit_code = al.main(
                    [
                        "--input-json",
                        tmp_path,
                        "--label",
                        "jetty",
                        "--format",
                        "json",
                    ]
                )
            self.assertEqual(exit_code, 0)
            data = json.loads(buf.getvalue())
            self.assertEqual(data["summary"]["total_issues"], 4)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
