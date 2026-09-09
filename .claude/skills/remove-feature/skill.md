---
name: remove-feature
description: Delete a feature and clean up all related files. Trigger when user types "/remove-feature", "delete this feature", "remove the feature", or "get rid of". This skill safely removes a feature by checking dependencies, archiving context, and cleaning up files. Use this to remove deprecated or unneeded features.
---

# Remove Feature Workflow

Safely delete a feature from your project.

**Reference**: See `CONTEXT-SCHEMA.md` for the JSON structure used by context files.

## Step 1: Identify Feature & Validate

When invoked, ask the user:

1. **Which feature to remove?** — Feature name
2. **Reason for removal?** — Why is it being removed?
3. **Confidence** — Are you sure this should be deleted?

Then validate:
- **Does it exist?** — Confirm feature folder and context file exist
- **Is it a dependency?** — Check project.md and other features/[feature-name].md files
- **Is it in use?** — Are there imports or references elsewhere in the codebase?

Read:
- `features/[feature-name]-context.json` — Understand the feature purpose
- `features/[feature-name].md` — Check dependencies and what might be using it
- `project.md` — Verify project-level dependencies

## Step 2: Check Dependencies

Warn the user if:
- Other features list this one as a dependency
- The codebase has imports from this feature
- The feature is critical to project functionality

Ask for confirmation if there are dependents. Option to:
- **Proceed anyway** — User takes responsibility for cleanup
- **List dependents** — Show what will break
- **Cancel** — Do not remove

## Step 3: Archive Context (Optional)

Before deletion, optionally:
1. **Create archive** — Save `features/[feature-name]-context.json` to `_archived/`
2. **Document removal** — Add removal metadata to archived context
3. **Keep for reference** — Use archived context if feature needs to be restored

Archive file: `_archived/[feature-name]-context.json` with added fields:

```json
{
  "archived": true,
  "removedDate": "[ISO 8601 date]",
  "removalReason": "[Why it was removed]",
  "archivedContent": {
    "originalContext": { /* full context.json content */ }
  }
}
```

## Step 4: Remove Feature

Delete:
1. **Feature folder** — Remove `features/[feature-name]/` entirely
2. **Context file** — Remove `features/[feature-name]-context.json` (or archive it first)
3. **Feature docs** — Remove `features/[feature-name].md`
4. **Code references** — Remove imports/uses from other features
5. **Tests** — Remove tests that depend on this feature
6. **Documentation** — Remove or update any docs referencing the feature

Update:
- Remove from project feature list in `project.md`
- Update any feature dependency lists in other features/[feature-name].md files
- Update any architectural documentation

## Step 5: Update Project Context

Update `project.md` if it references this feature:
- Remove from feature list
- Update feature count/summary
- Note in changelog that feature was removed

## Step 6: Verify Cleanup

Confirm:
- [ ] Feature folder removed
- [ ] Context file removed (or archived)
- [ ] No imports of this feature remain
- [ ] Tests updated/removed
- [ ] Documentation updated
- [ ] project.md updated
- [ ] No broken references

## Tips for Success

- **Check thoroughly** — Don't miss references with grep/find
- **Archive first** — Save context before deletion, just in case
- **Verify dependents** — Make sure nothing will break when this is removed
- **Update documentation** — Keep project.md and README accurate
- **Commit carefully** — Consider what the git history should show
- **Consider deprecation** — Could this be deprecated instead of removed?

---

## Example Workflow

**User**: "/remove-feature"

**Claude**: "Which feature would you like to remove?"

**User**: "old-payment-system"

**Claude**:
- Checks if other features depend on it
- Finds references in codebase
- Warns about dependencies
- User confirms removal
- Archives context file
- Removes feature folder and all files
- Removes imports from other features
- Updates project.md
- Verifies cleanup is complete
