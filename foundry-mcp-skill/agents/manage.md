# Manage Foundry Agents via Remote MCP

Use this workflow to create, update, clone, delete, or operate hosted agent containers.

## MCP Tools

| Tool | Use |
|------|-----|
| `agent_definition_schema_get` | Discover the valid schema before composing or editing a definition |
| `agent_update` | Create, update, or clone an agent |
| `agent_get` | Confirm existence, kind, and versions |
| `agent_delete` | Delete an agent permanently |
| `agent_container_status_get` | Check hosted container lifecycle state |
| `agent_container_control` | Start or stop the hosted runtime |

## Workflow Patterns

### Create or update an agent

1. Resolve `projectEndpoint` and desired `agentName`.
2. Call `agent_definition_schema_get` for the relevant schema (`prompt`, `hosted`, `tools`, or `all`) if you do not already have a validated structure.
3. Build the `agentDefinition` carefully:
   - prompt agents need a valid model reference,
   - hosted agents need image/runtime settings,
   - creation options can include metadata and description.
4. Call `agent_update`.
5. Read back the result or use `agent_get` if you need to verify what now exists.

### Clone an agent

1. Use `agent_get` to confirm the source agent and current version.
2. Call `agent_update` with:
   - `isCloneRequest: true`
   - `cloneTargetAgentName`
   - new `agentName`
   - optional `modelName` override if the clone should switch models.
3. Verify the cloned agent with `agent_get`.

### Start or stop a hosted container

1. Call `agent_container_status_get` first.
2. Only call `agent_container_control` if a state change is needed.
3. After start/stop, re-check status if the user needs confirmation.

### Delete an agent

1. Confirm `projectEndpoint` and `agentName`.
2. Use `agent_get` if there is any ambiguity.
3. Call `agent_delete` only after confirmation.

## Container State Guidance

| State | Meaning | Typical Action |
|-------|---------|----------------|
| `Running` | Runtime is ready | Invoke or leave it alone |
| `Starting` | Runtime is coming up | Wait and poll if needed |
| `Stopped` | Runtime is not serving | Start it before invoking |
| `Failed` | Startup or runtime failure | Surface the failure; do not mask it |
| `Updating` | Runtime mutation in progress | Wait until it stabilizes |

## Guardrails

- Always retrieve the schema before building a new definition shape from scratch.
- Do not assume a hosted agent will start instantly; container lifecycle is asynchronous.
- Treat delete as irreversible.
- Preserve explicit version targeting when the user asks for a specific agent version.
