---
name: foundry-mcp-models
description: >-
  Work with model catalog, model deployments, quota, monitoring, deprecation, benchmark, and recommendation workflows through the Foundry MCP Remote server. USE FOR: list Foundry models, inspect deployment, deploy model, remove deployment, check model quota, view model metrics, compare model options. DO NOT USE FOR: agent creation/invocation or evaluation dataset management.
---

# Foundry MCP Models

Use this sub-skill for account-scoped model operations exposed by the remote Foundry MCP server.

## Read This First

Choose the narrower workflow before acting:
- Deployment CRUD and inspection → [deployments.md](deployments.md)
- Monitoring, quota, deprecation, benchmark, and recommendation workflows → [operations.md](operations.md)

## MCP Tools

| Tool | Purpose |
|------|---------|
| `model_catalog_list` | Browse the model catalog |
| `model_details_get` | Fetch a model's detailed description and sample code |
| `model_deploy` | Create or update a deployment |
| `model_deployment_get` | List or inspect deployments |
| `model_deployment_delete` | Delete a deployment |
| `model_quota_list` | Inspect regional quota and usage |
| `model_monitoring_metrics_get` | Retrieve deployment monitoring metrics |
| `model_deprecation_info_get` | Inspect deprecation status for a deployment |
| `model_similar_models_get` | Find similar models |
| `model_switch_recommendations_get` | Recommend replacement models |
| `model_benchmark_get` | Retrieve benchmark catalog data |
| `model_benchmark_subset_get` | Fetch benchmark slices for specific model/version pairs |

## Shared Preconditions

1. Resolve `foundryAccountResourceId` for account-scoped calls.
2. Resolve `deploymentName` when the workflow targets a specific deployment.
3. Resolve `region` and subscription only for quota workflows that need them explicitly.
4. If the user names a model but not a deployment, separate model catalog work from deployment work.
5. If the user gives a model family or partial name, treat `model_catalog_list` as the required first step. Use one or more catalog-list queries to understand related variants before calling `model_details_get`.
6. If the workflow creates or updates a deployment and the user did not specify `skuName`, inspect comparable deployments in the same account first so the skill can infer a likely supported SKU instead of relying on a default.

## Common Routes

| User Intent | Read Next |
|-------------|-----------|
| “Show me available models” | [deployments.md](deployments.md) |
| “Deploy this model” | [deployments.md](deployments.md) |
| “Delete this deployment” | [deployments.md](deployments.md) |
| “What quota do I have in eastus?” | [operations.md](operations.md) |
| “Is this deployment deprecated?” | [operations.md](operations.md) |
| “What should I switch to?” | [operations.md](operations.md) |
| “Show benchmark data” | [operations.md](operations.md) |

## Guardrails

- Distinguish `modelName` from `deploymentName`; they are not interchangeable.
- For discovery, list before get: use `model_catalog_list` to find exact and nearby variants, then use `model_details_get` only for the chosen catalog entry.
- If a query like `gpt-5.4` could map to multiple related entries such as `gpt-5.4` and `gpt-5.4-pro`, keep exploring the catalog until the target is clear.
- Verify the account scope before mutating deployments.
- When `skuName` is missing for a deployment create/update flow, use nearby deployments as the primary hint for a supported SKU and retry once on unsupported-SKU errors with a better candidate.
- Use recommendation and similar-model tools as advisory outputs; do not auto-switch a deployment unless the user explicitly asks.
