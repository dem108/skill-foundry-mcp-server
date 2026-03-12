# Datasets and Evaluator Catalog Workflows

Use this document for asset preparation before running evaluations.

## Dataset Workflows

### List datasets or inspect one

Inputs:
- `projectEndpoint`
- optional `datasetName`
- optional `datasetVersion`

Actions:
1. Call `evaluation_dataset_get`.
2. If the user needs all versions for one dataset, follow with `evaluation_dataset_versions_get`.

### Create or update a dataset version

Inputs:
- `projectEndpoint`
- `datasetContentUri`
- optional `datasetName`
- optional `datasetVersion`
- optional `datasetType`
- optional `connectionName`
- optional `description`

Actions:
1. Confirm the storage URI and connection details.
2. Call `evaluation_dataset_create`.
3. Verify with `evaluation_dataset_get` or `evaluation_dataset_versions_get` if needed.

## Evaluator Catalog Workflows

### List evaluators or inspect one

Inputs:
- `projectEndpoint`
- optional `name`
- optional `version`
- optional `type`
- optional `limit`

Action:
1. Call `evaluator_catalog_get`.

### Create a custom evaluator

Inputs:
- `projectEndpoint`
- `name`
- `category`
- `scoringType`
- either `promptText` or `codeText`
- optional metadata fields like `displayName`, `description`, `metricName`, scoring bounds, threshold, direction

Action:
1. Ensure exactly one definition strategy is used:
   - prompt-based evaluator via `promptText`, or
   - code-based evaluator via `codeText`.
2. Call `evaluator_catalog_create`.

### Update evaluator metadata

1. Resolve `projectEndpoint`, `name`, and `version`.
2. Call `evaluator_catalog_update`.

### Delete a custom evaluator version

1. Resolve `projectEndpoint`, `name`, and `version`.
2. Call `evaluator_catalog_delete`.

## Guardrails

- Evaluator definition bodies are immutable after creation; use update only for metadata.
- For prompt-based evaluators, keep template variables aligned with the data shape you expect at runtime.
- Use the evaluator list to verify names before starting evaluation runs.
