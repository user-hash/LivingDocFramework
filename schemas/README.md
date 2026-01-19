# Schema Templates for Cognitive Graph

These JSON schema templates define the configuration for the semantic knowledge graph system. Copy them to your project's `.claude/devmemory/schema/` directory and customize for your codebase.

## Files

| Template | Purpose | Customize |
|----------|---------|-----------|
| `node-types.template.json` | Node type definitions | Add your entity types |
| `edge-types.template.json` | Edge type definitions | Add relationship types |
| `tiers.template.json` | File tier classifications | Add critical Tier A files |
| `categories.template.json` | System categories | Add your subsystems |
| `discovery-passes.template.json` | Discovery pass config | Enable/disable passes |
| `regex-patterns.template.json` | Regex patterns | Adjust for your conventions |

## Quick Start

1. Copy templates to your project:
   ```bash
   mkdir -p .claude/devmemory/schema
   cp schemas/*.template.json .claude/devmemory/schema/
   # Rename templates (remove .template suffix)
   for f in .claude/devmemory/schema/*.template.json; do
     mv "$f" "${f%.template.json}.json"
   done
   ```

2. Customize for your project:
   - Add your critical files to `tiers.json` Tier A
   - Add your subsystem patterns to `categories.json`
   - Adjust regex patterns for your naming conventions

3. Run graph discovery:
   ```bash
   python .claude/tools/devmemory/graph_builder.py discover
   ```

## Schema Details

### Node Types

Define what entities exist in your knowledge graph:
- `id`: Unique identifier used in code
- `label`: Human-readable display name
- `color`: Hex color for visualization
- `discovery.method`: How to find these nodes (`glob`, `json`, `markdown`, `parse`)
- `enabled`: Whether to discover this type

### Edge Types

Define relationships between entities:
- `id`: Unique identifier
- `label`: Display name
- `color`: Edge color in graph
- `discovery.method`: How to find these relationships

### Tiers

Risk classification for files:
- **Tier A**: Critical files requiring invariant citation before editing
- **Tier B**: Important files with moderate risk
- **Tier C**: Standard files (default)
- **Tier D**: Generated or rarely-touched files

Add file names to `files` array or glob patterns to `patterns` array.

### Categories

Organize code by subsystem:
- `path_patterns`: Regex patterns matching file paths
- `keywords`: Keywords in filename to match
- `is_default`: Fallback category for unmatched files

### Discovery Passes

Control the multi-pass discovery algorithm:
- `confidence`: How reliable this pass is (0.0-1.0)
- `enabled`: Whether to run this pass
- Higher ID passes run later, can override lower confidence findings

## Version

Schema templates v1.0.0 - Compatible with Living Doc Framework v1.1.0+
