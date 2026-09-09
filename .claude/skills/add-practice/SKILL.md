---
name: add-practice
description: Add a new mandatory development practice to practices.md. Use when a user wants to document a required workflow, pattern, or procedure that all developers must follow. Takes practice name, description, and optional link/examples, then appends to practices.md in the standard format.
---

# Add Practice to practices.md

When developers need to establish or document a new required practice, use this skill to add it to `practices.md` with consistent formatting.

## What You Do

1. Collect practice details from the user:
   - **Name** (required): Practice title (e.g., "Docker Development", "Code Review Process")
   - **Description** (required): Explanation of the practice, why it matters, how to do it
   - **Link** (optional): URL reference (docs, tickets, external resources)
   - **Examples** (optional): Code snippets, commands, or concrete examples

2. Format and append to practices.md:
   ```
   ## [Name]
   
   [Description]
   
   [Link section if provided]
   
   [Examples section if provided]
   ```

3. Verify:
   - Practice name is unique (doesn't duplicate existing section)
   - Description is clear and actionable
   - File is readable after append (no broken formatting)

## Output

Updated `practices.md` file with new practice section added before the "Last updated" footer.

## Example Usage

**Input:**
```
Name: Docker Development
Description: All builds happen inside Docker container. If no container exists, build one first. Orchestration via compose.yaml. When agent works inside container, grant full permissions. Remove container when finished.
Link: none
Examples: none
```

**Output:** practices.md updated with:
```
## Docker Development

All builds happen inside Docker container. If no container exists, build one first. Orchestration via compose.yaml. When agent works inside container, grant full permissions. Remove container when finished.
```

## Implementation Notes

- Append new practice before the `---` and "Last updated" line
- Use h2 header (`##`) for practice name
- Preserve existing formatting and sections
- If link provided, format as: `**Reference:** [description](url)`
- If examples provided, format as: `**Examples:**` followed by code block or list
