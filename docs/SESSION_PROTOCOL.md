# Session Start Protocol

Version sync protocol for AI-assisted workflows. Used in production on Nebulae; extracted and documented here.

## Why This Matters

AI sessions are stateless. Without sync verification:
- Claude might work on stale code
- Changes could conflict with latest version
- User has no visibility into what Claude is based on

This protocol ensures the AI always starts from the correct codebase state and reports it.

## The Mandatory Checkpoint

Add this to your `CLAUDE.md` or project context file:

```
MANDATORY SYNC CHECKPOINT

Claude MUST output this EXACT line as the FIRST thing in EVERY session:

  SYNCED: Based on [branch-name] at v[X.XXX]. Ready to continue.

If Claude does NOT output this line FIRST:
- STOP Claude immediately
- Say: "You did not sync. Run the sync protocol NOW."
```

## Session Start Commands

### Step 1: Find Latest Version

**Bash:**
```bash
git fetch --all
for branch in origin/main $(git for-each-ref --sort=-committerdate refs/remotes/origin/claude/ --format='%(refname:short)' | head -5); do
  version=$(git show "$branch:CHANGELOG.md" 2>/dev/null | grep -m1 "^## \[" | sed 's/## \[\([^]]*\)\].*/\1/')
  [ -n "$version" ] && echo "$branch -> v$version"
done
```

**PowerShell:**
```powershell
git fetch --all
$branches = @('origin/main') + (git for-each-ref --sort=-committerdate refs/remotes/origin/claude/ --format='%(refname:short)' | Select-Object -First 5)
foreach ($branch in $branches) {
    $version = (git show "${branch}:CHANGELOG.md" 2>$null | Select-String "^## \[" -List | Select-Object -First 1) -replace '## \[([^\]]+)\].*','$1'
    if ($version) { Write-Host "$branch -> v$version" }
}
```

### Step 2: Base on Highest Version

**If on main:**
```bash
git fetch origin main && git merge origin/main
```

**If on claude/* branch:**
```bash
git fetch origin claude/feature-ABC && git reset --hard origin/claude/feature-ABC
```

### Step 3: Report

Output this line:
```
SYNCED: Based on [branch-name] at v0.XXX. Ready to continue.
```

## Version Loading Protocol

When user says "load v0.X.Y":

**Bash/PowerShell:**
```bash
git fetch origin --tags          # ALWAYS fetch tags FIRST
git tag -l "v0.X.Y"              # VERIFY tag exists (if empty, ASK USER)
git reset --hard v0.X.Y          # Reset to exact version
git log --oneline -1             # Show current commit
```

**NEVER assume a version doesn't exist. ALWAYS fetch first.**

## Branch Base Verification

**NEVER switch to existing branch without checking its base!**

**Bash:**
```bash
git fetch origin --tags
LATEST=$(git tag -l "v0.*" | sort -V | tail -1)
git log --oneline claude/some-branch -1  # Check branch base
# If wrong base:
git checkout $LATEST
git branch -D claude/some-branch
git checkout -b claude/some-branch
```

**PowerShell:**
```powershell
git fetch origin --tags
$LATEST = git tag -l "v0.*" | Sort-Object -Property {[version]$_} | Select-Object -Last 1
git log --oneline claude/some-branch -1
# If wrong base:
git checkout $LATEST
git branch -D claude/some-branch
git checkout -b claude/some-branch
```

**A fresh branch takes 5 seconds. Fixing wrong-base takes 10+ minutes.**

## Status

This protocol is production-tested:

| Feature | Status | Notes |
|---------|--------|-------|
| Session start/resume | Production | Used in Nebulae |
| Session end/save | Production | Used in Nebulae |
| Version tracking | Production | Used in Nebulae |

## Integration

1. Add the checkpoint text to your `CLAUDE.md`
2. AI must output the sync line before any other action
3. User verifies version is correct before proceeding
4. If wrong version, stop immediately and re-sync

## Why This Works

- **User visibility**: You see the version immediately
- **Fast abort**: Wrong version? Stop before any work done
- **Git-backed**: Truth comes from git, not AI memory
- **Session-resistant**: Works across session boundaries

## Related

- [Agent Protocol](../protocols/AGENT_PROTOCOL.md) — Full agent compliance rules
- [Integration Guide](INTEGRATION.md) — Framework setup
