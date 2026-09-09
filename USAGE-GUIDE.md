# Feature Management Skills — Usage Guide

Real-world examples of how to use the feature management skills suite in your project workflow.

## Scenario 1: Build a New Feature from Scratch

You're building a SaaS app and need to add "Team Invitations" functionality.

### Step 1: Plan the Feature

```
You: /add-feature
```

Claude will ask:
- **Feature name?** → `team-invitations`
- **What should it do?** → `Allow users to invite team members via email and manage pending invitations`
- **Dependencies?** → `user-authentication, email-service, team-management`
- **Acceptance criteria?**
  - Users can send team invitations via email
  - Invited users receive email with join link
  - Pending invitations can be revoked
  - Accepted invitations add user to team

Claude reads `project.md`, understands your architecture, and creates:
- `features/team-invitations-context.json` — Planning and design
- `features/team-invitations.md` — Feature docs and dependencies
- `features/team-invitations/` — Empty folder ready for code

**Result**: Feature is planned and documented before any code is written ✅

### Step 2: Build the Feature

A few days later, you're ready to implement:

```
You: /build-feature
```

Claude loads the context and asks:
- **Which feature?** → `team-invitations`

Claude reads the context and:
1. Writes implementation code in `src/`
2. Writes comprehensive tests
3. Writes API documentation
4. Validates all acceptance criteria pass
5. Updates context.json status to "Complete"

You can check progress in conversation, ask questions, and refine the implementation.

**Result**: Feature is fully implemented and tested ✅

### Step 3: Ship It

Update your main app to use the new feature:
```javascript
import { inviteTeamMember } from './features/team-invitations/src/index.js';
```

Deploy to production.

---

## Scenario 2: Fix a Bug in a Completed Feature

Your "Team Invitations" feature is live. Users report that email invitations aren't being sent to certain domains.

### Step 1: Fix the Issue

```
You: /update-feature
```

Claude asks:
- **Which feature?** → `team-invitations`
- **What needs to change?** → `Fix email delivery to corporate domains with strict SPF policies`
- **Scope?** → `Small change to email sending logic`

Claude:
1. Reviews current implementation
2. Identifies the issue with SPF/DKIM validation
3. Updates email sender configuration
4. Adds tests for corporate domain emails
5. Tests thoroughly
6. **Does NOT automatically update context**

You review the fix and test it.

### Step 2: Document the Fix

Once you're satisfied:

```
You: Now update the context please
```

Claude updates `features/team-invitations-context.json`:
- Sets `phase` to "Active"
- Adds entry to `status.updates` array:
  ```json
  {
    "date": "2024-01-25T14:30:00Z",
    "change": "Fixed email delivery to corporate domains with strict SPF policies",
    "reason": "Users on corporate networks weren't receiving invitations",
    "scope": "src/email-sender.js, tests/corporate-domains.test.js",
    "breaking": false
  }
  ```

**Result**: Bug is fixed and change is documented ✅

---

## Scenario 3: Enhance a Feature with New Capability

Your product now supports "Single Sign-On (SSO)" and you want to integrate it with team invitations.

### Existing Feature Status
- `team-invitations` is complete and live
- Currently only supports email invitations
- Users want to invite via SSO organization

### Step 1: Plan the Enhancement

```
You: /add-feature
```

Create new feature: `team-invitations-sso`

This is a complementary feature that:
- Depends on `team-invitations` and `sso-provider`
- Allows syncing team members from SSO organization
- Auto-approves invitations for SSO users
- Removes users when removed from SSO org

Claude creates planning context for the new feature.

### Step 2: Build the Enhancement

```
You: /build-feature
```

Implement `team-invitations-sso` as a separate, focused feature.

**Why separate?**
- Original `team-invitations` feature stays simple and stable
- SSO integration is optional for users who don't use SSO
- Each feature has clear, focused responsibility
- Features can evolve independently

### Step 3: Update Original Feature (Optional)

If you want to update `team-invitations` to mention SSO integration in docs:

```
You: /update-feature
```

Choose: `team-invitations`

Change: `Update documentation to mention SSO integration available via team-invitations-sso`

This is a minimal update that:
- Updates `features/team-invitations/docs/`
- Does not change implementation
- Keeps original feature stable

Claude updates context when you request.

**Result**: SSO integration is available without destabilizing original feature ✅

---

## Scenario 4: Deprecate a Feature

Your app originally had a "Basic Notifications" system, but you've built "Advanced Notifications" with better features. It's time to remove the old one.

### Current State
- `basic-notifications` is complete but no longer used
- `advanced-notifications` is now the primary notification system
- All code that used `basic-notifications` has been migrated

### Step 1: Identify Dependencies

```
You: /remove-feature
```

Claude checks:
- **Which feature?** → `basic-notifications`
- **Why remove it?** → `Replaced by advanced-notifications feature; all code migrated`

Claude verifies:
- No other features depend on it ✅
- No active code references it ✅
- `project.md` can be updated ✅

### Step 2: Archive and Remove

Claude:
1. Archives `features/basic-notifications-context.json` to `_archived/`
2. Removes `features/basic-notifications/` folder
3. Removes `features/basic-notifications.md`
4. Updates `project.md` to remove reference
5. Adds note explaining why it was removed

### Step 3: Future Reference

If you ever need to understand why basic notifications were removed:
```bash
cat _archived/basic-notifications-context.json | jq '.removalReason'
# Output: "Replaced by advanced-notifications feature; all code migrated"
```

The original context is preserved for historical reference.

**Result**: Code is clean, old feature archived for reference ✅

---

## Scenario 5: Maintain Feature Across Multiple Developers

You have multiple developers working on your project. One developer builds a feature, another maintains it later.

### Developer A: Plans Feature

```
You (Dev A): /add-feature
```

Creates `features/payment-processing-context.json` with:
- Detailed technical design
- Rationale for architectural choices
- Acceptance criteria
- Implementation notes and gotchas

Commits to git.

### Developer B: Builds Feature

Weeks later, Dev B (who didn't originally plan it):

```
You (Dev B): /build-feature
```

Claude loads the context and Dev B can:
- Understand the original design intent
- See why certain decisions were made
- Implement following the planned architecture
- Validate against acceptance criteria

**Key benefit**: Design knowledge is captured and reusable. Dev B doesn't have to ask Dev A why they did it that way.

### Developer C: Fixes a Bug

Months later, Dev C finds a bug:

```
You (Dev C): /update-feature
```

Claude loads context and Dev C can:
- Understand the original design (not just current code)
- See architectural constraints
- Fix the bug without breaking original intent
- Document the fix

**Result**: Institutional knowledge is preserved in context files ✅

---

## Scenario 6: Work on a Feature Across Multiple Sessions

You start working on a complex feature but don't finish in one session.

### Session 1: Start Building

```
You: /build-feature
```

Claude loads context for `image-processing`:
- Reads planning and design
- Starts implementing
- Gets through core functionality
- You stop for the day

**Important**: Context is NOT updated during work. Your progress is only in conversation.

### Session 2: Resume Work

```
You: /build-feature
```

Claude loads the exact same context:
- Sees original design intent
- Can refer to it throughout the session
- Continues implementation from where you left off
- Maintains consistency with original design

You can pick up exactly where you left off because:
- Context file was not modified
- Planning is still fresh and available
- Design decisions are documented

### Session 3: Finish and Document

When feature is complete:

```
You: /build-feature
```

Final stage:
- Complete remaining work
- All tests pass
- Documentation done
- **Now** Claude updates context to "Complete"

**Result**: Clean context that serves as permanent reference ✅

---

## Scenario 7: Review Feature Architecture Before Implementation

New developer joins your team. Wants to understand a feature before modifying it.

```
New Dev: Let me understand the payment-processing feature before I work on it.
```

You don't run `/build-feature` yet. Instead:

```
New Dev: Show me the architecture of payment-processing
```

Claude reads `features/payment-processing-context.json` and can explain:
- Original design and rationale
- Architecture pattern used
- Key decisions and why they were made
- Acceptance criteria and success metrics
- Implementation notes and gotchas

No skill needed—just read the context file to onboard!

```bash
cat features/payment-processing-context.json | jq '.technicalDesign.keyDecisions'
```

**Result**: Onboarding is fast because design is documented ✅

---

## Best Practices

### ✅ DO

- **Create context before building** — Use `/add-feature` first
- **Reference context frequently** — Check design during implementation
- **Document decisions** — Add rationale to keyDecisions
- **Update context only when requested** — Keep it clean and stable
- **Track dependencies in feature.md** — Not in context.json
- **Preserve original design** — Don't change technicalDesign after implementation
- **Archive removed features** — Keep context for future reference
- **Use kebab-case** — Naming should be consistent

### ❌ DON'T

- **Build without planning** — Create context first with `/add-feature`
- **Update context constantly** — Only update status section when requested
- **Move design decisions to code comments** — Keep them in context.json
- **Hide dependencies** — List them clearly in feature.md
- **Delete archived contexts** — Keep them for reference
- **Ignore project.md** — Read it to match patterns
- **Make major changes without updating status** — Document updates in status.updates array

---

## Common Workflows

### Quick Bug Fix
```
/update-feature → Fix bug → Test → Done (no context update needed)
```

### Add Small Feature
```
/add-feature → /build-feature → (done, context auto-updates) → Done
```

### Major Refactor
```
/update-feature → Refactor code → Test thoroughly → Update context with breaking changes note
```

### Remove Feature
```
/remove-feature → Archive → Clean up → Done
```

### Onboard New Developer
```
Read features/[name]-context.json → Understand design → Read features/[name].md → Understand dependencies
→ /build-feature or /update-feature as needed
```

---

## Troubleshooting

### "I want to update context but haven't finished the feature yet"
- Wait until feature is complete
- Keep notes in conversation for now
- Update context only when ready to commit

### "What if I change my mind about the design?"
- Update context.json manually if needed (before implementation)
- If already implemented, document change in status.updates

### "My team keeps forgetting about feature dependencies"
- All dependencies MUST be in features/[name].md
- List them prominently
- Claude will reference them in `/add-feature` and `/build-feature`

### "Context file got corrupted somehow"
- Check `_archived/` for a backup (if feature was removed)
- Refer to git history to restore
- Use `/add-feature` to recreate if needed

### "Feature seems half-finished. How do I know what to do next?"
- Read the context file `features/[name]-context.json`
- Check status.phase and status.progress
- If status shows "Complete" but isn't, file a bug report
- Otherwise, `/build-feature` and Claude will resume

---

## Tips & Tricks

### Quickly Understand a Feature
```bash
cat features/[name]-context.json | jq '.technicalDesign.keyDecisions'
```

### See What Changed When
```bash
cat features/[name]-context.json | jq '.status.updates'
```

### List All Features
```bash
ls features/*-context.json | sed 's|features/||' | sed 's|-context.json||'
```

### Check Feature Status
```bash
cat features/[name]-context.json | jq '.status.phase, .status.progress'
```

### Review Dependencies
```bash
grep -h "Depends on\|Requires\|dependency" features/*.md
```

---

## Integration with CI/CD

### Pre-commit Checks
```bash
# Verify all features have context files
for f in features/*/; do
  name=$(basename "$f")
  [ -f "features/${name%-context.json}-context.json" ] || echo "Missing context: $name"
done
```

### Feature Documentation
```bash
# Generate feature list from project.md
grep "^## Features" project.md -A 50
```

### Validation
```bash
# Verify all context.json files are valid
find features -name '*-context.json' -exec jq empty {} \;
```

---

This guide covers the most common scenarios. Adapt the workflow to your team's needs!
