# Manual Entra Token Fallback for Foundry MCP Server

Use this workflow when the user's MCP client cannot complete the normal OAuth DCR flow against the Foundry MCP Server.

Typical cases:
- non-Copilot environments
- custom MCP clients
- client-side OAuth DCR issues in tools such as Opencode

This is a fallback path, not the preferred default over a working OAuth flow.

## What this gives you

- an Entra access token for `https://mcp.ai.azure.com`
- a way to send that token as `Authorization: Bearer ...`
- a reusable script at `scripts/manual_mcp_client.py`
- a way to list tools, call Foundry MCP tools, and send an `agent_invoke` message through the server

## Required Inputs

| Variable | Purpose |
|----------|---------|
| `FOUNDRY_MCP_SERVER_URL` | Optional MCP endpoint URL. Defaults to `https://mcp.ai.azure.com` |
| `FOUNDRY_MCP_BEARER_TOKEN` | Optional bearer token. If unset, the script acquires one through Azure CLI |
| `FOUNDRY_PROJECT_ENDPOINT` | Needed only if you want to call `agent_invoke` |
| `FOUNDRY_AGENT_NAME` | Needed only if you want to call `agent_invoke` |

> The default Foundry MCP Server endpoint is `https://mcp.ai.azure.com`. `FOUNDRY_MCP_SERVER_URL` is the MCP server endpoint, not the same thing as `projectEndpoint`.

## Step 1: Prepare the environment

Sign in to Azure CLI if needed with `az login`.

Install the Python client dependencies with `pip install mcp httpx`.

The fallback script lives at `foundry-mcp-skill/scripts/manual_mcp_client.py`.

## Step 2: Use the script

By default the script uses `https://mcp.ai.azure.com`. Set `FOUNDRY_MCP_SERVER_URL` only if you need to override that endpoint.

Then run `python scripts/manual_mcp_client.py --list-tools` to verify that:
- the script can acquire a token with `az account get-access-token --resource https://mcp.ai.azure.com`
- the bearer token is accepted by the MCP server
- the transport is working

To query the model catalog, run `python scripts/manual_mcp_client.py --tool model_catalog_list --arguments '{"modelName":"gpt-5.4"}'`.

## Step 3: Send and receive a message through `agent_invoke`

Set `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_AGENT_NAME`, then call `scripts/manual_mcp_client.py` with `--tool agent_invoke` and an `--arguments` JSON object containing `projectEndpoint`, `agentName`, and `inputText`.

Reuse the returned `conversationId` and `sessionId` values if you want to continue the same conversation, following the normal guidance in [agents/invoke.md](agents/invoke.md).

## Troubleshooting

- If you already have a token, export `FOUNDRY_MCP_BEARER_TOKEN`; otherwise the script acquires one automatically with Azure CLI.
- If the client gets unauthorized responses, refresh the token and retry.
- If the client can connect but a tool call fails, surface the actual MCP error instead of assuming it is an auth failure.
- If `agent_invoke` fails, verify `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_AGENT_NAME` separately from the MCP server URL.
- If you need to inspect or adapt the client behavior, edit `scripts/manual_mcp_client.py` instead of embedding custom source in the Markdown docs.

## Guardrails

- Treat this as a fallback for broken or unavailable OAuth DCR support.
- Keep the bearer token in memory or an environment variable; avoid writing it to disk.
- Do not confuse transport authentication to the MCP server with Foundry workflow identifiers like `projectEndpoint`.
