# Model Operations and Insight Workflows

Use this document for quota, monitoring, deprecation, benchmark, and recommendation workflows.

## MCP Tools by Intent

| Intent | Tool |
|--------|------|
| Regional quota and usage | `model_quota_list` |
| Deployment monitoring metrics | `model_monitoring_metrics_get` |
| Deprecation status | `model_deprecation_info_get` |
| Similar models | `model_similar_models_get` |
| Switching recommendations | `model_switch_recommendations_get` |
| Full benchmark catalog | `model_benchmark_get` |
| Benchmarks for selected models | `model_benchmark_subset_get` |

## Quota Workflow

Use when the user asks about available deployment quota in a region.

Required inputs:
- `subscriptionId`
- `region`

Action:
1. Call `model_quota_list`.
2. Report available vs used quota.
3. If the user also wants a deployment, switch back to `deployments.md` once quota is understood.

## Monitoring Workflow

Use when the user asks how a deployment is behaving.

Required inputs:
- `foundryAccountResourceId`
- `modelDeploymentName`
- optional `metricCategory`

Action:
1. Call `model_monitoring_metrics_get`.
2. Choose the metric category that matches the user's ask:
   - `Requests`
   - `Latency`
   - `Quota`
   - `AzureOpenAIUsage`
   - `ModelsUsage`
   - `ContentSafetyUsage`
   - `CognitiveServicesSLI`

## Deprecation Workflow

Required inputs:
- `foundryAccountResourceId`
- `modelDeploymentName`

Action:
1. Call `model_deprecation_info_get`.
2. If a model is approaching or past deprecation, follow with `model_switch_recommendations_get`.

## Similar Model Workflow

Choose one input strategy:
- provide `modelDeploymentName`, or
- provide `modelName` + `modelVersion`.

Action:
1. Call `model_similar_models_get`.
2. Use the result for exploration, not for automatic mutation.

## Switch Recommendation Workflow

Use when the user wants a safer migration target.

Inputs:
- `foundryAccountResourceId`
- either `modelDeploymentName` or `modelName` + `modelVersion`
- optional `sortBy`
- optional `top`

Action:
1. Call `model_switch_recommendations_get`.
2. Explain the sorting dimension if you choose one:
   - `QualityIndex`
   - `CostIndex`
   - `ThroughputIndex`
   - `SafetyIndex`
   - `LatencyIndex`
   - `DeprecationDate`
   - `ReleaseDate`
3. If the user wants to act on a recommendation, go back to `deployments.md`.

## Benchmark Workflows

### Full benchmark view
- Call `model_benchmark_get` for broad benchmark data.

### Targeted benchmark view
1. Resolve model pairs.
2. Call `model_benchmark_subset_get` with `{ modelName, modelVersion }[]`.

## Guardrails

- Recommendation tools are advisory; they do not mutate deployments.
- Quota is region-scoped and subscription-scoped; do not infer it from account scope alone.
- Monitoring and deprecation workflows should name the deployment explicitly.
