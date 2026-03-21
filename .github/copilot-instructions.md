# Copilot instructions

## Commands

This repository does not define build, lint, or automated test scripts. The concrete commands used to validate changes are the documented install and smoke-test flows:

- Install the skill locally: `mkdir -p ~/.agents/skills && cp -R ./foundry-mcp-skill ~/.agents/skills/foundry-mcp-skill`
- Symlink the skill during iteration: `ln -s "$(pwd)/foundry-mcp-skill" ~/.agents/skills/foundry-mcp-skill`
- Register the skill in GitHub Copilot CLI: `/skills add ~/.agents/skills/foundry-mcp-skill`
- From `foundry-mcp-skill/`, install the manual auth client dependencies: `pip install mcp httpx`
- From `foundry-mcp-skill/`, smoke-test the transport: `python scripts/manual_mcp_client.py --list-tools`
- From `foundry-mcp-skill/`, smoke-test a single tool call: `python scripts/manual_mcp_client.py --tool model_catalog_list --arguments '{"modelName":"gpt-5.4"}'`
- From `foundry-mcp-skill/`, smoke-test a single agent invocation: `python scripts/manual_mcp_client.py --tool agent_invoke --arguments '{"projectEndpoint":"...","agentName":"...","inputText":"..."}'`

## High-level architecture

- `README.md` covers installation, activation, troubleshooting, and the repo layout.
- `foundry-mcp-skill/SKILL.md` is the top-level router. It maps user intents to narrower workflow docs and defines the shared identifier-resolution rules used across the repository.
- The domain folders split the skill into workflow families:
  - `agents/` for agent create/update/clone/delete, hosted-container control, and invocation flows
  - `models/` for model catalog discovery, deployment CRUD, and account-scoped operations such as quota, monitoring, deprecation, and benchmarks
  - `evaluations/` for dataset/evaluator preparation and evaluation run/comparison workflows
  - `project-connections/` for project connection metadata discovery and CRUD
  - `prompt-optimizer/` for prompt refinement against a known deployment
- Each domain has a `SKILL.md` that routes into narrower leaf workflow docs such as `agents/manage.md`, `agents/invoke.md`, `models/deployments.md`, or `evaluations/runs-and-comparisons.md`. Those leaf docs contain the actual step order, required inputs, and guardrails.
- `manual-auth.md` plus `scripts/manual_mcp_client.py` provide the bearer-token fallback path when MCP OAuth DCR fails.
- `.vscode/mcp.json` already points the workspace at the global Foundry MCP endpoint, `https://mcp.ai.azure.com`.

## Key conventions

- Treat this repository as documentation-first. When behavior changes, update the relevant workflow Markdown and any routing tables that reference it.
- Preserve the YAML frontmatter pattern in every `SKILL.md` (`name` and `description`), because skill routing depends on it.
- Always read the most specific workflow doc before acting. The top-level skill routes into domain `SKILL.md` files, and those route again into the leaf workflows.
- Keep the MCP-first approach: prefer remote Foundry MCP tools over Azure CLI or SDK fallbacks whenever the workflow is covered.
- Resolve identifiers in the documented order: user input, then session context, then inferred values. If a value is inferred, surface it and confirm it before a blocking or mutating step.
- Keep scope types separate: `projectEndpoint` for agents, evaluations, and prompt optimization; `foundryAccountResourceId` for models and model operations; `foundryProjectResourceId` for project connections.
- Follow the documented read-before-mutate flow. Typical examples are `agent_definition_schema_get` before `agent_update`, `agent_get` before `agent_delete`, and `project_connection_list` or `project_connection_get` before connection mutations.
- Model discovery is intentionally multi-step: use `model_catalog_list` one or more times to narrow a family or partial name, and call `model_details_get` only after the exact target is clear.
- After creating or updating tool-using agents, run a realistic smoke test and verify that the expected tool usage appears in the invocation output.
- Preserve returned conversation state. Reuse `conversationId` for multi-turn agent chats and keep the same `sessionId` for sticky hosted-agent sessions.
- If OAuth DCR issues appear in a non-Copilot client, route to `manual-auth.md` instead of inventing a separate auth workflow.
- If you add or rename a workflow, keep all references in sync: the top-level `foundry-mcp-skill/SKILL.md`, the relevant domain `SKILL.md`, the leaf workflow doc, and any README examples or repository-content listings that mention it.
- If you change the manual bearer-token fallback, update both `manual-auth.md` and `scripts/manual_mcp_client.py`, and keep related references in `agents/invoke.md` aligned.
