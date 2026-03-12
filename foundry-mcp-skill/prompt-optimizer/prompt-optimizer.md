# Prompt Optimizer Workflow

Use this workflow to improve a developer prompt or system message with the remote Foundry MCP prompt optimizer.

## Tool

- `prompt_optimize`

## Required Inputs

| Parameter | Required | Notes |
|-----------|----------|-------|
| `developerMessage` | Yes | The prompt text to optimize |
| `deploymentName` | Yes | The model deployment used for optimization |
| `projectEndpoint` or `foundryAccountResourceId` | Yes | Provide one scope locator |
| `requestedChanges` | No | Use when refining a prompt that has already been optimized once |

## Workflow

1. Capture the exact prompt text the user wants improved.
2. Resolve the model deployment that should drive optimization.
3. Resolve one scope locator:
   - `projectEndpoint`, or
   - `foundryAccountResourceId`.
4. Call `prompt_optimize`.
5. Return the optimized prompt and explain any major change in direction.

## When to Use

- Improve a first draft of a system prompt
- Refine an existing developer message with specific requested changes
- Compare a rough prompt against a deployment-specific optimization result

## Guardrails

- Do not silently rewrite the user's intent; preserve the task while improving instruction quality.
- If the user wants a targeted refinement, pass it through `requestedChanges` rather than overwriting the whole prompt context.
- Treat optimization output as a proposed revision; the user still owns the final prompt.
