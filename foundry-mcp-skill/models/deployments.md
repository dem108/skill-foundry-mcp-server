# Model Catalog and Deployment Workflows

Use this document for model discovery and deployment CRUD.

## Typical Inputs

| Parameter | Used For |
|-----------|----------|
| `foundryAccountResourceId` | Account scope for deployment management |
| `deploymentName` | Inspecting, updating, or deleting an existing deployment |
| `modelName` | Catalog lookup or new deployment target |
| `modelVersion` | Pinning a specific version when deploying |
| `modelFormat` | Required for deployment creation |
| `skuName` / `skuCapacity` / `scaleType` / `scaleCapacity` | Optional deployment configuration |

## SKU Resolution for New Deployments

Treat SKU selection as an explicit decision, not a hidden default.

1. If the user provided `skuName` or `skuCapacity`, use that input directly.
2. If the user did not provide a SKU, inspect existing deployments in the same account with `model_deployment_get` and look for comparable entries:
   - same model family,
   - same publisher or format,
   - same capabilities such as `chatCompletion`, `responses`, or `embeddings`.
3. Reuse a matching SKU pattern when the account already shows one clearly. For example:
   - if nearby OpenAI chat or responses deployments in the same account use `GlobalStandard`, prefer `GlobalStandard`,
   - do not assume `Standard` is safe just because it is a common default.
4. If there is no strong comparable signal, tell the user which SKU you inferred and why before the mutating call.
5. Keep the first attempt conservative:
   - preserve any explicit user-provided SKU,
   - if capacity is unknown, start with a small capacity such as `1` unless the user asked for higher throughput.
6. If `model_deploy` fails with an unsupported-SKU error such as `InvalidResourceProperties`, re-check comparable deployments and retry once with the next best candidate instead of stopping immediately.
7. If there is still no supported SKU after one informed retry, surface the error and ask the user for a preferred SKU or quota target.

## Workflow A: Browse the model catalog

1. Start with `model_catalog_list` using the user's term as a discovery keyword, not as proof that a single exact model is intended.
2. Optionally filter by:
   - `modelName`
   - `publisherName`
   - `licenseName`
   - `searchForFreePlayground`
3. If the user gave a family name, partial name, or ambiguous term, keep discovery in the catalog first:
   - run one or more additional `model_catalog_list` queries with nearby terms or narrower filters,
   - compare related variants returned by the catalog,
   - do not jump to `model_details_get` until the intended entry is clear.
4. Examples of ambiguity that require more catalog exploration first:
   - `gpt-5.4` may relate to `gpt-5.4` and `gpt-5.4-pro`
   - a family or publisher term may expand to multiple deployable models with different capabilities
5. If the user wants implementation detail for one model after discovery, follow with `model_details_get` for the chosen catalog entry.

## Workflow B: Inspect existing deployments

1. Resolve `foundryAccountResourceId`.
2. Call `model_deployment_get`:
   - without `deploymentName` to list all deployments,
   - with `deploymentName` to inspect one deployment.
3. If the user asks about health or future viability, continue into [operations.md](operations.md).

## Workflow C: Create or update a deployment

1. Resolve `foundryAccountResourceId`.
2. Resolve deployment inputs:
    - `deploymentName`
    - `modelName`
    - `modelFormat`
    - optional `modelVersion`, `modelSource`, `skuName`, `skuCapacity`, `scaleType`, `scaleCapacity`
3. If the user is unsure which model to deploy, use `model_catalog_list` first and widen or refine the catalog search until the intended variant is clear. Use `model_details_get` only after selecting the specific model entry.
4. Resolve `skuName` deliberately:
   - reuse explicit user input when present,
   - otherwise inspect comparable existing deployments in the same account with `model_deployment_get`,
   - prefer the SKU pattern already used by similar deployments, such as `GlobalStandard` for nearby OpenAI chat or responses deployments when that pattern is visible.
5. Call `model_deploy`.
6. If the deployment fails because the SKU is unsupported, make one informed retry with a better candidate derived from comparable deployments instead of repeating the same request.
7. Verify with `model_deployment_get` if the user needs confirmation.

## Workflow D: Delete a deployment

1. Resolve `foundryAccountResourceId` and `deploymentName`.
2. Verify existence with `model_deployment_get` if there is any ambiguity.
3. Call `model_deployment_delete`.

## Error Handling

| Error | Likely Cause | Response |
|-------|--------------|----------|
| Unknown deployment | Wrong deployment name or account | Re-check with `model_deployment_get` |
| Invalid deployment payload | Missing `modelFormat`, unsupported version, or bad SKU details | Surface the MCP error, correct the payload, and for unsupported-SKU cases retry once with a stronger SKU candidate derived from comparable deployments |
| Model ambiguity | User gave only a family name | Stay in `model_catalog_list`, try broader or adjacent catalog queries, compare the returned variants, then call `model_details_get` only for the selected model |

## Notes

- Treat `model_catalog_list` as discovery and `model_deploy` as mutation.
- For model families or partial names, prefer multiple catalog-list passes over a premature detail lookup.
- For new deployments, prefer explicit SKU resolution over relying on service defaults.
- Use existing deployments in the same account as the primary signal for likely supported SKU names.
- If the user wants operational advice after listing a deployment, switch to [operations.md](operations.md) instead of overloading this flow.
