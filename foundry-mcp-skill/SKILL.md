---
name: foundry-mcp-skill
description: "**WORKFLOW SKILL** — Orchestrate the Foundry MCP Remote server for agents, model deployments, evaluations, project connections, and prompt optimization. WHEN: \"foundry MCP\", \"remote Foundry server\", \"manage Foundry agent\", \"deploy or inspect model\", \"run evaluation\", \"manage project connection\", \"optimize prompt\". INVOKES: remote Foundry MCP tools first; ask the user only for unresolved identifiers. FOR SINGLE OPERATIONS: read the matching sub-skill or call the specific MCP tool directly."
---

# Foundry MCP Skill

This skill helps an agent use the `foundry-mcp-remote` server as a workflow surface instead of treating each MCP call in isolation. It is MCP-first, workflow-oriented, and designed for broad coverage of the remote Foundry toolset.

The Foundry MCP Server endpoint is `https://mcp.ai.azure.com`.

## Sub-Skills

> **MANDATORY:** Before executing any workflow, read the matching sub-skill document first. Do not jump straight to a remote MCP tool call just because the parameter list looks obvious. The workflow docs below define required pre-checks, identifier resolution, and escalation rules.

> **MANDATORY for model discovery:** If the user gives a model family or partial name, start with `model_catalog_list` and explore related catalog entries before calling `model_details_get`. Do not assume the first matching detail record is the intended model.

> **MANDATORY for client auth failures:** If the user's MCP client cannot complete OAuth DCR against the Foundry MCP Server at `https://mcp.ai.azure.com`, offer the manual bearer-token fallback in [manual-auth.md](manual-auth.md). This is especially relevant for non-Copilot environments or tools where DCR is currently unreliable.

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| **agents** | Create, inspect, clone, invoke, delete, or operate hosted agent containers | [agents/SKILL.md](agents/SKILL.md) |
| **models** | Browse model catalog, inspect deployments, deploy or delete models, check quota, monitoring, deprecation, benchmarks, or recommendations | [models/SKILL.md](models/SKILL.md) |
| **evaluations** | Manage datasets, evaluator catalog entries, batch evaluation runs, and evaluation comparisons | [evaluations/SKILL.md](evaluations/SKILL.md) |
| **project-connections** | Discover metadata and manage project connections and datastores | [project-connections/project-connections.md](project-connections/project-connections.md) |
| **prompt-optimizer** | Optimize developer prompts or refine an existing system message against a deployed model | [prompt-optimizer/prompt-optimizer.md](prompt-optimizer/prompt-optimizer.md) |

## Intent Routing

Match the user's request to the most specific workflow and read that document before acting.

| User Intent | Workflow to Read |
|-------------|------------------|
| MCP server auth is failing in a non-Copilot client | `manual-auth.md` |
| Chat with or smoke-test an agent | `agents/invoke.md` |
| Create, update, clone, or delete an agent | `agents/manage.md` |
| Start, stop, or check a hosted agent container | `agents/manage.md` |
| Browse model catalog or inspect deployment details | `models/deployments.md` |
| Create, update, or delete a model deployment | `models/deployments.md` |
| Check quota, monitoring, deprecation, benchmark, similar-model, or switch guidance | `models/operations.md` |
| Register datasets or custom evaluators | `evaluations/datasets-and-evaluators.md` |
| Run agent-target or dataset-target batch evaluations | `evaluations/runs-and-comparisons.md` |
| Compare evaluation runs | `evaluations/runs-and-comparisons.md` |
| List, create, update, or delete project connections | `project-connections/project-connections.md` |
| Improve a system prompt or developer message | `prompt-optimizer/prompt-optimizer.md` |

> 💡 **Tip:** If the user asks for an end-to-end task like “evaluate my agent” or “deploy and test a model-backed agent,” chain the relevant sub-skills in order instead of compressing everything into one improvised flow.

## Shared Identifier Resolution

Only ask for values that are still missing after checking the user request and the current session context.

### Core identifiers

| Identifier | Typical Format | Common Workflows |
|------------|----------------|------------------|
| `projectEndpoint` | `https://{account}.services.ai.azure.com/api/projects/{project}` | agents, evaluations, prompt optimization |
| `foundryAccountResourceId` | `/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}` | models, account-level monitoring, quota, deployment management |
| `foundryProjectResourceId` | `/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}` | project connections |
| `agentName` | logical agent name | agent management and invocation |
| `deploymentName` | model deployment name | deployment, monitoring, and optimizer workflows |
| `datasetName` / `evaluationId` / `runId` | Foundry evaluation identifiers | evaluation workflows |

### Resolution order

1. Extract identifiers from the user's message.
2. Reuse identifiers established earlier in the same session.
3. If the user only supplied one scope, formulate the nearest likely identifier from context:
   - `projectEndpoint` often implies the related project context for agent and evaluation calls.
   - `foundryAccountResourceId` often implies the account scope for model deployment and monitoring calls.
   - `foundryProjectResourceId` is required for project connections; do not substitute `projectEndpoint` unless the user explicitly confirms the mapped project.
4. Show the inferred identifier to the user and confirm it before any workflow step that depends on it.
5. Ask the user only for the unresolved value that still blocks the next tool call.

> ⚠️ **Do not treat inferred resource IDs or endpoints as final automatically.** The agent may formulate a likely identifier from context, but it must confirm that inferred value with the user before proceeding.

## Workflow Families

### Agents

Use the remote MCP server for the full hosted/prompt agent lifecycle:
- `agent_get`
- `agent_update`
- `agent_delete`
- `agent_definition_schema_get`
- `agent_container_control`
- `agent_container_status_get`
- `agent_invoke`

### Models

Use model workflows for catalog discovery, deployment management, and operational insight:
- `model_catalog_list`
- `model_details_get`
- `model_deploy`
- `model_deployment_get`
- `model_deployment_delete`
- `model_quota_list`
- `model_monitoring_metrics_get`
- `model_deprecation_info_get`
- `model_similar_models_get`
- `model_switch_recommendations_get`
- `model_benchmark_get`
- `model_benchmark_subset_get`

### Evaluations

Use evaluation workflows for both preparation and execution:
- `evaluation_dataset_get`
- `evaluation_dataset_create`
- `evaluation_dataset_versions_get`
- `evaluator_catalog_get`
- `evaluator_catalog_create`
- `evaluator_catalog_update`
- `evaluator_catalog_delete`
- `evaluation_dataset_batch_eval_create`
- `evaluation_agent_batch_eval_create`
- `evaluation_get`
- `evaluation_comparison_get`
- `evaluation_comparison_create`

### Project connections

Use project connection workflows to discover valid metadata and manage connection entries:
- `project_connection_list_metadata`
- `project_connection_list`
- `project_connection_get`
- `project_connection_create`
- `project_connection_update`
- `project_connection_delete`

### Prompt optimization

Use `prompt_optimize` to iteratively improve a system prompt or developer message tied to a known model deployment.

## Tool Usage Conventions

- Prefer the remote Foundry MCP tools over Azure CLI or SDK fallbacks when the workflow is covered.
- Use `ask_user` only when a required identifier or behavioral choice is unresolved.
- For multi-step workflows, summarize the plan briefly, execute the MCP calls in the documented order, and report the concrete outcome.
- For model-family requests, prefer one or more `model_catalog_list` passes to understand nearby variants before narrowing to `model_details_get`.
- If MCP transport auth fails in the user's client, route to `manual-auth.md` before giving up on the Foundry MCP path.
- When a workflow can mutate state, verify the target first with a read operation whenever practical.
- Reuse returned IDs like `conversationId`, evaluation IDs, or dataset versions instead of regenerating state.
- For agent workflows, prefer an end-to-end loop: resolve project scope, create or update the agent, then invoke it with a realistic smoke test before declaring the workflow complete.
- Agent workflows are especially useful when the user wants one request to cover setup plus validation, such as creating an agent and immediately verifying that it can answer a real prompt with the intended tools.

## Prerequisites

- Access to a Foundry environment with the remote MCP server configured.
- Use `https://mcp.ai.azure.com` as the default Foundry MCP Server endpoint unless the user explicitly says they are targeting a different environment.
- A working auth path to the MCP server, either through the client's normal OAuth flow or the fallback in `manual-auth.md`.
- Valid Foundry identifiers for the target workflow.
- Permission to create or mutate the target resources.

## Escalation / Fallback

If the required workflow is not covered by the available remote MCP tools:
1. tell the user which gap you found,
2. preserve the identifiers you already resolved,
3. fall back to the nearest official toolchain only if the user wants that fallback.

## Additional Resources

- [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Foundry Samples](https://github.com/azure-ai-foundry/foundry-samples)
