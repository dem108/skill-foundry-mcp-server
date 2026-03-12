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
