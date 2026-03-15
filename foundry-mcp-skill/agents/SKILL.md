---
name: foundry-mcp-agents
description: >-
  Manage and invoke agents through the Foundry MCP Remote server. USE FOR: create agent, update agent, clone agent, start hosted container, stop hosted container, check agent status, invoke agent, multi-turn conversation, hosted agent readiness. DO NOT USE FOR: model deployment workflows, evaluation dataset management, or project connection CRUD.
---

# Foundry MCP Agents

Use this sub-skill for both **prompt agents** and **hosted agents** managed through the remote Foundry MCP server.

## Read This First

Choose the narrower workflow before calling tools:
- Invocation or chat flow → [invoke.md](invoke.md)
- Create/update/clone/delete/container management → [manage.md](manage.md)

## MCP Tools

| Tool | Purpose |
|------|---------|
| `agent_get` | List agents or retrieve one agent |
| `agent_update` | Create, update, or clone an agent |
| `agent_delete` | Permanently delete an agent |
| `agent_definition_schema_get` | Retrieve the authoritative schema before composing agent definitions |
| `agent_container_control` | Start or stop a hosted agent container |
| `agent_container_status_get` | Check hosted container lifecycle state |
| `agent_invoke` | Send a message to an agent |

## Agent Types

| Type | Kind | Notes |
|------|------|-------|
| Prompt agent | `prompt` | Model-backed LLM agent; available immediately after creation or update |
| Hosted agent | `hosted` | Container-backed agent; usually requires container lifecycle operations before invocation |

## Shared Preconditions

1. Ensure the MCP client can authenticate to the Foundry MCP Server. If OAuth DCR is failing in a non-Copilot environment, use the fallback in [../manual-auth.md](../manual-auth.md).
2. Resolve `projectEndpoint`.
3. Resolve `agentName` if the workflow targets a specific agent.
4. If you are creating or updating an agent, retrieve the schema first with `agent_definition_schema_get` unless you already have a validated definition from the same session.
5. For hosted agents, treat container status as a first-class pre-check.

## Practical Guidance

- Use this skill when the user wants an end-to-end agent workflow: resolve the project, create or update the agent, then invoke it to verify behavior.
- For prompt agents that need live public information, prefer `web_search_preview` before introducing custom backends.
- After creating a tool-using agent, do a realistic smoke test and confirm the tool was actually used.

## Example User Prompts

- `Use foundry-mcp-skill to create a prompt agent called local-time-agent in my current Foundry project. Use gpt-5.2-chat. It should answer what time it is in a user-provided location by using web search instead of guessing, ask a short clarification question for ambiguous places, and then show me the final stored agent definition.`
- `Use foundry-mcp-skill to invoke local-time-agent in my current Foundry project with 'What time is it in Seattle right now?' and tell me whether it used web search.`
- `Use foundry-mcp-skill to smoke-test local-time-agent with Tokyo, London, and Portland so we can verify normal lookups and ambiguity handling.`

## Common Workflow Patterns

| Intent | Read Next | Typical Tool Sequence |
|--------|-----------|-----------------------|
| Invoke an agent | [invoke.md](invoke.md) | `agent_get` or `agent_container_status_get` → `agent_invoke` |
| Create or update an agent | [manage.md](manage.md) | `agent_definition_schema_get` → `agent_update` |
| Clone an agent | [manage.md](manage.md) | `agent_get` → `agent_update` with clone settings |
| Start or stop hosted runtime | [manage.md](manage.md) | `agent_container_status_get` → `agent_container_control` |
| Delete an agent | [manage.md](manage.md) | `agent_get` → `agent_delete` |

## Guardrails

- Do not delete an agent before confirming the name and intended project scope.
- Do not invoke a hosted agent blindly when the container is `Stopped`, `Failed`, or still `Starting`.
- If the user's client cannot get through MCP auth, switch to the manual bearer-token fallback before abandoning the agent workflow.
- Reuse `conversationId` for multi-turn conversations.
- If a workflow needs sticky sessions for hosted agents, carry the same `sessionId` across follow-up turns.
