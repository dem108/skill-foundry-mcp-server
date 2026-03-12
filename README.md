# foundry-mcp-skill

This repository contains a Copilot skill package, `foundry-mcp-skill`, for working with the Foundry MCP Remote server.

The skill source lives in this repo:

- `./foundry-mcp-skill/`

Install it into the skills directory used by your client:

- GitHub Copilot CLI: `~/.agents/skills/foundry-mcp-skill/`
- Opencode: `~/agents/skills/foundry-mcp-skill/`

## Default Usage Flow

The most reliable way to use this skill depends on the client:

### GitHub Copilot CLI

1. Install the skill into `~/.agents/skills/foundry-mcp-skill`
2. In Copilot Chat, manually add it with:

```text
/skills add ~/.agents/skills/foundry-mcp-skill
```

3. Run `/skills` to confirm `foundry-mcp-skill` is now available

Copilot CLI currently seems unreliable at auto-recognizing copied or symlinked skills under `~/.agents/skills`, so the manual `/skills add ...` step is the recommended path.

### Opencode

1. Install the skill into `~/agents/skills/foundry-mcp-skill`
2. Copying or symlinking the skill there is typically enough
3. Opencode should recognize the installed skill from that directory

## Recommended Layout

- Keep the version-controlled source in this repo.
- For GitHub Copilot CLI, copy or symlink that folder into `~/.agents/skills/`.
- For Opencode, copy or symlink that folder into `~/agents/skills/`.

## Option 1: Install by Copying

Use this if you want a standalone installed copy.

### Linux / macOS

#### GitHub Copilot CLI

```bash
mkdir -p ~/.agents/skills
cp -R ./foundry-mcp-skill ~/.agents/skills/foundry-mcp-skill
```

#### Opencode

```bash
mkdir -p ~/agents/skills
cp -R ./foundry-mcp-skill ~/agents/skills/foundry-mcp-skill
```

### Windows PowerShell

#### GitHub Copilot CLI

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
Copy-Item -Recurse -Force ".\foundry-mcp-skill" "$HOME/.agents/skills/foundry-mcp-skill"
```

#### Opencode

```powershell
New-Item -ItemType Directory -Force "$HOME/agents/skills" | Out-Null
Copy-Item -Recurse -Force ".\foundry-mcp-skill" "$HOME/agents/skills/foundry-mcp-skill"
```

## Option 2: Install by Symlink

Use this if you want changes in the repo to be reflected immediately in the installed skill.

### Linux / macOS

#### GitHub Copilot CLI

Run from the repository root:

```bash
mkdir -p ~/.agents/skills
ln -s "$(pwd)/foundry-mcp-skill" ~/.agents/skills/foundry-mcp-skill
```

If the link already exists, remove it first:

```bash
rm ~/.agents/skills/foundry-mcp-skill
ln -s "$(pwd)/foundry-mcp-skill" ~/.agents/skills/foundry-mcp-skill
```

#### Opencode

Run from the repository root:

```bash
mkdir -p ~/agents/skills
ln -s "$(pwd)/foundry-mcp-skill" ~/agents/skills/foundry-mcp-skill
```

If the link already exists, remove it first:

```bash
rm ~/agents/skills/foundry-mcp-skill
ln -s "$(pwd)/foundry-mcp-skill" ~/agents/skills/foundry-mcp-skill
```

### Windows PowerShell

#### GitHub Copilot CLI

Run from the repository root:

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
New-Item -ItemType SymbolicLink -Path "$HOME/.agents/skills/foundry-mcp-skill" -Target (Resolve-Path ".\foundry-mcp-skill")
```

If the link already exists, remove it first:

```powershell
Remove-Item "$HOME/.agents/skills/foundry-mcp-skill"
New-Item -ItemType SymbolicLink -Path "$HOME/.agents/skills/foundry-mcp-skill" -Target (Resolve-Path ".\foundry-mcp-skill")
```

#### Opencode

Run from the repository root:

```powershell
New-Item -ItemType Directory -Force "$HOME/agents/skills" | Out-Null
New-Item -ItemType SymbolicLink -Path "$HOME/agents/skills/foundry-mcp-skill" -Target (Resolve-Path ".\foundry-mcp-skill")
```

If the link already exists, remove it first:

```powershell
Remove-Item "$HOME/agents/skills/foundry-mcp-skill"
New-Item -ItemType SymbolicLink -Path "$HOME/agents/skills/foundry-mcp-skill" -Target (Resolve-Path ".\foundry-mcp-skill")
```

## Add and Verify the Skill

### GitHub Copilot CLI

After copying or symlinking the skill:

1. Start or restart Copilot CLI if needed.
2. In Copilot Chat, run:

```text
/skills add ~/.agents/skills/foundry-mcp-skill
```

3. Run `/skills`.
4. Confirm `foundry-mcp-skill` appears in the available skills list.

If it does not appear:

- confirm the installed path is exactly `~/.agents/skills/foundry-mcp-skill`
- confirm the installed folder contains `SKILL.md`
- rerun `/skills add ~/.agents/skills/foundry-mcp-skill`
- restart the CLI session

### Opencode

After copying or symlinking the skill:

1. Confirm the installed path is `~/agents/skills/foundry-mcp-skill`
2. Start or restart Opencode if needed
3. Confirm the skill is recognized from that directory

## Repository Contents

- `foundry-mcp-skill/SKILL.md` — top-level workflow skill
- `foundry-mcp-skill/agents/` — agent management and invocation docs
- `foundry-mcp-skill/models/` — model deployment and operations docs
- `foundry-mcp-skill/evaluations/` — dataset, evaluator, and evaluation run docs
- `foundry-mcp-skill/project-connections/` — project connection workflows
- `foundry-mcp-skill/prompt-optimizer/` — prompt optimization workflow
