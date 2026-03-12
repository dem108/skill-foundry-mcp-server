# Evaluation Runs and Comparison Workflows

Use this document for batch execution, run inspection, and comparison analysis.

## Dataset-Target Batch Evaluation

Tool: `evaluation_dataset_batch_eval_create`

Required inputs:
- `projectEndpoint`
- `evaluatorNames`
- one dataset source supported by the tool invocation pattern

Optional inputs:
- `evaluationId`
- `evaluationName`
- `runName`
- `deploymentName` for LLM-judge evaluators

Workflow:
1. Verify datasets and evaluator names first.
2. Call `evaluation_dataset_batch_eval_create`.
3. Inspect runs with `evaluation_get`.

## Agent-Target Batch Evaluation

Tool: `evaluation_agent_batch_eval_create`

Required inputs:
- `projectEndpoint`
- `agentName`
- `agentVersion`
- `evaluatorNames`

Optional inputs:
- `evaluationId`
- `evaluationName`
- `runName`
- `systemPrompt`
- `deploymentName`
- synthetic data generation inputs such as `generateSyntheticData`, `samplesCount`, `generationPrompt`, `generationModelDeploymentName`, `outputDatasetName`

Workflow:
1. Verify the agent exists.
2. Verify evaluator names exist.
3. If using synthetic data, verify the generation deployment is suitable.
4. Call `evaluation_agent_batch_eval_create`.
5. Inspect resulting runs with `evaluation_get`.

## Inspection Workflows

### List evaluation groups
- Call `evaluation_get` with default `isRequestForRuns: false`.

### List runs within an evaluation group
- Call `evaluation_get` with `isRequestForRuns: true` and `evalId`.

### Get one run
- Call `evaluation_get` with `isRequestForRuns: true`, `evalId`, and `evalRunId`.

## Comparison Workflows

### List comparisons
- Call `evaluation_comparison_get` with `projectEndpoint` only.

### Get one comparison
- Call `evaluation_comparison_get` with `insightId`.

### Create a comparison
1. Resolve the baseline and treatment run IDs.
2. Construct the `insightRequest` payload carefully.
3. Call `evaluation_comparison_create`.

## Guardrails

- Batch evaluation tools can create new evaluation groups if you do not supply an existing `evaluationId`.
- Keep run identifiers from the creation response so later inspection and comparison calls are easy.
- Comparison requests should use clearly identified baseline and treatment runs; do not guess run IDs.
