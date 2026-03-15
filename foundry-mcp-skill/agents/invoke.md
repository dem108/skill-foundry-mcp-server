# Invoke Foundry Agent via Remote MCP

Use this workflow to chat with, smoke-test, or functionally validate an existing agent.

## When to Use This Workflow

- Send a one-off message to a prompt or hosted agent
- Continue a multi-turn conversation using `conversationId`
- Verify a new or updated agent responds correctly
- Route repeated calls through the same sticky `sessionId` when required by the hosted runtime

## Required Inputs

| Parameter | Required | Notes |
|-----------|----------|-------|
| `projectEndpoint` | Yes | Project scope for all agent invocations |
| `agentName` | Yes | Target agent |
| `inputText` | Yes | The user message or test prompt |
| `agentVersion` | No | Use when targeting a specific published version |
| `conversationId` | No | Reuse for multi-turn conversation state |
| `sessionId` | Sometimes | Use for sticky hosted sessions when the runtime expects it |

## Workflow

### Step 0: Ensure MCP server access

Before troubleshooting the target agent itself, make sure the client can authenticate to the Foundry MCP Server.

- If the user is in a non-Copilot environment and OAuth DCR is failing, switch to the fallback in [../manual-auth.md](../manual-auth.md).
- Use `https://mcp.ai.azure.com` as the default Foundry MCP Server endpoint unless the user explicitly provides a different one.
- That fallback uses `az account get-access-token --resource https://mcp.ai.azure.com` and the script at `../scripts/manual_mcp_client.py` to send `Authorization: Bearer ...` on the HTTP transport.

### Step 1: Verify the target agent

Use `agent_get` when the agent name is uncertain or when you need to verify the type.

- If the user gave an explicit `agentName` and recent context already proved it exists, you can skip this read.
- Otherwise, call `agent_get` first.

### Step 2: Check readiness

**Prompt agent**
- Ready immediately after creation or update.
- Optional pre-check: `agent_get`.

**Hosted agent**
- Call `agent_container_status_get`.
- Status handling:
  - `Running` → proceed
  - `Starting` → tell the user it is not ready yet and re-check if they want to wait
  - `Stopped` → offer to start it with `agent_container_control`
  - `Failed` → stop and surface the failure before invoking

### Step 3: Invoke the agent

Call `agent_invoke` with:
- `projectEndpoint`
- `agentName`
- `inputText`
- `agentVersion` if provided
- `conversationId` if continuing a thread
- `sessionId` if the hosted environment needs sticky routing

For tool-using prompt agents, inspect the returned `output` items to confirm the expected tool was actually used.

### Step 4: Continue a conversation

For follow-up turns:
1. keep the returned `conversationId`,
2. keep the same `sessionId` when using sticky hosted sessions,
3. pass both back into the next `agent_invoke` call.

## Error Handling

| Error | Likely Cause | Response |
|-------|--------------|----------|
| MCP auth failure | Client-side OAuth DCR failed or bearer token is missing/expired | Use [../manual-auth.md](../manual-auth.md) or refresh the bearer token |
| Agent not found | Wrong `agentName` or wrong project | Re-run `agent_get` and verify the target |
| Hosted container not ready | Runtime is stopped, starting, or failed | Use `agent_container_status_get`, then `agent_container_control` if appropriate |
| Invocation rejected | Invalid payload or model/runtime issue | Surface the MCP error clearly; do not hide it behind a fake success |
| Lost conversation context | Missing or stale `conversationId` | Start a new conversation without `conversationId` |

## Practical Notes

- Keep invocations small when you are smoke-testing a deployment.
- Separate MCP transport auth failures from `agent_invoke` payload or runtime failures.
- If the user wants a brand new thread, omit `conversationId` and create a new `sessionId` only if the runtime model requires one.
- For hosted agents, container status is part of the workflow, not an optional diagnostic.
- For a newly created tool-using agent, run at least one happy-path invocation and one ambiguity check when the prompt says the agent should ask follow-up questions.

## Example User Prompts

- `Use foundry-mcp-skill to invoke local-time-agent in my current Foundry project with 'What time is it in Seattle right now?' and tell me whether it used web search.`
- `Use foundry-mcp-skill to test local-time-agent with 'What time is it in Portland right now?' and confirm whether it asks a clarification question instead of guessing.`
