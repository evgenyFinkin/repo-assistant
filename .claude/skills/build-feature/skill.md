---
name: build-feature
description: Implement an existing feature based on its context file. Trigger when user types "/build-feature", "implement this feature", or "build the feature". This skill loads the feature's context from features/[feature-name]-context.md and implements it according to the design. Use this to resume work on a feature or execute a planned design.
---

# Build Feature Workflow

Implement a feature that has been planned with `/add-feature`.

**Reference**: See `CONTEXT-SCHEMA.md` for the JSON structure used by context files.

## Step 1: Load Feature Context

When invoked, ask the user:

1. **Which feature?** — Provide the feature name or list available features

Then read:
- `features/[feature-name]-context.json` — Planning context, technical design, and acceptance criteria
- `features/[feature-name].md` — Feature documentation and dependencies
- `project.md` — Project architecture and other features (for context)

## Step 2: Clarify Starting Point

Determine current status:
- **Not started** — Begin from Step 1 of implementation plan
- **In progress** — Ask what's been done; resume from checkpoint
- **Blocked** — Understand the blocker and proceed around it

## Step 3: Implement the Feature

Follow the technical design from the context file:

1. **Create core implementation** — Write the main feature code
2. **Add tests** — Unit tests, integration tests as specified
3. **Write documentation** — README, API docs, usage examples
4. **Handle edge cases** — Implement error handling and validation
5. **Integrate with dependencies** — Connect to required features/systems

**Note**: Do not update the context file during implementation. Keep working context in conversation. Context will be updated when build is complete.

## Step 4: Test & Validate

Verify against acceptance criteria from context file:
- [ ] Run test suite
- [ ] Check against each acceptance criterion
- [ ] Validate integration with dependencies
- [ ] Document any deviations from original design

## Step 5: Update Context (Build Complete)

When feature is complete, update `features/[feature-name]-context.json` status section:

```json
{
  "status": {
    "created": "[Original ISO 8601 date]",
    "lastUpdated": "[Current ISO 8601 date]",
    "phase": "Complete",
    "progress": "100%",
    "completedOn": "[ISO 8601 date]",
    "notes": "[Any lessons learned or changes from original plan]"
  }
}
```

**Keep all other context fields unchanged** — they preserve the original design intent.

## Tips for Success

- **Reference context files constantly** — Keep context.json and feature.md open to check design decisions
- **Keep work context in conversation** — Don't update context file until build is done
- **Test as you build** — Don't wait until the end to validate
- **Respect dependencies** — Ensure required features exist and work correctly
- **Follow project patterns** — Maintain consistency with existing code from project.md
- **Document as you code** — Add comments explaining *why* decisions were made
- **Update context only when done** — Update status section in context.json when feature is complete

---

## Example Workflow

**User**: "/build-feature"

**Claude**: "Which feature would you like to build? Available: payment-processing, export-to-pdf"

**User**: "payment-processing"

**Claude**:
- Reads `features/payment-processing-context.md`
- Summarizes the design and acceptance criteria
- Begins implementation following the technical approach
- Updates context file after each major milestone
- Validates against acceptance criteria
- Marks complete when all criteria met
