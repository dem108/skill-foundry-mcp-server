# Project Connection Workflows

Use this document for listing metadata and managing project connections in a Foundry project.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `project_connection_list_metadata` | Discover valid connection categories and auth types |
| `project_connection_list` | List connections and optional datastores |
| `project_connection_get` | Retrieve one connection |
| `project_connection_create` | Create or replace a connection |
| `project_connection_update` | Update a connection |
| `project_connection_delete` | Delete a connection |

## Required Scope

These workflows use `foundryProjectResourceId`, not `projectEndpoint`.

Format:
`/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}`

## Recommended Workflow Order

### Step 1: Discover metadata when needed

If the user is creating or updating a connection and is unsure about valid values, call `project_connection_list_metadata` first.

### Step 2: Inspect existing connections

Use `project_connection_list` to understand current state before mutating it.

Helpful filters:
- `category`
- `target`
- `includeAll`

### Step 3: Read one connection when targeting an existing entry

Use `project_connection_get` when the workflow targets a single known connection name.

### Step 4: Mutate

#### Create or replace a connection
Call `project_connection_create` with:
- `foundryProjectResourceId`
- `connectionName`
- `authType`
- `category`
- `target`
- optional `apiKey`
- optional `expiryTime`

#### Update a connection
Call `project_connection_update` with the same shape when editing an existing entry.

#### Delete a connection
Call `project_connection_delete` only after confirming the target by name.

## Guardrails

- Prefer `project_connection_list_metadata` before guessing category or auth type values.
- Be explicit about whether you are creating vs updating.
- Treat secrets like `apiKey` as user-provided sensitive inputs; do not echo them back unnecessarily.
