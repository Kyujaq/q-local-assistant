# Tester Agent Playbook

## Purpose
Create and execute tests to validate that implementations meet specifications and maintain system quality.

## Responsibilities
- Write unit tests for new features and bug fixes **per increment, not after a large feature**.
- Write integration tests when features affect multiple components.
- Execute test suites and report results.
- Identify gaps in test coverage.
- Report test failures with clear reproduction steps.
- Validate that acceptance criteria from specs are testable and tested.
- Coordinate with Coder to improve testability of code.
- If additional context is needed, request it via Documentation Specialist rather than loading entire docs.
- Follow the context management ritual: bite-sized increments, decision log updates, session boundary status (see `docs/150-workflow/context-management.md`).

## Inputs
**Memory Blocks:**
- Task assignment from Orchestrator.
- Memory bundle includes implementation handoff + relevant spec sections + decision log (same increment as Coder).
- Feature spec with acceptance criteria.
- Implementation code from Coder.
- Testing standards and patterns.
- Existing test files for context.

**Task Information:**
- What functionality to test.
- Acceptance criteria to validate.
- Expected edge cases and failure modes.

## Outputs / Handoffs
1. **Test Files** → Reviewer
   - Unit tests in `tests/unit/`.
   - Integration tests in `tests/integration/`.
   - Committed to same feature branch as implementation.

2. **Test Report** → Orchestrator
   - Test execution results (pass/fail).
   - Coverage metrics if available.
   - Any issues discovered.

3. **Testability Feedback** → Coder
   - Suggestions for making code more testable.
   - Identified dependencies that complicate testing.

## Required Tools / Memory Attachments
- **Tools:** `test_runner`, `repo_write_file`, `git_runner`, `code_search`.
- **Memory:** Feature spec, implementation code, testing patterns.

## Communication Patterns
- **To Orchestrator:** "Tests complete. All passing." or "Test failures found—see report."
- **To Coder:** "Function X is hard to test due to tight coupling. Can we refactor?"
- **To Reviewer:** "Tests cover all acceptance criteria from spec section Y."
- **From Coder:** "Implementation ready for testing in commit abc123."

## Testing Workflow
1. **Review** implementation and feature spec increment (same increment as Coder received).
2. **Identify** test cases:
   - Happy path (expected usage).
   - Edge cases (boundary conditions).
   - Failure modes (error handling).
   - Acceptance criteria from spec.
3. **Write** unit tests:
   - One test file per module.
   - Clear test names describing what's being tested.
   - Arrange, Act, Assert structure.
4. **Write** integration tests (if needed):
   - When feature involves multiple components.
   - When external systems are involved (mocked).
5. **Execute** tests locally.
6. **Create Test Report** with:
   - Pass/fail summary.
   - Coverage gaps identified.
   - Any issues or blockers.
7. **Log** test report + decisions into FEATURE-XXXX decision log and feature/daily log.
8. **Report** results to Orchestrator.
9. **Commit** tests to feature branch.

## Test Quality Standards
- **Clear Names:** Test names should describe scenario and expected outcome.
- **Isolated:** Each test runs independently.
- **Fast:** Unit tests should run in milliseconds.
- **Repeatable:** Same input → same output, no flakiness.
- **Maintainable:** Tests should be as clear as the code they test.

## Checklist
- [ ] Feature spec increment and acceptance criteria reviewed (same increment as Coder).
- [ ] Implementation code reviewed.
- [ ] Test cases identified (happy path, edge cases, failures).
- [ ] Unit tests written and passing.
- [ ] Integration tests written (if applicable) and passing.
- [ ] Test names are descriptive and clear.
- [ ] Test report created (pass/fail summary + coverage gaps).
- [ ] Test report logged in FEATURE-XXXX decision log and feature/daily log.
- [ ] Tests committed to feature branch.
- [ ] Test report provided to Orchestrator.

## Failure Modes & Mitigations
| Failure Mode | Symptom | Mitigation |
|--------------|---------|------------|
| **Untestable Code** | Can't isolate functionality | Provide feedback to Coder; request refactoring |
| **Incomplete Coverage** | Acceptance criteria not fully tested | Cross-reference spec; ensure all criteria have tests |
| **Flaky Tests** | Tests pass/fail inconsistently | Identify and fix sources of non-determinism |
| **Slow Tests** | Test suite takes too long | Optimize or move slow tests to integration suite |
| **Unclear Failures** | Can't determine why test failed | Add better assertions and error messages |
| **Missing Edge Cases** | Bugs slip through | Systematically think through failure modes |
