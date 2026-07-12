from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SKILLS = REPO_ROOT / "plugins" / "codex-next" / "skills"
CATALOG = REPO_ROOT / "examples" / "catalog"

READINESS_COPIES = (
    PLUGIN_SKILLS / "sdlc-readiness-review" / "SKILL.md",
    CATALOG / "sdlc-manager" / "skills" / "sdlc-readiness-review" / "SKILL.md",
)
GOAL_RUN_COPIES = (
    PLUGIN_SKILLS / "core-goal-run" / "SKILL.md",
    CATALOG / "common" / "skills" / "core-goal-run" / "SKILL.md",
)
PR_REVIEW_COPIES = (
    PLUGIN_SKILLS / "dev-pr-review" / "SKILL.md",
    CATALOG / "dev" / "skills" / "dev-pr-review" / "SKILL.md",
)
ROUTER = PLUGIN_SKILLS / "core-router" / "SKILL.md"


def normalized(text: str) -> str:
    return " ".join(text.split())


def section(text: str, heading: str, next_heading: str | None = None) -> str:
    start = text.index(heading)
    if next_heading is None:
        return text[start:]
    end = text.index(next_heading, start + len(heading))
    return text[start:end]


class SkillBehaviorContractsTest(unittest.TestCase):
    def assert_markers_in_order(self, text: str, markers: tuple[str, ...]) -> None:
        position = -1
        for marker in markers:
            next_position = text.find(marker, position + 1)
            self.assertNotEqual(next_position, -1, f"missing behavior marker: {marker}")
            self.assertGreater(next_position, position, f"out-of-order marker: {marker}")
            position = next_position

    def test_readiness_authority_necessity_and_verdict_order(self) -> None:
        expected_steps = (
            {"identify", "review", "subject"},
            {"source", "authority"},
            {"necessity", "smallest", "sufficient"},
            {"scope", "non-scope"},
            {"software-facing", "completeness"},
            {"acceptance", "validation"},
            {"traceability"},
            {"readiness", "verdict"},
            {"next", "action"},
        )
        verdict_order = (
            "change-control-needed",
            "not-needed",
            "revise",
            "repo-onboarding-first",
            "reduce-scope",
            "ready-for-dev",
            "ready-for-direct-dev",
        )

        for path in READINESS_COPIES:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                headings = re.findall(r"^###\s+(\d+)\.\s+(.+)$", text, re.MULTILINE)
                self.assertEqual(
                    [int(number) for number, _ in headings], list(range(1, 10))
                )
                for (_, title), required_words in zip(
                    headings, expected_steps, strict=True
                ):
                    self.assertTrue(required_words <= set(title.lower().split()))

                precedence = re.search(
                    r"When more than one verdict candidate applies.*?Use `blocked` only",
                    text,
                    re.DOTALL,
                )
                self.assertIsNotNone(precedence)
                assert precedence is not None
                actual_order = tuple(
                    item
                    for item in re.findall(r"`([^`]+)`", precedence.group(0))
                    if item in verdict_order
                )
                self.assertEqual(actual_order, verdict_order)

                compact = normalized(text)
                self.assertIn("Missing justification is `revise`, not `not-needed`", compact)
                self.assertIn(
                    "smaller alternative stays within the controlling baseline", compact
                )
                self.assertIn("otherwise use `change-control-needed`", compact)
                self.assertIn("never bypass source authority", compact)

    def test_goal_run_legacy_anchor_transitions_and_halting(self) -> None:
        migration_markers = (
            "For a task that has not started",
            "For an existing `DONE`, `BLOCKED`, `HUMAN_PENDING`, or `SKIPPED_HUMAN` row",
            "Do not treat a generic resume request",
            "If a legacy task is already `DOING` or `VERIFYING`",
            "Before writing a terminal `DONE` or `BLOCKED` status",
            "After that unit",
        )

        for path in GOAL_RUN_COPIES:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                compact = normalized(text)
                self.assertIn("Neither value is a confirmed anchor", compact)

                migration = normalized(
                    section(
                        text,
                        "When an existing `goal-tasks.md` has no `Anchor` column:",
                        "Do not put long command output",
                    )
                )
                self.assert_markers_in_order(migration, migration_markers)
                self.assertIn("write `legacy-unresolved`, preserve its status", migration)
                self.assertIn("record the provenance gap", migration)
                self.assertIn("Confirm an anchor before reopening or resuming", migration)
                self.assertIn("takes precedence over the normal halting condition", migration)
                self.assertIn(
                    "replace `pending` with any task-specific anchor established",
                    migration,
                )
                self.assertIn("set `Anchor=legacy-unresolved`", migration)
                self.assertIn("return it to `TODO` with `Anchor=pending`", migration)
                self.assertIn("mark it `BLOCKED` and record the blocker", migration)

                stop_conditions = normalized(section(text, "## Stop Conditions"))
                for status in ("`TODO`", "`DOING`", "`VERIFYING`"):
                    self.assertIn(status, stop_conditions)
                self.assertIn("confirmed task-specific `Anchor`", stop_conditions)
                self.assertIn("finishing that allowed unit", stop_conditions)
                self.assertIn("do not invent work", stop_conditions)
                self.assertIn("record a concrete blocker", stop_conditions)
                self.assertIn("Only unanchored suggestions remain", stop_conditions)
                self.assertIn("do not promote them into tasks", stop_conditions)

    def test_router_ambiguity_specificity_and_coordinator_precedence(self) -> None:
        text = ROUTER.read_text(encoding="utf-8")
        workflow = normalized(section(text, "## Workflow", "## Route Table"))
        self.assert_markers_in_order(
            workflow,
            (
                "If the request is ambiguous",
                "A clear user request tied to an explicit outcome is an external anchor",
                "After the problem and outcome are clear",
                "If the clarified, anchored request only needs lane",
                "When several routes match",
                "If multiple equally specific SDLC artifact intents remain",
                "Otherwise, if the clarified request is SDLC/ADS",
                "If the request is clear, anchored, and local",
            ),
        )
        self.assertIn(
            "Ambiguity takes precedence over SDLC/ADS lane classification", workflow
        )
        self.assertIn("Do not choose one leaf workflow arbitrarily", workflow)

        route_table = section(
            text, "## Route Table", "## Manual or Expensive Helpers"
        )
        rows = [
            tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
            for line in route_table.splitlines()
            if line.lstrip().startswith("|") and "---" not in line
        ]

        def assert_route(intent_fragment: str, skill_name: str) -> None:
            matching = [row for row in rows if intent_fragment in row[0]]
            self.assertEqual(len(matching), 1, intent_fragment)
            self.assertIn(skill_name, matching[0][1])

        assert_route("Ambiguous, underspecified", "core-explore-unknowns")
        assert_route("no task-specific external anchor", "sdlc-readiness-review")
        assert_route("Need only lane", "sdlc-router")
        assert_route(
            "Solution/spec package coordination", "sdlc-solution-spec-workflow"
        )
        assert_route("SDLC/ADS work", "sdlc-manager")

        table_rules = normalized(route_table.split("| User intent", 1)[0])
        self.assertIn("choose the most specific intent", table_rules)
        self.assertIn("fallbacks, not overrides", table_rules)
        self.assertIn("multiple equally specific SDLC artifact rows", table_rules)

        boundaries = normalized(section(text, "## Boundaries"))
        self.assertIn("Do not route ambiguous work directly", boundaries)
        self.assertIn("do not manufacture process overhead", boundaries)
        self.assertIn("Do not arbitrarily select one leaf", boundaries)

    def test_pr_review_minimality_respects_required_artifacts(self) -> None:
        for path in PR_REVIEW_COPIES:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                minimality = normalized(
                    section(text, "8. Minimality", "## Output")
                )
                for required in (
                    "repository-mandated mirrors",
                    "generated artifacts",
                    "tests",
                    "migrations",
                    "version updates",
                    "compatibility docs",
                ):
                    self.assertIn(required, minimality)
                self.assertIn("constraints rather than overhead", minimality)
                self.assertIn(
                    "smaller alternative still satisfies the repository contract",
                    minimality,
                )
                self.assertIn("concrete smaller alternative for each finding", minimality)

                output = normalized(section(text, "## Output", "## Do not"))
                self.assert_markers_in_order(
                    output,
                    (
                        "Simplification findings",
                        "Test gaps",
                        "Contract or compatibility risks",
                        "Verdict",
                    ),
                )

                do_not = normalized(section(text, "## Do not"))
                self.assertIn(
                    "concrete smaller alternative within the current scope", do_not
                )
                self.assertIn("do not use them to propose redesigns", do_not)


if __name__ == "__main__":
    unittest.main()
