# Roslyn: Semantic Code Understanding

[Back to README](../README.md)

> Roslyn is Microsoft's open-source compiler platform for C# and Visual Basic. This section is specific to .NET codebases, but the principle is universal: **every language needs a semantic analysis layer that AI agents can use to understand code meaning, not just text.** Python has `ast` and `mypy`. TypeScript has the compiler API. Rust has `syn` and `rust-analyzer`. None of them are as mature or as deeply integrated as Roslyn. **This is the single biggest gap in AI-assisted development today.** Until every major language has a Roslyn-equivalent, agents will keep making semantic mistakes that compile clean but fail silently at runtime.

---

## Why Text is Not Enough

LDF v1 enforces at the text level: "you changed a Tier A file, update the docs or the commit is blocked." That works. But an agent can bump the doc version, decide to disobey, go around the invariant, or just ignore it.

Grep finds strings. Roslyn sees the lifeblood flowing through the codebase.

Grep tells you a function name appears in 12 files. Roslyn tells you which 8 are real callers, which 3 are dead code, and which 1 is a comment.

---

## What This Looks Like in Practice

We develop **DAWG Beatcraft** ([dawgtools.org](https://dawgtools.org) | [itch.io](https://dawg-tools.itch.io/)), a Unity project: 406,000 lines of C#, 51 assemblies, real-time audio DSP, multiplayer networking, MIDI integration, and a complex UI layer. Roslyn is essential infrastructure for AI-assisted development at this scale.

**DSP flow verification:** Our audio pipeline processes samples on the audio thread with strict rules: no allocations, no main-thread calls, specific processing order. Roslyn scans method bodies in the DSP assembly and instantly detects violations that would compile fine but produce audio glitches or crashes at runtime. When an AI agent writes DSP code, Roslyn catches wrong argument ordering in reflection calls, identifies math operations where the precise function is actually faster than the approximated version, and verifies that filter coefficients are identical across mono and stereo paths.

**Real story: the rogue frequency.** We spent a week chasing a rogue frequency in the audio output. Traditional debugging (grep, breakpoints, reading code) could not find the source. Roslyn traced the actual signal flow through the DSP graph and instantly showed that a wet signal was being fed into the wrong buffer, which cascaded into multiple downstream effects. A week of manual diagnosis versus seconds of semantic analysis.

**Dead code detection:** In a 400k line codebase, knowing what is alive and what is dead is crucial. Roslyn traces actual call chains and type references through the full graph. When we remove a public method, Roslyn verifies every caller first, including indirect references through interfaces, generics, and reflection. Three separate times an AI agent claimed something was "unused" based on grep. Three separate times it broke callers that grep could not see.

**Architecture boundary enforcement:** With hexagonal architecture, the most important rule is that domain code never references platform code. Roslyn verifies this at the type level, inside method bodies, not just at the `using` statement level. It catches agents who write `UnityEngine.Debug.Log()` with a fully qualified name to bypass the using-guard.

**Silent runtime bugs:** Roslyn caught a reflection call with arguments in the wrong order. It found that an advanced math operation was both faster and 15% more precise than the approximation an AI agent substituted. These bugs compile clean but fail in production.

---

## What Roslyn Enables vs Text

| What text-level tools see | What Roslyn sees |
|------|------|
| "File X was modified" | "File X now references a type from a forbidden namespace" |
| "Invariant doc wasn't updated" | "The invariant itself is violated in the code" |
| "Tier A file changed" | "This change affects 47 downstream files; here's the blast radius" |
| Manual tier classification | Automatic tier inference from coupling metrics |
| Namespace-level boundary checks | Method-body-level verification |
| "This function name appears in N files" | "This function has N real callers and M dead references" |

---

## Architecture Rule Enforcement

Define rules in a simple JSON file:

```json
{
  "rules": [
    { "source": "MyApp.Domain", "must_not_reference": "MyApp.Infrastructure" },
    { "source": "MyApp.Core", "must_not_reference": "UnityEngine" }
  ]
}
```

Roslyn validates every edge in the dependency graph. Violations flagged with source file, target file, and the exact rule broken.

---

## Automatic Tier Detection

Instead of manually classifying every file:

```
1. Assembly has noEngineReferences: true  -> Pure
2. Assembly has Editor-only platforms     -> Tooling
3. File contains only interfaces          -> Boundary
4. File references no platform types      -> Boundary
5. File inherits MonoBehaviour            -> Runtime
6. Default                                -> Runtime
```

Assembly-level detection is authoritative. File-level detection is heuristic for assemblies without explicit flags.

---

## Coupling Metrics

Fan-in (how many nodes depend on this), fan-out (how many this depends on), instability (Ce / (Ca + Ce)). Computed from the real dependency graph, not from text matches. Stable nodes should be abstract. Unstable nodes should be concrete. Roslyn measures this directly, across the entire codebase, in seconds.

---

## The Key Insight

Roslyn turns documentation enforcement from reactive ("you changed a file, update the docs") into proactive ("your change violates this specific constraint, here's the proof").

Combined with hexagonal architecture, Roslyn can automatically:

- Classify tiers from coupling metrics instead of manual tagging
- Detect boundary violations at the type level, not just the namespace level
- Compute blast radius so you know which doc-sets need updating when a port interface changes
- Find stale invariants that reference code paths that no longer exist
- Show you the actual lifeblood of the codebase: what is alive, what is dead, what is critical, what is drifting

**LDF provides the structure. Architecture provides the boundaries. Roslyn provides the semantic verification.**
