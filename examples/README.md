# Living Documentation Framework - Examples

Example projects showing how to integrate the framework with different languages and tech stacks.

## Available Examples

### python-project/
**Language**: Python
**Framework**: Any (Django, Flask, FastAPI)
**Features**:
- Complete living-doc-config.yaml
- pytest integration
- API subsystem example
- Database tier A examples

**Quick Start**:
```bash
cd examples/python-project
./../../hooks/install.sh
python ../../tools/calculate_confidence.py
```

## Creating Your Own Example

1. **Copy template**:
   ```bash
   cp -r examples/python-project examples/my-project
   cd examples/my-project
   ```

2. **Edit config**:
   ```yaml
   # living-doc-config.yaml
   project:
     name: "My Project"
     language: "javascript"  # or go, rust, etc.
   ```

3. **Initialize docs**:
   ```bash
   mkdir -p docs
   touch CHANGELOG.md BUG_TRACKER.md BUG_PATTERNS.md
   # etc.
   ```

4. **Install hooks**:
   ```bash
   ../../hooks/install.sh
   ```

## Example Projects To Add

### JavaScript/TypeScript
- React frontend
- Node.js backend
- Next.js fullstack

### Go
- Microservice with gRPC
- CLI tool
- Web API

### Rust
- Systems programming
- WebAssembly
- Actix-web API

### C#/Unity
- Game project (Nebulae-style)
- ASP.NET Core API
- Desktop application

## Contributing Examples

To contribute an example:

1. Create directory: `examples/your-project-name/`
2. Add `living-doc-config.yaml`
3. Add `README.md` with setup instructions
4. Include minimal code structure
5. Document integration points
6. Test hooks work correctly

Submit PR with:
- Example code
- Configuration
- README
- Integration tests
