# Feature Context JSON Schema

Reference for `features/[feature-name]-context.json` structure used by feature management skills.

## Overview

Each feature has a context file that captures:
- **Original planning** — What was planned before implementation
- **Technical design** — Architecture and key decisions
- **Status** — Current phase and progress

The context file is:
- **Persistent** — Saved and loaded across sessions
- **Planning-focused** — Captures design intent, not implementation details
- **Minimal** — Only updated when build completes or user requests

## Full JSON Schema

```json
{
  "name": "Payment Processing",
  "description": "Handle Stripe payment integration and transaction management",
  "projectAlignment": "Enables core monetization feature; integrates with user-authentication for account linking and transaction history.",
  "acceptanceCriteria": [
    "Process credit card payments via Stripe API",
    "Store transaction history in database",
    "Handle payment failures and retries",
    "Provide webhook handling for payment status updates"
  ],
  "technicalDesign": {
    "architecture": "Follows async/event-driven pattern from project.md. Uses Stripe SDK for payment processing, emits payment events for other features to consume.",
    "fileStructure": {
      "description": "Standard feature structure matching project conventions",
      "directories": [
        "src/ - Implementation code",
        "tests/ - Unit and integration tests",
        "docs/ - API documentation and guides"
      ]
    },
    "keyDecisions": {
      "stripeAsPaymentProvider": "Industry standard with good SDK support; matches project tech stack choice of well-maintained libraries",
      "eventDrivenUpdates": "Allows payment-history and notification features to react to payment events without tight coupling",
      "webhookValidation": "All webhook calls validated with Stripe signatures to prevent spoofing"
    }
  },
  "implementationNotes": "Stripe API has rate limits (100 req/s); consider batch operations for bulk transaction processing. Test webhook handling thoroughly in local environment before deploy.",
  "status": {
    "created": "2024-01-15T10:30:00Z",
    "lastUpdated": "2024-01-15T10:30:00Z",
    "phase": "Planning",
    "progress": "0%"
  }
}
```

## Field Descriptions

### Top-level Fields

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | yes | Feature name |
| `description` | string | yes | One-sentence feature purpose |
| `projectAlignment` | string | yes | How this fits into project.md vision |
| `acceptanceCriteria` | array[string] | yes | Success criteria for completion |
| `technicalDesign` | object | yes | Architecture and design decisions |
| `implementationNotes` | string | no | Gotchas, tips, considerations |
| `status` | object | yes | Current phase and progress |

### `technicalDesign` Object

| Field | Type | Purpose |
|-------|------|---------|
| `architecture` | string | How the feature is built; which patterns from project.md it follows |
| `fileStructure` | object | Directory organization and what goes where |
| `keyDecisions` | object[string → string] | Architecture decisions with rationale |

### `status` Object (Planning Phase)

```json
{
  "created": "2024-01-15T10:30:00Z",
  "lastUpdated": "2024-01-15T10:30:00Z",
  "phase": "Planning",
  "progress": "0%"
}
```

### `status` Object (In Progress)

Not updated during implementation — context stays at "Planning" phase.

### `status` Object (Complete)

```json
{
  "created": "2024-01-15T10:30:00Z",
  "lastUpdated": "2024-01-20T15:45:00Z",
  "phase": "Complete",
  "progress": "100%",
  "completedOn": "2024-01-20T15:45:00Z",
  "notes": "Completed on schedule. Added extra webhook validation after discovering race condition in testing."
}
```

### `status` Object (Active/Maintained - After Updates)

```json
{
  "created": "2024-01-15T10:30:00Z",
  "lastUpdated": "2024-02-01T12:00:00Z",
  "phase": "Active",
  "progress": "100%",
  "completedOn": "2024-01-20T15:45:00Z",
  "updates": [
    {
      "date": "2024-02-01T12:00:00Z",
      "change": "Added refund support",
      "reason": "Users requested ability to refund transactions",
      "scope": "src/payment-handler.js, tests/refunds.test.js",
      "breaking": false
    }
  ]
}
```

## Guidelines

### Keep Context Stable

- **Original planning preserved** — Never rewrite `technicalDesign` or `acceptanceCriteria`
- **Status changes only** — Update only the `status` object to reflect current state
- **Track updates** — If feature evolves, add entries to `status.updates` array

### Avoid Duplication

- **Dependencies NOT in context** — Store in `features/[feature-name].md` and `project.md`
- **Implementation details NOT in context** — Those live in source code
- **Design rationale YES in context** — Why decisions were made, not how they're implemented

### Use ISO 8601 Dates

All dates in `YYYY-MM-DDTHH:MM:SSZ` format (UTC with Z suffix).

Example: `2024-01-15T10:30:00Z`

## When to Update Context

### Create (`/add-feature`)
- Create full context file with all fields at "Planning" phase

### Don't Update (During `/build-feature`)
- Context stays unchanged while coding
- Keep working progress in conversation only

### Update When Build Complete (`/build-feature` finish)
- Change `phase` to "Complete"
- Update `progress` to "100%"
- Add `completedOn` timestamp
- Add optional `notes` field with learnings
- Keep all other fields unchanged

### Update When Requested (`/update-feature`)
- Change `lastUpdated` timestamp
- Add entry to `status.updates` array
- Change `phase` to "Active" if appropriate
- Keep all other fields unchanged
- Can change `completedOn` to reflect when feature was last substantively completed

## Example Timeline

**2024-01-15 10:30** — Feature planned with `/add-feature`
```json
"status": {
  "created": "2024-01-15T10:30:00Z",
  "lastUpdated": "2024-01-15T10:30:00Z",
  "phase": "Planning",
  "progress": "0%"
}
```

**2024-01-20 15:45** — Build completed with `/build-feature`
```json
"status": {
  "created": "2024-01-15T10:30:00Z",
  "lastUpdated": "2024-01-20T15:45:00Z",
  "phase": "Complete",
  "progress": "100%",
  "completedOn": "2024-01-20T15:45:00Z",
  "notes": "Completed on schedule. Added extra webhook validation after discovering race condition in testing."
}
```

**2024-02-01 12:00** — Bug fix via `/update-feature`
```json
"status": {
  "created": "2024-01-15T10:30:00Z",
  "lastUpdated": "2024-02-01T12:00:00Z",
  "phase": "Active",
  "progress": "100%",
  "completedOn": "2024-01-20T15:45:00Z",
  "updates": [
    {
      "date": "2024-02-01T12:00:00Z",
      "change": "Fixed race condition in webhook processing",
      "reason": "Discovered in production that concurrent webhooks could cause duplicate charges",
      "scope": "src/webhook-handler.js",
      "breaking": false
    }
  ]
}
```

**2024-03-15 09:30** — Feature archived via `/remove-feature`
```json
{
  "archived": true,
  "removedDate": "2024-03-15T09:30:00Z",
  "removalReason": "Replaced by unified payment system that handles multiple providers",
  "archivedContent": {
    "originalContext": { /* full context.json */ }
  }
}
```
