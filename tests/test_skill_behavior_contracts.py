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
REQUIREMENTS_COPIES = (
    PLUGIN_SKILLS / "sdlc-requirements-workflow" / "SKILL.md",
    CATALOG
    / "sdlc-manager"
    / "skills"
    / "sdlc-requirements-workflow"
    / "SKILL.md",
)
SDLC_ROUTER_COPIES = (
    PLUGIN_SKILLS / "sdlc-router" / "SKILL.md",
    CATALOG / "sdlc-manager" / "skills" / "sdlc-router" / "SKILL.md",
)
SOLUTION_SPEC_COPIES = (
    PLUGIN_SKILLS / "sdlc-solution-spec-workflow" / "SKILL.md",
    CATALOG
    / "sdlc-manager"
    / "skills"
    / "sdlc-solution-spec-workflow"
    / "SKILL.md",
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

    def test_goal_run_explicit_tracking_and_phase_boundary_updates(self) -> None:
        for path in GOAL_RUN_COPIES:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                compact = normalized(text)
                self.assertIn(
                    "Use only when the user explicitly invokes this skill", compact
                )
                self.assertIn(
                    "Do not use this workflow for ordinary work that can finish "
                    "in the current turn",
                    compact,
                )
                self.assertNotIn("legacy-unresolved", text)
                self.assertNotIn("`Anchor`", text)

                workflow = normalized(
                    section(text, "## Workflow", "## Human and External Boundaries")
                )
                self.assert_markers_in_order(
                    workflow,
                    (
                        "Confirm that the user explicitly requested persistent "
                        "goal tracking",
                        "Read the source goal and existing tracker files",
                        "Create tracker files only when they are missing",
                        "Extract actionable tasks",
                        "Continue the current safe task",
                        "Update tracker files only at a meaningful phase "
                        "boundary",
                        "Before stopping, ensure completed work has evidence",
                    ),
                )
                self.assertIn(
                    "Do not interrupt implementation after every small unit", workflow
                )

                stop_conditions = normalized(section(text, "## Stop Conditions"))
                self.assertIn("no actionable automatic task remains", stop_conditions)
                self.assertIn("requires a user decision", stop_conditions)
                self.assertIn("verification has a concrete blocker", stop_conditions)
                self.assertIn(
                    "Do not treat a difficult, slow, or incomplete task as blocked",
                    stop_conditions,
                )

    def test_router_recommends_one_path_and_stops(self) -> None:
        text = ROUTER.read_text(encoding="utf-8")
        compact = normalized(text)
        route_choices = normalized(
            section(text, "## Route Choices", "## Capability Map")
        )
        self.assert_markers_in_order(
            route_choices,
            (
                "Direct execution",
                "One bounded skill",
                "One explicit control workflow",
            ),
        )
        self.assertIn(
            "Direct execution is a successful routing result", route_choices
        )
        self.assertIn("Do not recommend a skill only because one exists", route_choices)

        decision_rules = normalized(
            section(text, "## Decision Rules", "## Output")
        )
        self.assert_markers_in_order(
            decision_rules,
            (
                "Prefer direct work",
                "Recommend a bounded skill only when",
                "Do not infer that a midstream project needs",
                "show its explicit `$skill` name and wait",
                "Ask at most one question",
            ),
        )

        boundaries = normalized(section(text, "## Boundaries"))
        self.assertIn("Do not call another skill or imitate its workflow", boundaries)
        self.assertIn("Do not create or edit files", boundaries)
        self.assertIn("Do not run commands, spawn agents", boundaries)
        self.assertIn(
            "Do not turn ambiguity alone into an unknowns, grilling, or "
            "readiness process",
            boundaries,
        )
        self.assertIn("Do not return several equally weighted routes", boundaries)
        self.assertIn("Recommend the smallest useful path and stop", compact)
        self.assertNotIn("continue with the selected skill", compact.lower())

    def test_sdlc_router_is_explicit_read_only_and_recommend_only(self) -> None:
        for path in SDLC_ROUTER_COPIES:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                compact = normalized(text)
                self.assertIn(
                    "Use only when the user explicitly invokes this skill", compact
                )
                self.assertIn("This skill only recommends a route", compact)
                self.assertIn(
                    "It does not write or update `local/sdlc`", compact
                )

                next_skill_routing = normalized(
                    section(text, "## Next Skill Routing", "## Output")
                )
                self.assertIn(
                    "Recommend the smallest next step. Do not invoke it",
                    next_skill_routing,
                )

                boundaries = normalized(section(text, "## Boundaries"))
                self.assertIn("Do not create or edit files", boundaries)
                self.assertIn(
                    "Do not invoke, imitate, or begin the recommended skill",
                    boundaries,
                )

    def test_coordinators_recommend_instead_of_auto_invoking_controls(self) -> None:
        for path in REQUIREMENTS_COPIES:
            with self.subTest(path=path):
                compact = normalized(path.read_text(encoding="utf-8"))
                self.assertIn(
                    "recommend an explicit `core-grilling` run and stop", compact
                )
                self.assertIn(
                    "Do not invoke `sdlc-router` from this workflow", compact
                )
                self.assertIn(
                    "Optional next-skill recommendations; do not invoke them "
                    "automatically",
                    compact,
                )

        for path in SOLUTION_SPEC_COPIES:
            with self.subTest(path=path):
                compact = normalized(path.read_text(encoding="utf-8"))
                for skill_name in (
                    "sdlc-hld-workflow",
                    "sdlc-architecture-decision-record",
                    "sdlc-lld-workflow",
                    "sdlc-dev-handoff-planning",
                ):
                    self.assertIn(f"recommend `{skill_name}`", compact.lower())
                self.assertIn(
                    "Recommend at most one downstream skill", compact
                )
                self.assertGreaterEqual(compact.lower().count("do not invoke"), 5)

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
