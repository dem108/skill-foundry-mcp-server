# Continuous Evaluation Workflows

Use this document for agent-level continuous evaluation configuration.

## Get Continuous Evaluation Configuration

Tool: `continuous_eval_get`

Required inputs:
- `projectEndpoint`
- `agentName`

Optional inputs:
- `scenario` (`standard` or `business`; does not apply to hosted agents)

Workflow:
1. Verify the agent exists first.
2. Call `continuous_eval_get`.
3. Preserve returned configuration identifiers for later updates or deletion.

## Create or Update Continuous Evaluation

Tool: `continuous_eval_create`

Required inputs:
- `projectEndpoint`
- `agentName`
- `evaluatorNames`

Optional inputs:
- `deploymentName` for LLM-judge evaluators
- `enabled`
- `intervalHours` (hosted agents)
- `maxTraces` (hosted agents)
- `samplingRate` (prompt/workflow agents)
- `maxHourlyRuns` (prompt/workflow agents)
- `scenario` (`standard` or `business`)

Workflow:
1. Verify the agent exists.
2. Verify evaluator names exist before enabling the configuration.
3. If using quality evaluators, resolve a suitable `deploymentName`.
4. Call `continuous_eval_create`.
5. Read the configuration back with `continuous_eval_get` if the user wants confirmation.

## Delete Continuous Evaluation

Tool: `continuous_eval_delete`

Required inputs:
- `projectEndpoint`
- `agentName`
- `configId`

Workflow:
1. Use `continuous_eval_get` first if the config ID is not already known.
2. Confirm the target configuration.
3. Call `continuous_eval_delete`.

## Guardrails

- Treat continuous evaluation as agent-scoped configuration, not as a one-off evaluation run.
- Do not guess evaluator names; verify them first with the evaluator catalog.
- Preserve `configId` values returned by `continuous_eval_get`; delete requires the exact identifier.
- Hosted agents and prompt/workflow agents support different tuning knobs, so do not assume every optional field applies to every agent kind.
