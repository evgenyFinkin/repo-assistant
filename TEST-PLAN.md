# Test Plan for Feature Management Skills

This document outlines how to test the feature management skills suite before deploying to production.

## Test Setup

### Prerequisites
- Project with `project.md` file describing architecture
- `features/` directory created
- Access to create, modify, and delete files
- Ability to run tests with the skill

### Test Data
Create a sample `project.md` with:
- Project description and goals
- Existing features (if any)
- Technology stack
- Architectural patterns
- Directory structure guidelines

Example:
```markdown
# Project Architecture

## Overview
A SaaS application for project management.

## Technology Stack
- Node.js 18+
- React for frontend
- PostgreSQL for database
- Event-driven architecture

## Existing Features
- User Authentication (OAuth2)
- Project Management (CRUD operations)
- Real-time Collaboration (WebSockets)

## Patterns
- Features are self-contained in features/[name]/ directories
- All async operations use events
- Tests must cover happy path and error cases
- Documentation required for public APIs
```

---

## Test Cases

### Test 1: Create a Simple Feature (`/add-feature`)

**Objective**: Verify that `/add-feature` correctly scaffolds a new feature

**Steps**:
1. User invokes: `/add-feature`
2. Respond to prompts:
   - Feature name: `task-management`
   - Description: `Allow users to create, assign, and track tasks within projects`
   - Dependencies: `project-management`, `user-authentication`
   - Acceptance criteria: 
     - Users can create tasks
     - Tasks can be assigned to team members
     - Task status can be updated
     - Tasks deleted permanently

**Expected Outputs**:
- ✅ `features/task-management-context.json` created with:
  - Name, description, projectAlignment, acceptanceCriteria
  - technicalDesign with architecture, fileStructure, keyDecisions
  - status.phase = "Planning"
  - status.progress = "0%"
- ✅ `features/task-management.md` created with:
  - Feature overview
  - File structure description
  - Listed dependencies: project-management, user-authentication
- ✅ `features/task-management/` folder created with src/, tests/, docs/ subdirectories
- ✅ `project.md` updated to include task-management in feature list

**Validation**:
```bash
# Verify files exist
ls -la features/task-management-context.json
ls -la features/task-management.md
ls -la features/task-management/

# Verify context.json is valid JSON
cat features/task-management-context.json | jq .

# Verify project.md mentions task-management
grep -i "task-management" project.md
```

**Pass Criteria**:
- All three files created
- Context.json is valid JSON with all required fields
- project.md includes the new feature

---

### Test 2: Build a Feature (`/build-feature`)

**Objective**: Verify that `/build-feature` loads context and implements

**Steps**:
1. Use feature from Test 1: `task-management`
2. User invokes: `/build-feature`
3. System automatically loads `features/task-management-context.json`
4. Claude implements feature:
   - Creates `features/task-management/src/index.js`
   - Creates `features/task-management/tests/task-management.test.js`
   - Creates `features/task-management/docs/API.md`
   - Implements all acceptance criteria

**Expected Outputs**:
- ✅ Complete implementation in `features/task-management/`
- ✅ Tests passing (100% of acceptance criteria covered)
- ✅ Documentation complete
- ✅ `features/task-management-context.json` updated:
  - status.phase = "Complete"
  - status.progress = "100%"
  - status.completedOn = (current timestamp)
  - Optional: status.notes = (implementation notes)

**Validation**:
```bash
# Verify implementation files exist
ls -la features/task-management/src/
ls -la features/task-management/tests/
ls -la features/task-management/docs/

# Verify context.json updated
cat features/task-management-context.json | jq '.status'

# Expected output:
# {
#   "created": "...",
#   "lastUpdated": "...",
#   "phase": "Complete",
#   "progress": "100%",
#   "completedOn": "..."
# }
```

**Pass Criteria**:
- Implementation exists and runs
- Tests pass
- Documentation complete
- Context.status shows "Complete" with 100% progress
- All other context fields preserved (name, technicalDesign, etc.)

---

### Test 3: Update a Feature (`/update-feature`)

**Objective**: Verify that `/update-feature` can modify completed features

**Steps**:
1. Use feature from Test 2: `task-management` (now complete)
2. User invokes: `/update-feature`
3. Describe change: `Add task priority levels (low, medium, high, urgent)`
4. Claude:
   - Updates implementation to support priorities
   - Adds tests for priority handling
   - Updates documentation
   - Does NOT update context.json automatically

5. User then says: `Now update the context please`
6. Claude updates `features/task-management-context.json`:
   - status.lastUpdated = (current timestamp)
   - status.phase = "Active"
   - Adds entry to status.updates array

**Expected Outputs**:
- ✅ Updated implementation with priority support
- ✅ New tests passing
- ✅ Updated documentation
- ✅ Context unchanged (until user requests update)
- ✅ Context.json updated with change log:
  ```json
  {
    "status": {
      "created": "...",
      "lastUpdated": "2024-XX-XXTXX:XX:XXZ",
      "phase": "Active",
      "progress": "100%",
      "completedOn": "...",
      "updates": [
        {
          "date": "2024-XX-XXTXX:XX:XXZ",
          "change": "Added task priority levels",
          "reason": "Users need to prioritize tasks",
          "scope": "src/task-handler.js, tests/priority.test.js",
          "breaking": false
        }
      ]
    }
  }
  ```

**Validation**:
```bash
# Verify implementation changed
grep -i "priority" features/task-management/src/index.js

# Verify context was NOT updated during change
# (context.json lastUpdated should match previous test)

# After user requests update:
cat features/task-management-context.json | jq '.status.updates'

# Should show the priority update in the updates array
```

**Pass Criteria**:
- Implementation updated correctly
- Context not automatically updated during work
- Context updates only when user requests
- Updates array properly records changes

---

### Test 4: Remove a Feature (`/remove-feature`)

**Objective**: Verify that `/remove-feature` safely removes features

**First**, create a temporary feature to remove:

1. User invokes: `/add-feature`
2. Create temporary feature: `analytics-tracking`
3. Build it: `/build-feature`

**Then**, remove it:

1. User invokes: `/remove-feature`
2. Specify: `analytics-tracking`
3. Reason: `Moving to third-party analytics provider`
4. Confirm deletion

**Expected Outputs**:
- ✅ `features/analytics-tracking/` removed
- ✅ `features/analytics-tracking.md` removed
- ✅ `features/analytics-tracking-context.json` archived to `_archived/`
- ✅ `project.md` updated (analytics-tracking removed from feature list)
- ✅ Archived context includes removal metadata:
  ```json
  {
    "archived": true,
    "removedDate": "2024-XX-XXTXX:XX:XXZ",
    "removalReason": "Moving to third-party analytics provider",
    "archivedContent": {
      "originalContext": { /* full context */ }
    }
  }
  ```

**Validation**:
```bash
# Verify removal
ls -la features/analytics-tracking/  # Should not exist
ls -la features/analytics-tracking.md  # Should not exist

# Verify archive
cat _archived/analytics-tracking-context.json | jq '.archived'
# Should return: true

# Verify project.md updated
grep -i "analytics-tracking" project.md  # Should not find it
```

**Pass Criteria**:
- Feature folder and docs removed
- Context archived with metadata
- project.md updated
- Can recover from archive if needed

---

### Test 5: Context Stability (Verify Original Design Preserved)

**Objective**: Verify that context fields preserve original design even after updates

**Steps**:
1. Create feature with `/add-feature` for `notifications`
2. Record original technicalDesign.keyDecisions:
   ```json
   {
     "eventDriven": "Notifications sent via event system, not direct calls",
     "queueing": "Uses job queue for async notification delivery"
   }
   ```
3. Build feature with `/build-feature`
4. Update feature with `/update-feature` (add email notifications)
5. User requests context update
6. Verify technicalDesign.keyDecisions unchanged

**Validation**:
```bash
# After update, check that keyDecisions preserved
cat features/notifications-context.json | \
  jq '.technicalDesign.keyDecisions'

# Should still show original decisions:
# {
#   "eventDriven": "...",
#   "queueing": "..."
# }
```

**Pass Criteria**:
- Original design decisions preserved
- Only status section modified
- technicalDesign, acceptanceCriteria unchanged

---

### Test 6: Dependencies Correctly Tracked

**Objective**: Verify dependencies tracked in feature.md and project.md, not context.json

**Steps**:
1. Create two features: `user-profiles` and `profile-pictures`
2. `profile-pictures` depends on `user-profiles`
3. Verify:
   - `features/profile-pictures.md` lists `user-profiles` as dependency
   - `project.md` notes the dependency
   - `features/profile-pictures-context.json` does NOT include dependency list

**Validation**:
```bash
# Check feature.md has dependency
grep -i "user-profiles" features/profile-pictures.md  # Should find it

# Check project.md mentions relationship
grep -i "profile-pictures" project.md  # Should mention user-profiles dependency

# Check context.json does NOT have dependency section
jq 'keys' features/profile-pictures-context.json | grep -i dependenc  # Should NOT find it
```

**Pass Criteria**:
- Dependencies documented in feature.md
- Dependencies listed in project.md
- Context.json does not include dependency tracking

---

## Regression Tests

Run these tests after any skill updates to ensure nothing broke:

### Regression 1: Context JSON Schema
Verify all created context.json files conform to schema:
- Required fields present: name, description, projectAlignment, acceptanceCriteria, technicalDesign, status
- Status object has: created, lastUpdated, phase, progress
- All dates are ISO 8601 format with Z suffix

### Regression 2: No Unintended Context Updates
1. Build a feature
2. Work on updating it WITHOUT user requesting context update
3. Verify context.json lastUpdated timestamp unchanged until user explicitly requests update

### Regression 3: Feature Folder Structure
1. Create 3 different features
2. Verify each has:
   - features/[name]/src/
   - features/[name]/tests/
   - features/[name]/docs/
   - features/[name].md in root of features/

### Regression 4: project.md Consistency
1. Add 3 features
2. Remove 1 feature
3. Verify project.md:
   - Lists remaining 2 features
   - Does not reference removed feature
   - Accurately reflects current state

---

## Performance Tests

### Performance 1: Context Loading
- `/build-feature` should load context.json within 1 second
- Should handle large context files (>1MB) gracefully

### Performance 2: Update Speed
- `/update-feature` should complete typical changes in <2 minutes
- Should not keep context file locked during work

---

## Edge Case Tests

### Edge Case 1: Feature Name Already Exists
1. Create feature `notifications`
2. Try to create another `notifications` with `/add-feature`
3. System should warn about duplicate and prevent overwrite

### Edge Case 2: Remove Feature with Dependents
1. Create `user-authentication`
2. Create `user-profiles` depending on `user-authentication`
3. Try `/remove-feature` for `user-authentication`
4. System should warn that `user-profiles` depends on it
5. Require explicit confirmation to proceed

### Edge Case 3: Invalid JSON Context
1. Manually corrupt `features/[name]-context.json`
2. Try `/build-feature` on that feature
3. System should detect corruption and error gracefully
4. Should suggest fixing the JSON file

### Edge Case 4: Missing project.md
1. Try `/add-feature` when `project.md` doesn't exist
2. System should warn about missing file
3. Should either ask for input or refuse gracefully

---

## Success Criteria

All tests pass if:
- ✅ Files created with correct structure
- ✅ Context.json always valid JSON
- ✅ Context stability maintained (original design preserved)
- ✅ Status only field updated between builds/updates
- ✅ Dependencies tracked in feature.md and project.md
- ✅ project.md kept in sync with features
- ✅ Archives preserve complete context for recovery
- ✅ No unintended context updates
- ✅ Clear error messages for edge cases

---

## Running Tests

To run test cases:

1. **Set up test project**:
   ```bash
   mkdir test-project
   cd test-project
   # Create project.md with sample content
   mkdir features _archived
   ```

2. **For each test**:
   - Follow the "Steps" section
   - Verify all "Expected Outputs"
   - Run "Validation" commands
   - Check "Pass Criteria"

3. **Report results**:
   - Document which tests passed/failed
   - Include validation command output
   - Note any unexpected behavior

---

## Notes

- Tests assume fresh project state (features/ created but empty)
- Each test can be run independently after setup
- Tests should be run in order initially
- Regression tests should run after any skill modifications
- Edge cases help identify robustness issues
