# skill-foundry-mcp-server

An agent skill for working with the [Foundry MCP Server](https://learn.microsoft.com/azure/foundry/mcp/get-started?view=foundry&tabs=user).

## Why

**Microsoft Foundry** (Azure AI Foundry) is Azure's platform for building, deploying, and managing AI agents and models. The **Foundry MCP Server** exposes Foundry's capabilities through the Model Context Protocol, enabling programmatic access to:

- **Agents**: Create, deploy, invoke, and manage hosted/prompt agents
- **Models**: Browse catalogs, deploy models, monitor usage, check quotas
- **Evaluations**: Run batch evaluations, compare results, manage datasets
- **Project connections**: Configure datastores and external connections
- **Prompt optimization**: Iteratively improve system prompts

**This skill** orchestrates MCP workflows so you can manage Foundry resources conversationally through Copilot, instead of manually constructing API calls or navigating the Azure portal.

## Installation

**Copy to skills directory:**

Linux/macOS:
```bash
mkdir -p ~/.agents/skills
cp -R ./foundry-mcp-skill ~/.agents/skills/foundry-mcp-skill
```

Windows (PowerShell):
```powershell
mkdir -Force $HOME\.agents\skills
Copy-Item -Recurse .\foundry-mcp-skill $HOME\.agents\skills\foundry-mcp-skill
```

**Symlink instead of copy:**

Linux/macOS:
```bash
ln -s "$(pwd)/foundry-mcp-skill" ~/.agents/skills/foundry-mcp-skill
```

Windows (PowerShell):
```powershell
New-Item -ItemType SymbolicLink -Path $HOME\.agents\skills\foundry-mcp-skill -Target (Resolve-Path ".\foundry-mcp-skill")
```

## Confirm skill

**GitHub Copilot CLI:**

After installation, manually add the skill in Copilot Chat:

```
/skills add ~/.agents/skills/foundry-mcp-skill
```

**Opencode:**

Skills are auto-detected from `~/.agents/skills/` - no manual activation needed.

## Use

Try these example prompts:

- `Use foundry-mcp-skill to list agents in my Foundry project https://myaccount.services.ai.azure.com/api/projects/myproject`
- `Use foundry-mcp-skill to find the latest models in the Foundry model catalog`

For more examples and available tools, see the [Foundry MCP Server documentation](https://learn.microsoft.com/en-us/azure/foundry/mcp/available-tools?view=foundry).

## Troubleshooting

**Copilot CLI:** If skill doesn't appear after `/skills add`, restart Copilot CLI and try again.

**Opencode:** If skill isn't recognized, confirm the path is `~/.agents/skills/foundry-mcp-skill` and restart Opencode.

## Repository contents

- `foundry-mcp-skill/SKILL.md` — top-level workflow skill
- `foundry-mcp-skill/agents/` — agent workflows
- `foundry-mcp-skill/models/` — model workflows
- `foundry-mcp-skill/evaluations/` — evaluation workflows
- `foundry-mcp-skill/project-connections/` — project connection workflows
- `foundry-mcp-skill/prompt-optimizer/` — prompt optimizer workflow
- `foundry-mcp-skill/manual-auth.md` — bearer-token fallback guidance
- `foundry-mcp-skill/scripts/manual_mcp_client.py` — manual MCP client helper
