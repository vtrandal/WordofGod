# Contributing & Git Workflow Discipline

This document defines the development workflow, branching strategy, and recovery procedures for the **Word of God** project. 

Whether you are a human developer or an autonomous AI agent (such as Google Antigravity / Gemini CLI), adhering to these guidelines ensures repository stability, deterministic rollbacks, and zero corruption of production code.

---

## 1. Branching Strategy: Trunk-Based Development

We follow a **Trunk-Based Development** model with short-lived, disposable feature branches.

* **`main` (Trunk)**:
  * Represents production-ready, verified code.
  * Deploys automatically to the live Progressive Web App (PWA) at [https://vtrandal.github.io/WordofGod/](https://vtrandal.github.io/WordofGod/).
  * Direct, unverified edits to `main` are discouraged.
* **Feature & Agent Branches (`agy/<task-name>` or `feature/<task-name>`)**:
  * All non-trivial modifications, refactors, and automated agent sessions must run inside dedicated sandbox branches.
  * If a session is interrupted (due to a power loss, VM reboot, or network failure), `main` remains 100% clean and operational.

---

## 2. Standard Operating Procedure (SOP) Lifecycle

### Stage 1: Pre-Flight (Ensure a Pristine Baseline)
Before starting any new task or agent session, verify that your working directory is clean:

```bash
git checkout main
git pull origin main
git status    # Must report: "nothing to commit, working tree clean"
```

If you have uncommitted changes or loose files:
```bash
git stash -u  # Safely stashes uncommitted and untracked files
```

### Stage 2: Branch & Execute
Create and switch to an isolated branch:

```bash
# Modern syntax (Git 2.23+):
git switch -c agy/task-name

# Or classic syntax:
git checkout -b agy/task-name
```

Perform the work, run verification builds, and test on local browsers or mobile devices.

### Stage 3: Post-Session Triage

#### Scenario A: The Task Failed, Was Interrupted, or Corrupted
Do not waste time manually auditing partial edits. Use the **One-Command Recovery Hatch** to instantly reset the branch to the exact byte-level state of the baseline commit:

```bash
# 1. Preview what untracked files would be deleted (safety dry-run):
git clean -nd

# 2. Reset tracked files and purge newly created artifacts:
git reset --hard HEAD
git clean -fd
```

To abandon the attempt completely and delete the sandbox branch:
```bash
git switch main
git branch -D agy/task-name
```

#### Scenario B: The Task Succeeded & Passed Verification
Audit changes, commit them with a descriptive message, and integrate into `main`:

```bash
git diff
git add -A
git commit -m "feat(module): descriptive summary of changes"

# Switch to main and merge
git switch main
git merge agy/task-name
git branch -d agy/task-name
```

---

## 3. Releases & Version Tagging Policy

* **Branches Look Forward**: Branches are ephemeral, disposable workspaces for in-flight or exploratory work.
* **Tags Look Backward**: Git tags (e.g. `v1.0.0-pwa`, `v1.1.0`) are immutable milestones created **only after** work is completed, verified, and merged into `main`. Never create tags before starting unverified experimental work.

To create an official milestone release tag:
```bash
git tag -a v1.0.0-pwa -m "Milestone release: Working 67-book PDFs and PWA Audio Reader"
git push origin v1.0.0-pwa
```

---

## 4. Build Pipeline & Consistency Verification

Any change affecting PDFs, bookshelf metadata, or PWA reading features must maintain pipeline consistency:

1. **Rebuild Orchestrator**:
   ```bash
   python3 generate_indexes.py
   ```
   Ensures that `Master_Index.pdf`, `Master_Index_Cloud.pdf`, and `index.html` remain perfectly synchronized.

2. **Design Document Compilation**:
   ```bash
   pdflatex -interaction=nonstopmode Design_Document.tex
   ```
   Ensures that architectural specifications in `Design_Document.pdf` stay current with production code.
