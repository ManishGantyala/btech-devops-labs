# Experiment 03 – Practice Source Code Management on GitHub

## Aim

To practice source code management on GitHub by taking the real application built in Exercise 1 (the TechFest 2026 event registration form) through a feature branch → Pull Request → review → merge workflow.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain what a feature branch is for and why changes are made on one instead of directly on `main`.
- Create a branch, commit a change to real project source code, and push that branch to GitHub.
- Open a Pull Request on GitHub and review its diff before merging.
- Merge a Pull Request and bring the merged change back into the local repository.
- Verify, both locally and on GitHub, that a change was managed correctly from branch to merge.

This experiment assumes Git and GitHub basics — repositories, staging, commits, `push`/`pull`/`clone` — are already understood from Experiment 02. Those are not re-explained here; only referenced where needed.

## Requirements

- The Experiment 01 source code (`experiment-01/index.html`, `style.css`, `script.js`), already tracked in this repository and already pushed to GitHub.
- Git installed, and Git configured with a user name and email (Experiment 02, Section 2).
- A GitHub account with push access to this repository.
- A terminal or command prompt.

## Concept — What "Source Code Management" Means in This Experiment

Experiment 02 covered individual Git and GitHub commands using a disposable practice folder. This experiment is different: it applies those commands to the **real, existing application** from Exercise 1, in the sequence a change is normally managed on GitHub.

```text
main --(branch)--> feature branch --(edit, commit)--> pushed branch --(Pull Request)--> reviewed diff --(merge)--> main
                                                                                                                 |
                                                                                                          (pull locally)
```

Two ideas are central here:

- **Feature branch** — a change is developed on its own branch, not directly on `main`, so `main` always stays in a working state.
- **Pull Request (PR)** — GitHub's mechanism for proposing a branch's changes to be merged. A PR shows exactly which lines changed (the diff) and requires a deliberate merge action — it is not just `git push`. Reviewing that diff before merging, even alone, is the core habit this experiment teaches.

## Procedure

### Step 1 — Confirm the Starting State

**What:** Check that the local repository is on `main` and up to date with GitHub before starting any new work.

**Why:** Starting a feature branch from an outdated or dirty `main` can carry over unrelated changes or conflicts.

**Command:**

```bash
git switch main
git status
git pull origin main
```

**Observe:** `git status` reports a clean working tree, and `git pull` reports either the new commits it fetched or "Already up to date."

### Step 2 — Create a Feature Branch

**What:** Create a new branch off `main` to hold the upcoming change to the Exercise 1 source code.

**Why:** Isolating the change on its own branch keeps `main` — the working registration form — untouched until the change has been reviewed and merged.

**Command:**

```bash
git switch -c update-registration-form
```

**Observe:** `git branch` lists `update-registration-form` with a `*` marking it as the current branch.

### Step 3 — Make a Small Change to the Exercise 1 Source Code

**What:** Edit one of the real Exercise 1 files (`experiment-01/index.html`, `style.css`, or `script.js`) with one small, self-contained change.

**Why:** The experiment is about managing a real change through GitHub, not about the change's complexity — a small, single-purpose edit is easiest to review and merge cleanly.

> **Note:** No specific change is prescribed by the source material for this experiment. The example below is illustrative only — pick any small, genuine improvement to the registration form when carrying this out (for example, a wording tweak, a label change, or a minor style adjustment), and treat it as the actual change for Steps 3 onward.
>
> **Example (illustrative, not actually applied to the project files):** changing the submit button's label in `experiment-01/index.html` from `Register` to `Register Now`.

**Action:** Edit the chosen file and save it.

**Observe:**

```bash
git status
git diff
```

The changed file appears as modified, and `git diff` shows exactly the lines edited.

### Step 4 — Stage and Commit the Change

**What:** Record the change as a commit on the feature branch.

**Why:** A commit with a clear message is what makes the change reviewable later, both locally and in the Pull Request diff.

**Command:**

```bash
git add <modified-file>
git commit -m "<meaningful commit message>"
```

*(Adjust the file name and message to match whatever change was actually made in Step 3.)*

**Observe:** `git status` reports a clean working tree; `git log --oneline` shows the new commit on top.

### Step 5 — Push the Feature Branch to GitHub

**What:** Upload the feature branch — not `main` — to GitHub.

**Why:** A branch must exist on GitHub before a Pull Request can be opened from it.

**Command:**

```bash
git push -u origin update-registration-form
```

**Observe:** GitHub's push output includes a link to open a Pull Request for the branch. The branch also becomes visible in the repository's branch dropdown on GitHub.

### Step 6 — Open a Pull Request

**What:** On GitHub, open a Pull Request from `update-registration-form` into `main`.

**Why:** The Pull Request is the formal record of "this branch is ready to be merged" and is where the change gets reviewed before it becomes part of `main`.

**Action:**

1. Go to the repository on GitHub.
2. Click **Compare & pull request** for the pushed branch (or **New pull request**, then select the branch).
3. Confirm the base branch is `main` and the compare branch is `update-registration-form`.
4. Add a short title and description of the change.
5. Click **Create pull request**.

**Observe:** The Pull Request page opens, showing its status as open and unmerged.

### Step 7 — Review the Diff

**What:** Inspect exactly what the Pull Request changes before merging it.

**Why:** This is the review step that distinguishes managed source code from an unreviewed `git push` — confirming the diff matches the intended change catches mistakes before they reach `main`.

**Action:** Open the **Files changed** tab on the Pull Request.

**Observe:** Only the intended file(s) are listed, and the highlighted additions/removals match the edit made in Step 3 — nothing unrelated is included.

### Step 8 — Merge the Pull Request

**What:** Merge the reviewed branch into `main` using GitHub's UI.

**Why:** Merging is the point where the change officially becomes part of the project's main line of history.

**Action:** On the Pull Request page, click **Merge pull request**, then **Confirm merge**.

**Observe:** The Pull Request status changes to **Merged**. The repository's default branch view now shows the change in `main` on GitHub.

### Step 9 — Pull the Merged Change Back Locally

**What:** Update the local `main` branch with the change that was just merged on GitHub.

**Why:** The merge happened on GitHub, not on the local machine — the local `main` is still behind until it is pulled.

**Command:**

```bash
git switch main
git pull origin main
```

**Observe:** The edited file's content locally now matches what was merged, and `git log --oneline` shows the merged commit on `main`.

### Step 10 — Clean Up the Feature Branch

**What:** Delete the feature branch now that it has been merged.

**Why:** A merged branch left behind adds clutter and makes the branch list harder to read over time.

**Command:**

```bash
git branch -d update-registration-form
git push origin --delete update-registration-form
```

**Observe:** `git branch` no longer lists the feature branch locally, and it no longer appears in the branch dropdown on GitHub.

## Observation / Verification

| Check | Where | Confirms |
|---|---|---|
| `git branch` | Local | Feature branch was created, then removed after merge |
| `git log --oneline` on `main` | Local | Merged commit is present after `git pull` |
| Pull Request **Files changed** tab | GitHub | Diff matched the intended change before merging |
| Pull Request status | GitHub | Shows **Merged**, not left open |
| Repository file view | GitHub | `experiment-01` file reflects the merged change |
| `git status` | Local | Working tree is clean after the full cycle |

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Editing directly on `main` instead of a feature branch | Change has no isolated history, no PR possible | `git switch -c <branch>` before editing |
| Forgetting to push the branch before opening a PR | GitHub has no branch to compare | `git push -u origin <branch>` first |
| Merging without opening the **Files changed** tab | Unintended or unrelated changes get merged | Always review the diff before clicking merge |
| Forgetting to pull `main` after merging on GitHub | Local `main` looks outdated, missing the merged change | `git switch main && git pull origin main` |
| Leaving merged branches around | Branch list fills up with stale branches | Delete the branch locally and on GitHub after merge |

## Quick Reference

| Command / Action | Purpose |
|---|---|
| `git switch -c <branch>` | Create and switch to a new feature branch |
| `git add` / `git commit -m` | Stage and commit the change on the branch |
| `git push -u origin <branch>` | Push the feature branch to GitHub |
| GitHub → **Compare & pull request** | Open a Pull Request from the pushed branch |
| PR → **Files changed** tab | Review the diff before merging |
| PR → **Merge pull request** | Merge the branch into `main` on GitHub |
| `git switch main && git pull origin main` | Bring the merged change back locally |
| `git branch -d` / `git push origin --delete` | Remove the merged branch, locally and remotely |

## Result

The Experiment 01 event registration source code was carried through a complete source code management cycle on GitHub: a feature branch was created, a change was made and committed, the branch was pushed, a Pull Request was opened and its diff reviewed, the Pull Request was merged into `main`, and the merged change was pulled back into the local repository.
