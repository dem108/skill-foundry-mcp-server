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
4. For prompt agents, choose the simplest practical tool setup that matches the user's goal. For public lookup tasks, `web_search_preview` is often enough.
5. Call `agent_update`.
6. Read back the result or use `agent_get` if you need to verify what now exists.
7. If the new or updated agent is meant to use tools, run a smoke-test invocation immediately before declaring success.

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
- Do not treat `agent_update` success as proof that the agent behaves correctly; validate with an invocation when the workflow depends on tool use.
- Do not assume a hosted agent will start instantly; container lifecycle is asynchronous.
- Treat delete as irreversible.
- Preserve explicit version targeting when the user asks for a specific agent version.

## Prompt-Agent Example: Local Time via Web Search

Example user prompt:

`Using foundry-mcp-skill, create a prompt agent called local-time-agent in my current Foundry project. It should answer questions like "What time is it in Tokyo?" by using web search to find the current local time, not by guessing. If the location is ambiguous, it should ask a short clarifying question. Use gpt-5.2-chat and show me the final agent definition after creation.`

Use this as a default pattern for simple lookup agents unless the user already has a backend or API they want to connect.
