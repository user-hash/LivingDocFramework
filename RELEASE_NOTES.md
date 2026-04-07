# Release Notes

## v2.0.0 — LDF v2

**Date**: 2026-04-07
**Status**: Active development

LDF v2 is a ground-up repositioning. The framework is no longer about hooks and commit blocking. It is a methodology for building well-architected codebases with AI assistance.

### What changed

**New core ideas:**
- Hexagonal architecture as the structural foundation
- Pure assemblies with compiler-enforced boundaries
- Invariant-driven development (INV-xxx codes)
- Framework over hardcoding
- AI instruction files (CLAUDE.md)
- Ratchet testing
- Intentional knowledge hardening (not mandatory on every change)

**Roslyn section:**
- Major new section on semantic code understanding for C#/.NET
- Why text-level tools are not enough for complex codebases
- Real examples from a 400k LOC Unity project
- Call to action: every language needs a Roslyn equivalent

**Dual-AI workflow:**
- Code agent (embedded, full codebase access) + Chat agent (disconnected, broad perspective)
- Clear role separation: human decides, code agent executes, chat agent thinks

**Human/AI roles:**
- AI agents maintain docs, humans architect
- Addresses the most common question about LDF

**Anonymized production tree:**
- Full doc structure from a real project: 76 invariants, 18 invariant files, 10 bug pattern files, 11 code maps, 23 architecture docs

**Cleanup:**
- Removed dead files (empty post-commit hook, unused requirements.txt, legacy examples)
- Updated all docs to match new direction
- Removed stale roadmap items and "coming soon" stubs

### Numbers from the project that proved this methodology

- 1,718 C# files, 406,000+ lines of code
- 51 assemblies, 13 pure (zero engine references)
- 76 invariant codes across 35 scopes
- Built by a solo developer with AI assistance over 5 months

---

## v0.2.0

See [CHANGELOG.md](CHANGELOG.md) for earlier versions.
