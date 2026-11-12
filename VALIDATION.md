# Validation

Checked on November 12, 2026 on Windows with Codex CLI 0.166.0, Claude Code 2.1.309, Python 3.12, Pillow 10.4.0, and available pdflatex and pdftocairo executables.

## Installation

Using temporary CODEX_HOME and CLAUDE_CONFIG_DIR directories, registered the local marketplace and installed brainmaps@brainmaps in each CLI. Codex reported version 1.1.0 installed and enabled. Claude Code reported version 1.1.0 and discovered exactly one skill, brainmaps, with no agents, hooks, MCP servers, or LSP servers. Both Claude manifest and marketplace passed strict validation. The optional directory-listing check notes that no icon is supplied; public-directory submission was not performed.

The skill install checker passed. All 17 reference PNGs decoded successfully, all packaged Python files compiled, JSON files parsed, and local README links resolved. Installation does not prove execution in an authenticated agent conversation; no model-driven source-to-board session or graphical render review was performed.

## Included sample

Built the two supplied GRPO room files in an isolated temporary working directory using the actual builder and available equation-rendering tools. The output contained 1,126 elements, 49 images, 73 arrows, and unique element IDs. The subsequent audit exited 1: it reported 59 notes with long lines, 42 wide notes, one text element below 14px, one overlapping note pair, and too few worked-calculation notes for its threshold (31 detected).

These are limitations of the supplied example content and layout, not installation failures. The sample needs editing and visual review before it should be presented as a polished final board. README screenshots are pre-existing gallery references, not a claimed fresh render of this sample.
