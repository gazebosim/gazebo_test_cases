#!/usr/bin/env python3
"""Analyze open and closed GitHub issues broken down by label."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import csv
import io
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_OWNER = "gazebosim"
DEFAULT_REPO = "gazebo_test_cases"
GITHUB_API_BASE = "https://api.github.com"

SORT_KEYS = ("total", "open", "closed", "open-pct", "closed-pct", "name")
OUTPUT_FORMATS = ("table", "markdown", "csv", "json")


@dataclass(frozen=True)
class LabelStats:
    """Open/closed statistics for a single label within an issue subset."""

    label: str
    open: int
    closed: int
    total: int
    open_pct: float
    closed_pct: float
    subset_pct: float


@dataclass(frozen=True)
class AnalysisSummary:
    """Aggregate open/closed statistics for the filtered issue subset."""

    total_issues: int
    open_issues: int
    closed_issues: int
    open_pct: float
    closed_pct: float


@dataclass(frozen=True)
class AnalysisResult:
    """Complete analysis result including summary and per-label stats."""

    repository: str
    include_labels: list[str]
    exclude_labels: list[str]
    summary: AnalysisSummary
    labels: list[LabelStats]


def _calc_pct(part: int, whole: int) -> float:
    return (part / whole * 100.0) if whole > 0 else 0.0


def parse_next_link(link_header: str | None) -> str | None:
    """Extract the `rel="next"` URL from a GitHub API Link header."""
    if not link_header:
        return None
    for part in link_header.split(","):
        match = re.match(r'\s*<([^>]+)>\s*;\s*rel="([^"]+)"', part)
        if match and match.group(2) == "next":
            return match.group(1)
    return None


def resolve_github_token(explicit_token: str | None = None) -> str | None:
    """Resolve a GitHub token from CLI argument, environment, or `gh auth token`."""
    if explicit_token:
        return explicit_token
    for env_var in ("GITHUB_TOKEN", "GH_TOKEN"):
        token = os.getenv(env_var)
        if token:
            return token
    try:
        proc = subprocess.run(
            ["gh", "auth", "token"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode == 0:
        token = proc.stdout.strip()
        if token:
            return token
    return None


def _build_issues_url(
    owner: str,
    repo: str,
    include_labels: list[str],
) -> str:
    params: dict[str, str] = {"state": "all", "per_page": "100"}
    if include_labels:
        params["labels"] = ",".join(include_labels)
    query = urllib.parse.urlencode(params)
    return f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues?{query}"


def fetch_issues(
    owner: str,
    repo: str,
    include_labels: list[str] | None = None,
    token: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch all matching issues (including closed) from the GitHub REST API."""
    url: str | None = _build_issues_url(owner, repo, include_labels or [])
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "gazebo-test-cases-label-analyzer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    all_issues: list[dict[str, Any]] = []
    while url:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
                if not isinstance(payload, list):
                    raise RuntimeError(f"Unexpected GitHub API response: {payload}")
                all_issues.extend(payload)
                url = parse_next_link(resp.headers.get("Link"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            hint = ""
            if exc.code in (401, 403) and not token:
                hint = (
                    " (Hint: set GITHUB_TOKEN / GH_TOKEN, pass --token, "
                    "or authenticate with `gh auth login`.)"
                )
            raise RuntimeError(
                f"GitHub API request failed with HTTP {exc.code}: {detail}{hint}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Failed to reach GitHub API: {exc.reason}") from exc

    return all_issues


def extract_issue_labels(issue: dict[str, Any]) -> list[str]:
    """Return unique label names from an issue dict (REST or `gh` JSON format)."""
    raw_labels = issue.get("labels") or []
    seen: set[str] = set()
    names: list[str] = []
    for item in raw_labels:
        if isinstance(item, str):
            name = item
        elif isinstance(item, dict) and isinstance(item.get("name"), str):
            name = item["name"]
        else:
            continue
        if name not in seen:
            seen.add(name)
            names.append(name)
    return names


def is_pull_request(issue: dict[str, Any]) -> bool:
    """Return True if an item returned by the issues API is a pull request."""
    return "pull_request" in issue or bool(issue.get("isPullRequest"))


def normalize_issue_state(issue: dict[str, Any]) -> str:
    """Return normalized lowercase issue state ('open' or 'closed')."""
    return str(issue.get("state", "")).strip().lower()


def filter_issues(
    issues: list[dict[str, Any]],
    include_labels: list[str] | None = None,
    exclude_labels: list[str] | None = None,
    include_prs: bool = False,
) -> list[dict[str, Any]]:
    """Filter issues by PR status, required labels (AND), and excluded labels."""
    required = set(include_labels or [])
    excluded = set(exclude_labels or [])

    matched: list[dict[str, Any]] = []
    for issue in issues:
        if not include_prs and is_pull_request(issue):
            continue
        labels = set(extract_issue_labels(issue))
        if required and not required.issubset(labels):
            continue
        if excluded and excluded.intersection(labels):
            continue
        matched.append(issue)
    return matched


def sort_label_stats(
    stats: list[LabelStats],
    sort_by: str = "total",
    order: str | None = None,
) -> list[LabelStats]:
    """Sort LabelStats rows deterministically."""
    if sort_by not in SORT_KEYS:
        raise ValueError(f"Unsupported sort key '{sort_by}'. Expected one of {SORT_KEYS}.")

    if order is None:
        descending = sort_by != "name"
    else:
        descending = order == "desc"

    key_map = {
        "total": lambda s: (s.total, s.open, s.label.lower()),
        "open": lambda s: (s.open, s.total, s.label.lower()),
        "closed": lambda s: (s.closed, s.total, s.label.lower()),
        "open-pct": lambda s: (s.open_pct, s.total, s.label.lower()),
        "closed-pct": lambda s: (s.closed_pct, s.total, s.label.lower()),
        "name": lambda s: (s.label.lower(), s.label),
    }

    if sort_by == "name":
        return sorted(stats, key=key_map[sort_by], reverse=descending)

    # Keep alphabetical secondary tie-breaker ascending even when primary metric is descending.
    if descending:
        return sorted(
            stats,
            key=lambda s: (-key_map[sort_by](s)[0], -key_map[sort_by](s)[1], s.label.lower()),
        )
    return sorted(stats, key=key_map[sort_by])


def analyze_issues(
    issues: list[dict[str, Any]],
    repository: str,
    include_labels: list[str] | None = None,
    exclude_labels: list[str] | None = None,
    target_labels: list[str] | None = None,
    exclude_filter_labels: bool = False,
    include_prs: bool = False,
    sort_by: str = "total",
    order: str | None = None,
) -> AnalysisResult:
    """Filter issues and compute open/closed counts and percentages per label."""
    inc = list(include_labels or [])
    exc = list(exclude_labels or [])
    matched = filter_issues(
        issues,
        include_labels=inc,
        exclude_labels=exc,
        include_prs=include_prs,
    )

    open_total = 0
    closed_total = 0
    counts: dict[str, list[int]] = {}  # label -> [open_count, closed_count]

    for issue in matched:
        state = normalize_issue_state(issue)
        if state == "open":
            open_total += 1
            state_idx = 0
        elif state == "closed":
            closed_total += 1
            state_idx = 1
        else:
            continue

        for label in extract_issue_labels(issue):
            if label not in counts:
                counts[label] = [0, 0]
            counts[label][state_idx] += 1

    total_issues = len(matched)
    summary = AnalysisSummary(
        total_issues=total_issues,
        open_issues=open_total,
        closed_issues=closed_total,
        open_pct=_calc_pct(open_total, total_issues),
        closed_pct=_calc_pct(closed_total, total_issues),
    )

    if target_labels:
        selected_labels = list(dict.fromkeys(target_labels))
    else:
        selected_labels = list(counts.keys())
        if exclude_filter_labels and inc:
            inc_set = set(inc)
            selected_labels = [lbl for lbl in selected_labels if lbl not in inc_set]

    label_stats: list[LabelStats] = []
    for label in selected_labels:
        open_cnt, closed_cnt = counts.get(label, [0, 0])
        lbl_total = open_cnt + closed_cnt
        label_stats.append(
            LabelStats(
                label=label,
                open=open_cnt,
                closed=closed_cnt,
                total=lbl_total,
                open_pct=_calc_pct(open_cnt, lbl_total),
                closed_pct=_calc_pct(closed_cnt, lbl_total),
                subset_pct=_calc_pct(lbl_total, total_issues),
            )
        )

    sorted_stats = sort_label_stats(label_stats, sort_by=sort_by, order=order)
    return AnalysisResult(
        repository=repository,
        include_labels=inc,
        exclude_labels=exc,
        summary=summary,
        labels=sorted_stats,
    )


def _format_header_lines(result: AnalysisResult) -> list[str]:
    inc_text = ", ".join(result.include_labels) if result.include_labels else "(all)"
    lines = [
        f"Repository: {result.repository}",
        f"Filter labels: {inc_text}",
    ]
    if result.exclude_labels:
        lines.append(f"Excluded labels: {', '.join(result.exclude_labels)}")
    s = result.summary
    lines.append(
        f"Matching issues: {s.total_issues} "
        f"(Open: {s.open_issues} [{s.open_pct:.1f}%], "
        f"Closed: {s.closed_issues} [{s.closed_pct:.1f}%])"
    )
    return lines


def format_result(result: AnalysisResult, output_format: str = "table") -> str:
    """Format an AnalysisResult in table, markdown, csv, or json format."""
    if output_format == "json":
        payload = {
            "repository": result.repository,
            "include_labels": result.include_labels,
            "exclude_labels": result.exclude_labels,
            "summary": asdict(result.summary),
            "labels": [asdict(row) for row in result.labels],
        }
        return json.dumps(payload, indent=2)

    if output_format == "csv":
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        writer.writerow(["label", "open", "closed", "total", "open_pct", "closed_pct", "subset_pct"])
        for row in result.labels:
            writer.writerow(
                [
                    row.label,
                    row.open,
                    row.closed,
                    row.total,
                    f"{row.open_pct:.2f}",
                    f"{row.closed_pct:.2f}",
                    f"{row.subset_pct:.2f}",
                ]
            )
        return buf.getvalue().rstrip("\n")

    if output_format == "markdown":
        lines = [f"- **{line.split(':', 1)[0]}**:{line.split(':', 1)[1]}" for line in _format_header_lines(result)]
        lines.append("")
        if not result.labels:
            lines.append("_No labels found for the matching issues._")
            return "\n".join(lines)
        lines.append("| Label | Open | Closed | Total | Open % | Closed % | Subset % |")
        lines.append("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in result.labels:
            lines.append(
                f"| `{row.label}` | {row.open} | {row.closed} | {row.total} | "
                f"{row.open_pct:.1f}% | {row.closed_pct:.1f}% | {row.subset_pct:.1f}% |"
            )
        return "\n".join(lines)

    if output_format == "table":
        lines = _format_header_lines(result)
        lines.append("")
        if not result.labels:
            lines.append("No labels found for the matching issues.")
            return "\n".join(lines)

        headers = ("Label", "Open", "Closed", "Total", "Open %", "Closed %", "Subset %")
        rows = [
            (
                row.label,
                str(row.open),
                str(row.closed),
                str(row.total),
                f"{row.open_pct:.1f}%",
                f"{row.closed_pct:.1f}%",
                f"{row.subset_pct:.1f}%",
            )
            for row in result.labels
        ]
        widths = [
            max(len(headers[i]), *(len(r[i]) for r in rows))
            for i in range(len(headers))
        ]
        header_line = "  ".join(
            headers[i].ljust(widths[i]) if i == 0 else headers[i].rjust(widths[i])
            for i in range(len(headers))
        )
        sep_line = "  ".join("-" * widths[i] for i in range(len(headers)))
        lines.append(header_line)
        lines.append(sep_line)
        for r in rows:
            lines.append(
                "  ".join(
                    r[i].ljust(widths[i]) if i == 0 else r[i].rjust(widths[i])
                    for i in range(len(headers))
                )
            )
        return "\n".join(lines)

    raise ValueError(f"Unsupported output format '{output_format}'. Expected one of {OUTPUT_FORMATS}.")


def parse_owner_and_repo(owner: str, repository: str) -> tuple[str, str]:
    """Allow `--repository owner/name` shorthand while keeping explicit `--owner`."""
    if "/" in repository:
        parts = repository.split("/", 1)
        if parts[0] and parts[1]:
            return parts[0], parts[1]
    return owner, repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze open and closed GitHub issues per label within an optionally "
            "label-filtered subset."
        )
    )
    parser.add_argument(
        "-o",
        "--owner",
        default=DEFAULT_OWNER,
        help=f"GitHub repository owner (default: {DEFAULT_OWNER})",
    )
    parser.add_argument(
        "-r",
        "--repository",
        "--repo",
        dest="repository",
        default=DEFAULT_REPO,
        help=f"GitHub repository name or owner/repo (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "-l",
        "--label",
        dest="include_labels",
        action="append",
        default=[],
        help="Filter issues to those having this label (repeatable for AND filtering).",
    )
    parser.add_argument(
        "-x",
        "--exclude-label",
        dest="exclude_labels",
        action="append",
        default=[],
        help="Exclude issues having this label (repeatable).",
    )
    parser.add_argument(
        "-t",
        "--target-label",
        dest="target_labels",
        action="append",
        default=[],
        help="Report statistics only for these specific labels (repeatable).",
    )
    parser.add_argument(
        "--exclude-filter-labels",
        action="store_true",
        help="Omit the --label filter labels from the per-label output table.",
    )
    parser.add_argument(
        "--include-prs",
        action="store_true",
        help="Include pull requests in addition to issues.",
    )
    parser.add_argument(
        "--sort",
        choices=SORT_KEYS,
        default="total",
        help="Sort output rows by field (default: total).",
    )
    parser.add_argument(
        "--order",
        choices=("asc", "desc"),
        default=None,
        help="Sort order (default: asc for name, desc for numeric fields).",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        choices=OUTPUT_FORMATS,
        default="table",
        help="Output format (default: table).",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="GitHub API token (defaults to GITHUB_TOKEN, GH_TOKEN, or `gh auth token`).",
    )
    parser.add_argument(
        "--input-json",
        default=None,
        help="Read issues from a local JSON file instead of querying the GitHub API.",
    )
    parser.add_argument(
        "--save-json",
        default=None,
        help="Save fetched raw issues JSON to a local file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    owner, repo = parse_owner_and_repo(args.owner, args.repository)
    repo_slug = f"{owner}/{repo}"

    if args.input_json:
        with open(args.input_json, "r", encoding="utf-8") as f:
            issues = json.load(f)
        if not isinstance(issues, list):
            print("Error: --input-json must contain a JSON array of issues.", file=sys.stderr)
            return 1
    else:
        token = resolve_github_token(args.token)
        try:
            issues = fetch_issues(
                owner=owner,
                repo=repo,
                include_labels=args.include_labels,
                token=token,
            )
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        if args.save_json:
            with open(args.save_json, "w", encoding="utf-8") as f:
                json.dump(issues, f, indent=2)

    result = analyze_issues(
        issues=issues,
        repository=repo_slug,
        include_labels=args.include_labels,
        exclude_labels=args.exclude_labels,
        target_labels=args.target_labels,
        exclude_filter_labels=args.exclude_filter_labels,
        include_prs=args.include_prs,
        sort_by=args.sort,
        order=args.order,
    )
    print(format_result(result, output_format=args.output_format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
