# Feature Management Skills Suite

A complete workflow for creating, building, updating, and removing features in your project with persistent context management.

## Overview

This suite provides four complementary skills that work together to manage features from conception through implementation and maintenance:

```
User Types "/add-feature"
         ↓
   Creates planning context
         ↓
User Types "/build-feature"
         ↓
   Implements from context
         ↓
User Types "/update-feature" (optional)
         ↓
   Makes changes & updates context
         ↓
User Types "/remove-feature" (optional)
         ↓
   Archives & cleans up
```

## Skills

### 1. `/add-feature`
**Purpose**: Plan and scaffold a new feature

**What it does**:
- Reads `project.md` to understand architecture
- Interviews user about feature requirements
- Designs feature to match project patterns
- Creates `features/[feature-name]-context.json` (planning context)
- Creates `features/[feature-name].md` (feature docs with dependencies)
- Creates `features/[feature-name]/` folder structure
- Updates `project.md` with new feature

**Inputs**: Feature name, description, dependencies, acceptance criteria

**Outputs**: 
- Context file (JSON)
- Feature documentation (Markdown)
- Empty feature folder ready for implementation

**Trigger phrases**:
- "/add-feature"
- "add a new feature"
- "create a feature"

---

### 2. `/build-feature`
**Purpose**: Implement a planned feature

**What it does**:
- Loads context from `features/[feature-name]-context.json`
- Reviews feature documentation and dependencies
- Implements code following technical design
- Writes tests and documentation
- Validates against acceptance criteria
- Updates context status when complete

**Inputs**: Feature name (loads context automatically)

**Outputs**:
- Full implementation in `features/[feature-name]/`
- Updated context.json with completion status
- Code, tests, and documentation

**Trigger phrases**:
- "/build-feature"
- "implement this feature"
- "build the feature"
- "let's code this"

**Important**: Context is NOT updated during implementation—only when build is complete. This keeps the context clean and preserves the original design intent.

---

### 3. `/update-feature`
**Purpose**: Fix bugs or add functionality to completed features

**What it does**:
- Loads context and implementation
- Understands change scope and impact
- Implements updates following original patterns
- Validates impact on dependencies
- Updates context when requested (or after changes)

**Inputs**: 
- Feature name
- What needs to change (bug fix, refactor, new functionality)
- Change scope

**Outputs**:
- Updated feature code
- Updated tests
- Updated context with change log

**Trigger phrases**:
- "/update-feature"
- "fix this feature"
- "modify the feature"
- "add functionality to"

**Important**: Context is updated only when user requests it or after significant changes. This keeps the context stable between maintenance cycles.

---

### 4. `/remove-feature`
**Purpose**: Safely delete a feature and clean up

**What it does**:
- Checks for dependent features
- Warns about breaking changes
- Archives context file (optional)
- Removes feature folder
- Removes code references
- Updates project.md

**Inputs**: 
- Feature name
- Reason for removal
- Confirmation of intent

**Outputs**:
- Archived context (in `_archived/`)
- Removed feature folder
- Updated project.md and dependencies

**Trigger phrases**:
- "/remove-feature"
- "delete this feature"
- "remove the feature"
- "get rid of"

---

## File Structure

Each feature has this structure:

```
features/
├── [feature-name]/
│   ├── src/              # Implementation code
│   ├── tests/            # Test files
│   ├── docs/             # Documentation
│   └── README.md         # Feature overview
├── [feature-name].md     # Feature documentation with dependencies
└── [feature-name]-context.json  # Planning & design context
```

Plus in project root:
- `project.md` — Master architecture and feature list
- `_archived/` — Removed feature contexts (optional)

---

## Context File Format

All skills use `features/[feature-name]-context.json` with this structure:

```json
{
  "name": "Feature Name",
  "description": "What it does",
  "projectAlignment": "How it fits into project.md",
  "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
  "technicalDesign": {
    "architecture": "Design approach",
    "fileStructure": { /* directory organization */ },
    "keyDecisions": { /* why decisions were made */ }
  },
  "implementationNotes": "Gotchas and tips",
  "status": {
    "created": "2024-01-15T10:30:00Z",
    "lastUpdated": "2024-01-15T10:30:00Z",
    "phase": "Planning",
    "progress": "0%"
  }
}
```

**See `CONTEXT-SCHEMA.md` for complete schema documentation and examples.**

---

## Key Principles

### 1. Context is Planning, Not Implementation Details
- Context captures **why** decisions were made
- Implementation details live in source code
- Dependencies tracked in feature.md and project.md

### 2. Context Stays Stable
- Original design preserved even as feature evolves
- Only status section updated (replaced, not appended)
- Updates recorded with rationale
- This makes context useful for future developers

### 3. Minimal Context Updates
- **During `/build-feature`**: No updates—work in conversation
- **After `/build-feature`**: Update status to "Complete"
- **During `/update-feature`**: No updates—track changes in conversation
- **After `/update-feature`**: Update status only if user requests

### 4. Dependencies Tracked Separately
- **Features themselves**: Listed in `features/[feature-name].md`
- **Project-wide**: Listed in `project.md`
- **Not in context.json**: Keeps context focused on design

### 5. Clear Naming
- Features use kebab-case: `payment-processing`, `user-authentication`
- Context files: `features/[feature-name]-context.json`
- Documentation: `features/[feature-name].md`
- Folders: `features/[feature-name]/`

---

## Workflow Examples

### Simple Feature (No Updates)

```
1. User: "/add-feature"
   → Creates payment-processing context & docs
   
2. User: "/build-feature"
   → Implements payment processing
   → Updates context to "Complete" when done
   
Done!
```

### Feature with Bug Fix

```
1. User: "/add-feature"
   → Creates export-to-pdf context
   
2. User: "/build-feature"
   → Implements PDF export
   → Updates context to "Complete"
   
3. Bug reported in production
   
4. User: "/update-feature"
   → Fixes rendering issue
   → (No automatic context update)
   
5. User: "Now update the context please"
   → Updates status with fix details
```

### Feature Replacement

```
1. Old feature: payment-stripe (already complete)

2. User: "/add-feature"
   → Creates payment-unified context (supports multiple providers)

3. User: "/build-feature"
   → Implements unified payment system
   → Updates context to "Complete"

4. User: "/remove-feature"
   → Archives payment-stripe context
   → Removes payment-stripe folder
   → Updates project.md
   → Confirms payment-unified is the new payment handler
```

---

## Tips for Success

### When Using `/add-feature`
- Read `project.md` carefully—it contains architectural patterns
- Match naming and structure of existing features
- Make acceptance criteria specific and testable
- Document design decisions with rationale

### When Using `/build-feature`
- Reference context and feature docs constantly
- Keep working notes in conversation (don't update context yet)
- Test as you code—don't wait until the end
- Update context.json only when complete

### When Using `/update-feature`
- Check dependencies before making changes
- Test thoroughly—changes can have side effects
- Document why you changed things, not just what
- Request context update only when you're satisfied

### When Using `/remove-feature`
- Verify no critical dependencies exist
- Archive context for future reference
- Update all documentation
- Make sure you have git history if you need to restore

---

## Integration with Project

These skills assume:
- Your project has a `project.md` file describing architecture
- Features are organized in `features/` directory
- Each feature is self-contained
- Dependencies can be identified by imports or explicit lists

The skills help maintain a clean, documented, and easy-to-understand feature structure that grows as your project grows.

---

## Files in This Skill Suite

- **add-feature-SKILL.md** — Plan and scaffold features
- **build-feature-SKILL.md** — Implement planned features
- **update-feature-SKILL.md** — Maintain and improve features
- **remove-feature-SKILL.md** — Safely remove features
- **CONTEXT-SCHEMA.md** — JSON schema and examples
- **README.md** — This file

---

## Next Steps

1. Review each skill file for details
2. Check CONTEXT-SCHEMA.md for JSON structure examples
3. Install skills into your system
4. Start with `/add-feature` to create your first managed feature
5. Use `/build-feature` to implement it
6. Use `/update-feature` and `/remove-feature` as needed
