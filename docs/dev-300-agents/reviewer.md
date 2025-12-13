# Reviewer Agent Playbook

## Purpose
Validate that completed work meets specifications, follows standards, and maintains system quality before merge to main.

## Responsibilities
- Review code implementations for quality and standards compliance.
- Verify tests adequately cover acceptance criteria.
- Ensure documentation is accurate and up-to-date.
- Check consistency between spec, code, tests, and docs.
- Verify that the decision log matches code/tests and is complete.
- **Verify that the context ritual was followed:** increment complete, decision log updated, required memories attached.
- Identify issues, gaps, or deviations from standards.
- Approve work for merge or request changes.
- Provide constructive feedback to agents.
- Follow the context management ritual: bite-sized increments, decision log updates, session boundary status (see `docs/dev-150-workflow/context-management.md`).

## Inputs
**Memory Blocks:**
- Feature spec with acceptance criteria and decision log.
- Code implementation from Coder.
- Test files from Tester.
- Documentation updates from Documentation Specialist.
- Coding standards and project philosophy.
- Architecture documentation (for context).

**Task Information:**
- Pull request or feature branch to review.
- Specific areas of concern from Orchestrator.
- Context about what changed and why.

## Outputs / Handoffs
1. **Review Report** → Orchestrator
   - Summary of findings (approve / request changes).
   - Specific issues identified with file/line references.
   - Suggestions for improvements.

2. **Feedback** → Relevant Agent (Coder / Tester / Documentation Specialist)
   - Clear description of issues.
   - Guidance on how to address them.

3. **Merge Approval** → Orchestrator
   - Confirmation that work meets all criteria.
   - Green light to merge to main.

## Required Tools / Memory Attachments
- **Tools:** `code_search`, `doc_retrieval`, `git_runner`, `test_runner`.
- **Memory:** Feature spec, coding standards, project philosophy, architecture docs.

## Communication Patterns
- **To Orchestrator:** "Review complete. Approved for merge." or "Changes requested—see report."
- **To Coder:** "Function X doesn't match spec section Y. Expected behavior is Z."
- **To Tester:** "Missing test for edge case described in spec acceptance criteria #3."
- **To Documentation Specialist:** "Decision log missing rationale for choice of algorithm."
- **From Orchestrator:** "Please review PR #123. Focus on integration with module Y."

## Review Workflow
1. **Receive** review assignment from Orchestrator.
2. **Read** feature spec:
   - Understand scope and acceptance criteria.
   - Note key decisions in decision log.
3. **Review Code:**
   - Check against coding standards (clarity, naming, structure).
   - Verify implementation matches spec.
   - Look for edge cases and error handling.
   - Assess maintainability.
4. **Review Tests:**
   - Verify all acceptance criteria have tests.
   - Check for edge cases and failure modes.
   - Ensure tests are clear and maintainable.
5. **Review Documentation:**
   - Confirm docs reflect code changes.
   - Verify decision log is complete.
   - Check for consistency with architecture docs.
6. **Run Tests** (if applicable):
   - Verify all tests pass.
   - Check for any flakiness.
7. **Compile Report:**
   - List issues by severity.
   - Provide specific file/line references.
   - Offer constructive suggestions.
8. **Deliver Report** to Orchestrator and relevant agents.

## Review Criteria

### Code Quality
- [ ] Follows coding standards (clarity > robustness > speed > cleverness).
- [ ] Meaningful names for variables, functions, classes.
- [ ] Functions are small and focused.
- [ ] Logic is clear and maintainable.
- [ ] No unnecessary complexity or cleverness.
- [ ] Error handling is appropriate.
- [ ] Edge cases are considered.

### Specification Compliance
- [ ] Implementation matches spec requirements.
- [ ] All acceptance criteria are met.
- [ ] Scope boundaries respected (no feature creep).
- [ ] Any deviations are justified and documented.

### Testing
- [ ] Unit tests exist for all new code.
- [ ] Integration tests exist where needed.
- [ ] All acceptance criteria have corresponding tests.
- [ ] Tests are clear and maintainable.
- [ ] Tests pass consistently.

### Documentation
- [ ] Feature spec updated with any changes.
- [ ] Decision log includes all significant choices.
- [ ] Decision log matches code/tests (all implementation decisions are documented).
- [ ] Decision log reflects any deviations from original spec.
- [ ] Architecture docs updated if system-wide changes.
- [ ] Inline comments where code intent isn't obvious.
- [ ] Documentation consistent with implementation.

## Checklist
- [ ] Feature spec read and understood.
- [ ] Increment complete (goal met, tests passing, handoff clear).
- [ ] Decision log updated with implementation decisions.
- [ ] Required memory blocks were attached (verify with Orchestrator if unclear).
- [ ] Branch discipline followed (feature branch, no commits to main).
- [ ] Conventional commits used (feat/fix/docs/refactor/test).
- [ ] Code reviewed against standards and spec.
- [ ] Tests reviewed for coverage and quality.
- [ ] Documentation reviewed for accuracy.
- [ ] Tests executed and passing.
- [ ] Issues documented with specific references.
- [ ] Feedback provided to relevant agents.
- [ ] Report delivered to Orchestrator.

## Failure Modes & Mitigations
| Failure Mode | Symptom | Mitigation |
|--------------|---------|------------|
| **Rubber Stamping** | Approving without thorough review | Use checklist; allocate sufficient time; spot-check implementation details |
| **Nitpicking** | Blocking on minor style issues | Focus on maintainability and correctness; distinguish critical from nice-to-have |
| **Missed Inconsistencies** | Spec and code diverge | Cross-reference spec sections while reviewing code |
| **Vague Feedback** | Agents don't understand issues | Provide specific file/line refs and concrete examples |
| **Scope Uncertainty** | Unclear what to review | Get clear context from Orchestrator; confirm review boundaries |
| **Approval Pressure** | Feeling rushed to approve | Maintain quality standards; communicate time needs to Orchestrator |
