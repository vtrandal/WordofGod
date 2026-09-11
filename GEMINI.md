# Project Rules: Word of God

These rules apply to all AI agents (Antigravity CLI, Gemini, etc.) operating in this repository.

## 1. Git State Management & Discipline
* **Pre-Flight Verification**: Always verify `git status` at the start of a session. Never start multi-file edits on a dirty working tree without alerting the user or stashing loose work.
* **Sandbox Branching for Multi-Step Features**: For non-trivial features, refactors, or new components, prefer creating an isolated disposable branch (e.g. `agy/<task-name>`) to protect the `main` branch.
* **Preserve Trunk (`main`) Stability**: The `main` branch automatically deploys to live GitHub Pages (`https://vtrandal.github.io/WordofGod/`). Only verified, syntax-clean code should be merged and pushed to `main`.
* **Zero Secret Leaks**: The `.env` file contains GitHub credentials and must NEVER be staged, committed, or pushed. Ensure it remains in `.gitignore`.
* **Safe Cleanup**: Never run `git clean -fd` blindly without checking untracked files with `git status` first, so user-created scratch files or notes are not accidentally destroyed.

## 2. Architecture & Pipeline Consistency
* **Preserve Multi-Format Synergy**:
  * Local edition: `Master_Index.pdf` (relative `/GoToR` links to `books/*.pdf`).
  * Cloud edition: `Master_Index_Cloud.pdf` (high-speed CDN links returning `Content-Type: application/pdf`).
  * PWA Web reader: `index.html`, `manifest.json`, `sw.js`, `icons/`.
* **Rebuild Orchestration**: Whenever metadata or book links change, run `python3 generate_indexes.py` to keep all index files synchronized.
* **Service Worker Caching**: Whenever `index.html` or core assets are modified, bump the cache version in `sw.js` (e.g., `word-of-god-shell-vX`) so mobile devices invalidate their local cache and fetch the latest build.
* **Documentation Currency**: Keep `IDEAS.md`, `README.md`, and `Design_Document.tex` updated to reflect new implementations or architectural lessons learned.
