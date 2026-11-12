# Install BrainMaps

## Local plugin

Follow the commands in [README.md](README.md), replacing `ButWhySo/BrainMaps` with `./` when registering a local checkout. On Windows PowerShell, use `claude.cmd` if execution policy blocks the `claude.ps1` launcher. Start a new agent session after installation.

## Standalone skill

Copy the complete `skills/brainmaps/` directory into `~/.agents/skills/brainmaps/` for Codex or `~/.claude/skills/brainmaps/` for Claude Code. Preserve scripts, examples, requirements, and the gallery. Install Pillow in your agent's Python environment and run the copied `scripts/check_install.py` with that interpreter.

Invoke the standalone skill with `$brainmaps` in Codex or `/brainmaps` in Claude Code. The plugin-installed Claude skill instead uses `/brainmaps:brainmaps`. Choose either plugin or standalone installation to avoid duplicate discovery.

## Verify a checkout

```sh
python -m pip install -r requirements.txt
python skills/brainmaps/scripts/check_install.py
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## Build the sample

The sample covers GRPO, a reinforcement-learning training method, and problems addressed by related methods. Run from a separate working directory because the builder writes a formula cache to its current directory. In the following commands, replace `/absolute/path/to/BrainMaps` with your checkout path and use an empty working directory:

```sh
python /absolute/path/to/BrainMaps/skills/brainmaps/scripts/build_board.py /absolute/path/to/BrainMaps/skills/brainmaps/examples demo.excalidraw --figs /absolute/path/to/BrainMaps/skills/brainmaps/examples/figs --cols 2
python /absolute/path/to/BrainMaps/skills/brainmaps/scripts/audit_board.py demo.excalidraw
```

Open `demo.excalidraw` in Excalidraw. The audit checks selected structural and content problems; visual inspection is still needed to judge layout and readability. Successful installation does not prove a skill has loaded in an existing conversation.
