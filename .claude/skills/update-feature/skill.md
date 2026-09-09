---
name: update-feature
description: Modify an existing completed feature or fix bugs. Trigger when user types "/update-feature", "fix this feature", "modify the feature", or "make changes to". This skill loads the feature's context and implementation, then makes targeted updates. Use this to refactor, add functionality, or fix issues in existing features.
---

# Update Feature Workflow

Modify an existing feature that has already been implemented.

**Reference**: See `CONTEXT-SCHEMA.md` for the JSON structure used by context files.

## Step 1: Load Feature & Context

When invoked, ask the user:

1. **Which feature?** — Feature name to update
2. **What needs to change?** — Bug fix, refactor, new functionality?
3. **Scope** — Is this a small change or major rework?

Then read:
- `features/[feature-name]-context.json` — Original design and decisions
- `features/[feature-name].md` — Feature documentation and dependencies
- `features/[feature-name]/` — Current implementation

## Step 2: Understand Current State

Analyze:
- **What's currently implemented** — Review existing code and structure
- **What's working** — What should be preserved?
- **What's broken or needs change** — Specific issues or desired changes
- **Impact** — Which other features might be affected?

## Step 3: Plan the Update

Document your update plan:
- **Scope** — Exactly what will change
- **Rationale** — Why these changes are needed
- **Testing strategy** — How will you validate the changes?
- **Breaking changes?** — Will this affect dependent features?

**Note**: Keep working notes in conversation. Context will be updated when user requests it or when updates are complete.

## Step 4: Implement Changes

Make the updates:
1. **Modify code** — Update affected files
2. **Update tests** — Fix or add tests for new functionality
3. **Update docs** — Reflect changes in README and docs
4. **Validate** — Run tests and check for regressions
5. **Review** — Compare against original design; explain any deviations

## Step 5: Update Context & Status (When Requested)

When user requests or after updates are complete, update `features/[feature-name]-context.json`:

```json
{
  "status": {
    "created": "[Original ISO 8601 date - keep unchanged]",
    "lastUpdated": "[Current ISO 8601 date]",
    "phase": "Active/Maintained",
    "progress": "100%",
    "updates": [
      {
        "date": "[ISO 8601 date]",
        "change": "[What changed]",
        "reason": "[Why it changed]",
        "scope": "[Files/components affected]",
        "breaking": false
      }
    ]
  }
}
```

**Keep all other context fields** — Preserve original design intent even as feature evolves.

## Tips for Success

- **Preserve original intent** — Don't accidentally break what was working
- **Check dependencies** — Check features/[feature-name].md for what features use this one
- **Test thoroughly** — Updates can have unexpected side effects
- **Document changes** — Explain *why* you changed things, not just *what*
- **Keep track of updates** — Record in conversation what changed and why
- **Consider backwards compatibility** — Can old code still use this feature?
- **Update context when requested** — User decides when to save changes to context.json

---

## Example Workflow

**User**: "/update-feature"

**Claude**: "Which feature would you like to update?"

**User**: "payment-processing — it needs to handle refunds now"

**Claude**:
- Reads context and current implementation
- Plans refund functionality
- Updates code to handle refunds
- Adds tests for refund scenarios
- Updates documentation
- Records the change in context file
- Validates it still works with dependent features
