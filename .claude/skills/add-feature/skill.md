---
name: add-feature
description: Create a new feature for your project and initialize its context. Trigger when user types "/add-feature" or says "add a new feature". This skill reads project.md to understand the project architecture and helps you plan the feature before implementation. It creates a context file (features/[feature-name]-context.json) and feature documentation that stores all planning information for later resumption.
---

# Add Feature Workflow

Create a new feature in your project with full context planning.

**Reference**: See `CONTEXT-SCHEMA.md` for the JSON structure used by context files.

## Step 1: Gather Feature Information

When invoked, collect the following from the user:

1. **Feature Name** — A descriptive, kebab-case name (e.g., `user-authentication`, `export-to-pdf`)
2. **Feature Description** — What should this feature do?
3. **Dependencies** — Does it depend on other existing features?
4. **Acceptance Criteria** — How will you know when it's complete?

## Step 2: Analyze Project Context

Read `project.md` from the root of the project to understand:
- Overall project architecture and goals
- Existing feature patterns and naming conventions
- Technology stack and frameworks in use
- Directory structure and organizational principles
- Any architectural constraints or guidelines

## Step 3: Design the Feature

Based on project.md, help the user define:
- **Feature Purpose** — How does this fit into the project vision?
- **Technical Approach** — Which patterns from the project should this follow?
- **File Structure** — Where will code, tests, docs live?
- **Integration Points** — How does it connect to existing features?
- **Success Metrics** — What makes this feature successful?

## Step 4: Create Context File

Generate `features/[feature-name]-context.json` with:

```json
{
  "name": "[Feature Name]",
  "description": "[Brief description of what this feature does]",
  "projectAlignment": "[How this fits into project.md goals and architecture]",
  "acceptanceCriteria": [
    "Criterion 1",
    "Criterion 2",
    "Criterion 3"
  ],
  "technicalDesign": {
    "architecture": "[How it's built, which patterns it follows from project.md]",
    "fileStructure": {
      "description": "Organization of features/[feature-name]/ directory",
      "directories": ["src/", "tests/", "docs/"]
    },
    "keyDecisions": {
      "decision1": "Rationale based on project patterns",
      "decision2": "Rationale based on project patterns"
    }
  },
  "implementationNotes": "[Gotchas, tips, or considerations from project analysis]",
  "status": {
    "created": "[ISO 8601 date]",
    "lastUpdated": "[ISO 8601 date]",
    "phase": "Planning",
    "progress": "0%"
  }
}
```

**Important**: Dependencies and feature structure are tracked in:
- `features/[feature-name].md` — Feature documentation with file structure and dependencies
- `project.md` — Project-wide feature list and architecture

## Step 5: Create Feature Folder & Documentation

Create the directory structure in `features/[feature-name]/` with:
- `features/[feature-name].md` — Feature documentation with:
  - Overview and purpose
  - File structure and organization
  - Dependencies (other features or external libraries)
  - API or usage documentation
- `src/` — Implementation code
- `tests/` — Test files
- `docs/` — Additional documentation

Update `project.md` to include this feature in the feature list.

## Tips for Success

- **Read project.md carefully** — Extract naming conventions, architectural patterns, tech stack, and existing feature examples
- **Check for duplication** — Scan existing features to ensure you're not building something that already exists
- **Follow project patterns** — Use the same language, framework, and file organization as the rest of the project
- **Document decisions** — Record *why* you made architectural choices, not just *what* they are
- **Link to dependencies** — Reference other features this depends on by name

---

## Output

This skill creates:

1. **`features/[feature-name]-context.json`** — Planning context (used by `/build-feature` to resume)
2. **`features/[feature-name].md`** — Feature documentation with dependencies
3. **`features/[feature-name]/`** — Folder structure (empty, ready for `/build-feature`)
4. **Updated `project.md`** — Adds feature to project feature list

## Example Workflow

**User**: "/add-feature"

**Claude**: Reads project.md, then asks:
1. What's the feature name?
2. What should it do?
3. What other features does it depend on?

**User provides**: "Payment processing", "Handle Stripe integration", "Depends on user-authentication"

**Claude**: 
- Analyzes project.md architecture
- Designs feature to match project patterns
- Creates `features/payment-processing-context.json` (with planning context)
- Creates `features/payment-processing.md` (with dependencies and structure)
- Creates `features/payment-processing/` folder
- Updates `project.md`
- Summarizes what's ready for `/build-feature`
