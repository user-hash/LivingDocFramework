# Workflow: Human + Two AI Agents

[Back to README](../README.md)

---

## Who Does What

AI agents maintain the docs. The human architects. Here is how we split the work.

### The Human

You are the architect. You decide:

- When to harden knowledge (not every commit, only when it matters)
- What the invariants are (the AI writes them down, you identify the rule)
- Architecture direction (what goes where, which boundaries to enforce)
- When to override the AI (escape hatches exist for a reason)
- What to feed to the chat agent for a second opinion

You do not manually update CHANGELOG, CODE_DOC_MAP, or BUG_PATTERNS on every change. That is what the code agent is for.

### The Code Agent (embedded)

Your AI coding tool with full codebase access. File system, git, terminal, Roslyn, MCP tools. It lives inside the codebase.

What it does:

- Reads CLAUDE.md and respects invariants before writing code
- Maintains CHANGELOG entries when committing
- Updates CODE_DOC_MAP when files are created or renamed
- Writes bug pattern entries after fixing bugs (when you say it is worth documenting)
- Runs Roslyn verification to check boundary violations
- Executes ratchet tests
- Loads context via print-context.sh before editing

Deep context, narrow perspective. Sees every line of code but can get tunnel vision.

### The Chat Agent (disconnected)

A separate AI, ideally from a different provider. No terminal, no git, no file system access. Just a chat window. You upload or paste the codebase (or parts of it) at the start of each conversation.

It knows your codebase. But it gets a fresh copy every time. No memory from yesterday, no accumulated assumptions, no "I already looked at this." Every conversation starts from zero with the current state of the code.

What it does:

- Broad architectural review ("here is our assembly map, does this make sense?")
- Spots holes the code agent misses ("you have 13 pure assemblies but Math depends on nothing, is that intentional?")
- Challenges assumptions ("why is this a port and not a direct dependency?")
- Offers design alternatives ("three ways to structure this, here are the tradeoffs")
- Sanity checks invariants ("INV-DSP-003 says audio-thread-only, but what about the preview path?")

### Why Two Agents, Two Providers

A single AI develops blind spots. A disconnected chat agent from a different provider brings:

- **Different training biases.** What one model overlooks, another catches.
- **Forced context compression.** You have to explain the architecture to feed it. That forces you to clarify your own thinking.
- **No codebase anchoring.** It judges the design on its merits, not on what is already there.
- **Cheap second opinions.** A 5-minute chat conversation can save hours of wrong-direction work.

In practice our workflow looks like this:

```
1. Human identifies a problem or decision
2. Chat agent discusses architecture, tradeoffs, approach
3. Human decides direction
4. Code agent implements with full codebase context
5. Code agent maintains docs as it works
6. Human reviews and decides what to harden
```

Zip the codebase and feed it to the chat. Ours fits in one conversation. Or just feed it a specific question and the relevant files.

**The code agent executes. The chat agent thinks. The human decides.**

---

## Intentional Knowledge Hardening

LDF is not forced on every commit. You activate it when you need it:

- **Tighten architecture when the work is done.** After a subsystem stabilizes, lock in what you learned. Write the invariants. Map the files. Record the decisions.
- **Use it to solve a problem.** Chasing a bug for a week? Document the signal flow, write the invariant that prevents recurrence, add a bug pattern.
- **Refresh when you have a decision.** Made a meaningful architectural choice? Record it while the reasoning is fresh.
- **Granular hexagonal architecture as you need it.** Extract one port, one adapter, one pure assembly. When that works, do another.

When you decide to capture knowledge, the structure is already there. You know where to put it.

**Update docs when you need to, when you have a hard crack to solve, when you are happy with the results. Not always. Only when it matters.**
