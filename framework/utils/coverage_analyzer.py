"""
Coverage Analyzer — Demo_QA
==============================
Maps manual test cases from the Test Library to automated check scripts
and identifies coverage gaps. Produces a structured coverage report with
mappings, gaps, and statistics.

Usage:
    from framework.utils.coverage_analyzer import CoverageAnalyzer

    analyzer = CoverageAnalyzer(
        test_library_path="test_library",
        tests_path="tests/check_scripts"
    )
    report = analyzer.analyze()
    print(f"Coverage: {report.coverage_rate:.1f}%")
"""

import os
import re
import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from framework.utils.logger_factory import get_logger

log = get_logger(__name__)


# =============================================================================
# DATA MODELS
# =============================================================================


@dataclass
class CoverageMapping:
    """Maps a manual test case to its corresponding automated check script."""

    test_case_id: str
    title: str
    check_script: Optional[str]
    status: str  # "automated", "planned", "manual-only"
    justification: str  # Why gap exists (empty if automated)
    automation_dependency: str  # A, B, C, or D


@dataclass
class CoverageReport:
    """Complete coverage analysis report."""

    mappings: List[CoverageMapping] = field(default_factory=list)
    gaps: List[CoverageMapping] = field(default_factory=list)
    statistics: dict = field(default_factory=dict)


@dataclass
class ParsedTestCase:
    """Parsed representation of a manual test case from markdown."""

    id: str
    title: str
    priority: str
    automation_status: str
    automation_dependency: str
    file_path: str


# =============================================================================
# COVERAGE ANALYZER
# =============================================================================


class CoverageAnalyzer:
    """Maps manual test cases to automated tests and identifies gaps.

    Scans the test_library/ directory for markdown test case files,
    discovers check_T{id}_* functions in the check_scripts/ directory,
    and produces a coverage report showing which test cases are automated,
    planned, or manual-only.

    Args:
        test_library_path: Path to test_library/ directory.
        tests_path: Path to tests/check_scripts/ directory.
    """

    # Pattern to extract numeric ID from test case IDs like TC_LOGIN_001
    _TC_ID_PATTERN = re.compile(r"TC_[A-Z]+_(\d+)")

    # Pattern to extract numeric ID from check script function names
    _CHECK_SCRIPT_PATTERN = re.compile(r"check_T(\d+)_\w+")

    def __init__(self, test_library_path: str, tests_path: str):
        self.test_library_path = Path(test_library_path)
        self.tests_path = Path(tests_path)
        log.info(
            "CoverageAnalyzer initialized — library: %s, scripts: %s",
            self.test_library_path,
            self.tests_path,
        )

    def analyze(self) -> CoverageReport:
        """Produce coverage mapping between manual and automated tests.

        Parses all test case markdown files, discovers all check script
        functions, matches them by ID, and computes coverage statistics.

        Returns:
            CoverageReport with mappings, gaps, and statistics.
        """
        log.info("Starting coverage analysis...")

        # Step 1: Parse all manual test cases
        test_cases = self._parse_test_cases()
        log.info("Parsed %d manual test cases", len(test_cases))

        # Step 2: Discover all check script functions
        check_scripts = self._discover_check_scripts()
        log.info("Discovered %d check script functions", len(check_scripts))

        # Step 3: Match cases to scripts
        mappings = self._match_cases_to_scripts(test_cases, check_scripts)

        # Step 4: Identify gaps (non-automated cases)
        gaps = [m for m in mappings if m.status != "automated"]

        # Step 5: Compute statistics
        total = len(mappings)
        automated = sum(1 for m in mappings if m.status == "automated")
        planned = sum(1 for m in mappings if m.status == "planned")
        manual_only = sum(1 for m in mappings if m.status == "manual-only")

        # Count by automation dependency category
        dependency_counts = {}
        for m in mappings:
            cat = m.automation_dependency
            dependency_counts[cat] = dependency_counts.get(cat, 0) + 1

        statistics = {
            "total": total,
            "automated": automated,
            "planned": planned,
            "manual_only": manual_only,
            "coverage_rate": (automated / total * 100) if total > 0 else 0.0,
            "dependency_categories": dependency_counts,
        }

        report = CoverageReport(
            mappings=mappings,
            gaps=gaps,
            statistics=statistics,
        )

        log.info(
            "Coverage analysis complete — %d/%d automated (%.1f%%)",
            automated,
            total,
            statistics["coverage_rate"],
        )

        return report

    def _parse_test_cases(self) -> List[ParsedTestCase]:
        """Parse markdown test case files from test_library/.

        Scans all subdirectories (login/, cart/, catalog/, checkout/) for
        markdown files and extracts test case metadata from each.

        Returns:
            List of ParsedTestCase objects with extracted metadata.
        """
        test_cases = []

        if not self.test_library_path.exists():
            log.warning("Test library path does not exist: %s", self.test_library_path)
            return test_cases

        # Scan all subdirectories for .md files (skip template and coverage_analysis)
        for md_file in sorted(self.test_library_path.rglob("*.md")):
            # Skip non-test-case files
            if md_file.name in ("template.md", "coverage_analysis.md"):
                continue

            # Only process files that look like test cases (TC_*.md)
            if not md_file.stem.startswith("TC_"):
                continue

            parsed = self._parse_single_test_case(md_file)
            if parsed:
                test_cases.append(parsed)
            else:
                log.warning("Could not parse test case from: %s", md_file)

        return test_cases

    def _parse_single_test_case(self, file_path: Path) -> Optional[ParsedTestCase]:
        """Parse a single markdown test case file.

        Handles two formats:
        1. Section-based (## Test Case ID, ## Title, etc.)
        2. Table-based (## Test Case Information with | Field | Value | table)

        Args:
            file_path: Path to the markdown file.

        Returns:
            ParsedTestCase if successfully parsed, None otherwise.
        """
        try:
            content = file_path.read_text(encoding="utf-8")
        except (IOError, OSError) as e:
            log.error("Cannot read file %s: %s", file_path, e)
            return None

        tc_id = None
        title = None
        priority = ""
        automation_status = ""
        automation_dependency = ""

        # Try table-based format first (## Test Case Information with table)
        table_match = re.search(
            r"##\s+Test Case Information\s*\n\s*\|.*\|.*\|\s*\n\s*\|[-\s|]+\|\s*\n((?:\s*\|.*\|.*\n)+)",
            content,
        )
        if table_match:
            table_rows = table_match.group(1)
            for row in table_rows.strip().split("\n"):
                cells = [c.strip() for c in row.split("|") if c.strip()]
                if len(cells) >= 2:
                    field_name = re.sub(r"\*+", "", cells[0]).strip().lower()
                    value = cells[1].strip()

                    if field_name == "id":
                        tc_id = value
                    elif field_name == "title":
                        title = value
                    elif field_name == "priority":
                        priority = value
                    elif field_name == "automation status":
                        automation_status = value
                    elif field_name == "automation dependency":
                        automation_dependency = value

        # Try section-based format (## Test Case ID, ## Title, etc.)
        if not tc_id:
            id_match = re.search(
                r"##\s+Test Case ID\s*\n\s*(.+)", content
            )
            if id_match:
                tc_id = id_match.group(1).strip()

        if not title:
            title_match = re.search(r"##\s+Title\s*\n\s*(.+)", content)
            if title_match:
                title = title_match.group(1).strip()

        if not priority:
            priority_match = re.search(r"##\s+Priority\s*\n\s*(.+)", content)
            if priority_match:
                priority = priority_match.group(1).strip()

        if not automation_status:
            status_match = re.search(
                r"##\s+Automation Status\s*\n\s*(.+)", content
            )
            if status_match:
                automation_status = status_match.group(1).strip()

        if not automation_dependency:
            dep_match = re.search(
                r"##\s+Automation Dependency(?:\s+Category)?\s*\n\s*(.+)", content
            )
            if dep_match:
                automation_dependency = dep_match.group(1).strip()

        # Fallback: extract ID from filename if not found in content
        if not tc_id:
            tc_id = file_path.stem

        # Fallback: extract title from first heading
        if not title:
            heading_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
            if heading_match:
                # Strip common prefixes like "Test Case: " or "TC_XXX_NNN — "
                raw_title = heading_match.group(1).strip()
                raw_title = re.sub(r"^Test Case:\s*", "", raw_title)
                raw_title = re.sub(r"^TC_\w+\s*[—–-]\s*", "", raw_title)
                title = raw_title if raw_title else file_path.stem

        if not tc_id:
            return None

        return ParsedTestCase(
            id=tc_id,
            title=title or tc_id,
            priority=priority,
            automation_status=automation_status.lower() if automation_status else "",
            automation_dependency=automation_dependency.upper() if automation_dependency else "",
            file_path=str(file_path),
        )

    def _discover_check_scripts(self) -> List[str]:
        """Discover automated test functions matching check_T{id}_* pattern.

        Scans Python files in the tests_path directory for function definitions
        that follow the check_T{number}_{description} naming convention.

        Returns:
            List of function names (e.g., ["check_T001_login_valid_credentials"]).
        """
        scripts = []

        if not self.tests_path.exists():
            log.warning("Check scripts path does not exist: %s", self.tests_path)
            return scripts

        for py_file in sorted(self.tests_path.glob("check_*.py")):
            if py_file.name == "__init__.py":
                continue

            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if self._CHECK_SCRIPT_PATTERN.match(node.name):
                            scripts.append(node.name)

            except (SyntaxError, IOError, OSError) as e:
                log.warning("Cannot parse check script %s: %s", py_file, e)

        return scripts

    def _match_cases_to_scripts(
        self, cases: List[ParsedTestCase], scripts: List[str]
    ) -> List[CoverageMapping]:
        """Match test case IDs to corresponding check script functions.

        Matching strategy:
        1. Extract numeric ID from check script names (check_T{id}_desc → id)
        2. Extract numeric ID from test case IDs (TC_FEATURE_NNN → NNN)
        3. If a numeric ID uniquely identifies a test case, match directly
        4. If multiple test cases share the same numeric suffix, use keyword
           matching between the test case title/feature and the script description

        Args:
            cases: List of parsed manual test cases.
            scripts: List of check script function names.

        Returns:
            List of CoverageMapping objects showing the match status.
        """
        # Build a lookup from numeric ID to script name(s)
        script_map = {}
        for script_name in scripts:
            match = self._CHECK_SCRIPT_PATTERN.match(script_name)
            if match:
                numeric_id = int(match.group(1))
                script_map[numeric_id] = script_name

        # Group test cases by their numeric suffix to detect collisions
        cases_by_numeric_id = {}
        for case in cases:
            id_match = self._TC_ID_PATTERN.search(case.id)
            if id_match:
                numeric_id = int(id_match.group(1))
                if numeric_id not in cases_by_numeric_id:
                    cases_by_numeric_id[numeric_id] = []
                cases_by_numeric_id[numeric_id].append(case)

        # Check if numeric IDs are unique across all test cases
        has_collisions = any(
            len(group) > 1 for group in cases_by_numeric_id.values()
        )

        # Track which scripts have been claimed (avoid duplicate mappings)
        claimed_scripts = set()

        mappings = []
        for case in cases:
            # Extract numeric ID from test case ID
            id_match = self._TC_ID_PATTERN.search(case.id)
            if not id_match:
                log.warning(
                    "Cannot extract numeric ID from test case: %s", case.id
                )
                mappings.append(
                    CoverageMapping(
                        test_case_id=case.id,
                        title=case.title,
                        check_script=None,
                        status=case.automation_status or "manual-only",
                        justification="Cannot extract numeric ID for matching",
                        automation_dependency=case.automation_dependency,
                    )
                )
                continue

            numeric_id = int(id_match.group(1))
            matched_script = None

            if not has_collisions:
                # Simple case: numeric IDs are unique, direct match
                matched_script = script_map.get(numeric_id)
            else:
                # Collision case: multiple test cases share numeric suffix
                # Use keyword matching between test case and script descriptions
                matched_script = self._find_best_script_match(
                    case, scripts, claimed_scripts
                )

            if matched_script and matched_script not in claimed_scripts:
                claimed_scripts.add(matched_script)
                mappings.append(
                    CoverageMapping(
                        test_case_id=case.id,
                        title=case.title,
                        check_script=matched_script,
                        status="automated",
                        justification="",
                        automation_dependency=case.automation_dependency,
                    )
                )
            else:
                # No matching script found — determine gap status
                # Use the test case's stated status if available (planned vs manual-only)
                # but never mark as "automated" without an actual script
                stated_status = case.automation_status if case.automation_status else ""
                if stated_status == "automated":
                    # Test case claims automated but no script found — mark as planned
                    status = "planned"
                elif stated_status in ("planned", "manual-only"):
                    status = stated_status
                else:
                    status = "manual-only"

                justification = self._generate_gap_justification(case)
                mappings.append(
                    CoverageMapping(
                        test_case_id=case.id,
                        title=case.title,
                        check_script=None,
                        status=status,
                        justification=justification,
                        automation_dependency=case.automation_dependency,
                    )
                )

        return mappings

    def _find_best_script_match(
        self,
        case: ParsedTestCase,
        scripts: List[str],
        claimed: set,
    ) -> Optional[str]:
        """Find the best matching check script for a test case using keywords.

        Extracts keywords from the test case title and feature group, then
        scores each unclaimed script by keyword overlap.

        Args:
            case: The test case to match.
            scripts: All available check script names.
            claimed: Set of already-claimed script names.

        Returns:
            Best matching script name, or None if no good match found.
        """
        # Extract feature from test case ID (e.g., TC_LOGIN_001 → login)
        feature_match = re.match(r"TC_([A-Z]+)_\d+", case.id)
        feature = feature_match.group(1).lower() if feature_match else ""

        # Build keyword set from title and feature
        title_words = set(
            re.findall(r"[a-z]+", case.title.lower())
        )
        title_words.add(feature)

        # Common keyword mappings for better matching
        keyword_aliases = {
            "login": {"login", "credentials", "authentication"},
            "cart": {"cart", "add", "remove", "shopping"},
            "catalog": {"catalog", "product", "browse", "sort", "detail"},
            "checkout": {"checkout", "complete", "cancel", "shipping"},
        }

        # Expand keywords with aliases
        expanded_keywords = set(title_words)
        for alias_key, alias_set in keyword_aliases.items():
            if alias_key in title_words or alias_key == feature:
                expanded_keywords.update(alias_set)

        best_script = None
        best_score = 0

        for script in scripts:
            if script in claimed:
                continue

            # Extract description words from script name
            # check_T001_login_valid_credentials → {login, valid, credentials}
            desc_part = re.sub(r"^check_T\d+_", "", script)
            script_words = set(desc_part.split("_"))

            # Score by keyword overlap
            score = len(expanded_keywords & script_words)

            if score > best_score:
                best_score = score
                best_script = script

        # Require minimum score to avoid false matches
        return best_script if best_score >= 1 else None

    def _generate_gap_justification(self, case: ParsedTestCase) -> str:
        """Generate a justification string for unautomated test cases.

        Args:
            case: The parsed test case without a matching script.

        Returns:
            A justification string based on the automation dependency category.
        """
        category = case.automation_dependency

        justifications = {
            "A": f"Category A (app-only); candidate for automation in next sprint",
            "B": f"Category B (external validation required); needs additional tooling",
            "C": f"Category C (hardware required); not feasible in emulator-only setup",
            "D": f"Category D (precondition-dependent); requires specific state setup",
        }

        return justifications.get(
            category,
            f"Automation dependency category not specified",
        )
