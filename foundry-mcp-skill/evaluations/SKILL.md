---
name: foundry-mcp-evaluations
description: >-
  Manage Foundry evaluation datasets, evaluator catalog entries, batch or continuous evaluation workflows, and evaluation comparisons through the remote MCP server. USE FOR: register dataset, create evaluator, run batch evaluation, inspect evaluation run, configure continuous eval, compare runs. DO NOT USE FOR: model deployment CRUD or agent container lifecycle.
---

# Foundry MCP Evaluations

Use this sub-skill for evaluation assets, batch execution, and continuous evaluation.

## Read This First

Choose the narrower workflow before acting:
- Dataset and evaluator preparation → [datasets-and-evaluators.md](datasets-and-evaluators.md)
- Batch runs, result inspection, and comparisons → [runs-and-comparisons.md](runs-and-comparisons.md)
- Continuous evaluation configuration → [continuous-evals.md](continuous-evals.md)

## MCP Tools

| Tool | Purpose |
|------|---------|
| `evaluation_dataset_get` | List datasets or fetch a dataset version |
| `evaluation_dataset_create` | Create or update dataset versions |
| `evaluation_dataset_versions_get` | List versions for a dataset |
| `evaluator_catalog_get` | List or fetch evaluator definitions |
| `evaluator_catalog_create` | Create a custom evaluator |
| `evaluator_catalog_update` | Update evaluator metadata |
| `evaluator_catalog_delete` | Delete a custom evaluator version |
| `evaluation_dataset_batch_eval_create` | Run a dataset-target batch evaluation |
| `evaluation_agent_batch_eval_create` | Run an agent-target batch evaluation |
| `evaluation_get` | List evaluation groups or runs |
| `evaluation_comparison_get` | List or fetch comparisons |
| `evaluation_comparison_create` | Create a new comparison insight |
| `continuous_eval_get` | Inspect continuous evaluation configuration for an agent |
| `continuous_eval_create` | Enable or update continuous evaluation for an agent |
| `continuous_eval_delete` | Delete a continuous evaluation configuration |

## Shared Preconditions

1. Resolve `projectEndpoint`.
2. Distinguish preparation assets from execution artifacts:
   - datasets and evaluator catalog entries are reusable assets,
   - evaluations and comparisons are run artifacts.
3. For batch evaluations, make sure the evaluator names exist first.

## Common Routes

| Intent | Read Next |
|--------|-----------|
| Register a dataset | [datasets-and-evaluators.md](datasets-and-evaluators.md) |
| Build a custom evaluator | [datasets-and-evaluators.md](datasets-and-evaluators.md) |
| Run dataset-based evaluation | [runs-and-comparisons.md](runs-and-comparisons.md) |
| Run agent evaluation | [runs-and-comparisons.md](runs-and-comparisons.md) |
| Compare evaluation runs | [runs-and-comparisons.md](runs-and-comparisons.md) |
| Configure continuous evaluation | [continuous-evals.md](continuous-evals.md) |

## Guardrails

- Treat evaluator definitions as versioned assets.
- Do not start an evaluation run with guessed evaluator names.
- Do not enable or delete continuous evaluation without confirming the target agent and configuration.
- Keep evaluation IDs and run IDs from prior responses; they are useful for follow-up inspection and comparison.
