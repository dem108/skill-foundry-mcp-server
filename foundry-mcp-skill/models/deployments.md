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
4. Call `model_deploy`.
5. Verify with `model_deployment_get` if the user needs confirmation.

## Workflow D: Delete a deployment

1. Resolve `foundryAccountResourceId` and `deploymentName`.
2. Verify existence with `model_deployment_get` if there is any ambiguity.
3. Call `model_deployment_delete`.

## Error Handling

| Error | Likely Cause | Response |
|-------|--------------|----------|
| Unknown deployment | Wrong deployment name or account | Re-check with `model_deployment_get` |
| Invalid deployment payload | Missing `modelFormat`, unsupported version, or bad SKU details | Surface the MCP error and correct the requested inputs |
| Model ambiguity | User gave only a family name | Stay in `model_catalog_list`, try broader or adjacent catalog queries, compare the returned variants, then call `model_details_get` only for the selected model |

## Notes

- Treat `model_catalog_list` as discovery and `model_deploy` as mutation.
- For model families or partial names, prefer multiple catalog-list passes over a premature detail lookup.
- If the user wants operational advice after listing a deployment, switch to [operations.md](operations.md) instead of overloading this flow.
