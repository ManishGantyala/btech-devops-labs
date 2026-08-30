# Experiment 02 – Explore Git and GitHub Commands

## Aim

To explore Git and GitHub commands, and to understand how they work together to track changes in a project and collaborate using a remote repository.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain why version control is needed.
- Explain what Git is and what GitHub is, and how they differ.
- Configure Git and create a local repository.
- Track a file through the working directory → staging area → commit cycle.
- View commit history and inspect changes.
- Create, switch, and merge branches.
- Connect a local repository to GitHub and push, pull, and clone repositories.

## Requirements

- A computer with Git installed.
- A terminal or command prompt.
- A GitHub account.

---

## 1. Why Version Control Is Needed

While building software, files are modified constantly. A developer might change a file today, change it again tomorrow, and later need the version from three days ago. Keeping copies like `script.js`, `script_v2.js`, `script_final.js` by hand quickly becomes unmanageable — and gets worse the moment more than one person is editing the same project.

A **Version Control System (VCS)** solves this: it automatically records every change made to a project, so any earlier version can be recovered, changes can be compared, and multiple people can work on the same codebase without overwriting each other.

**Git** is the version control system used in this experiment. **GitHub** is where a Git project can be hosted online so it can be shared. The rest of this document explains both, then walks through using them.

## 2. What Is Git?

Git is a **distributed version control system** that runs on your own computer and tracks the history of a project.

*Distributed* means every developer's computer holds a **complete copy** of the project's history — not just the latest files, but every past version too. This is why most Git commands (creating commits, viewing history, switching branches) work instantly with no internet connection; a network is only needed when sharing changes with someone else.

With Git, a developer can: create a repository, track files, record changes as commits, create branches to work on features independently, compare versions, and merge work back together.

## 3. What Is GitHub?

GitHub is an online platform that hosts Git repositories. Git itself has no built-in "cloud" — GitHub is what turns a project sitting on one computer into something that can be shared, backed up, and worked on by a team.

With GitHub, a repository can be: stored online as a backup and a shared source of truth, accessed and updated by multiple collaborators, and browsed through a web interface.

```text
Your Computer                 GitHub
------------------            ------------------
Local Git Repository  --push-->  GitHub Repository
                       <--pull--
```

## 4. Git vs GitHub

| | Git | GitHub |
|---|---|---|
| What it is | A version control system | A website that hosts Git repositories |
| Where it runs | Installed on your computer | Accessed online |
| Works offline? | Yes, for local operations | No, requires a network connection |
| What it gives you | Commands to track and manage changes | A place to share, back up, and collaborate on repositories |

## 5. Core Vocabulary

A few terms are used constantly from here on. Read these once now — they will make much more sense once you see them in action in Section 7 onward.

| Term | Meaning |
|---|---|
| **Repository (repo)** | The location where Git stores a project's files and their full history. Can be *local* (your computer) or *remote* (e.g., on GitHub). |
| **Working directory** | The actual project folder on disk, where you create and edit files. |
| **Staging area** | A holding area where you choose exactly which changes should go into the *next* commit, instead of committing everything you've touched. |
| **Commit** | A saved checkpoint of staged changes, with a message describing what changed. |
| **Branch** | An independent line of development, so a feature can be built without disturbing the main codebase. |
| **Remote** | A copy of the repository stored somewhere else — in this experiment, on GitHub. `origin` is the conventional name given to a project's main remote. |

## 6. Basic Git Workflow

This is the cycle every change in a Git project goes through. Keep this diagram in mind — every command taught below is one arrow in it.

```text
Working Directory --(git add)--> Staging Area --(git commit)--> Local Repository
                                                                       |
                                                                  (git push)
                                                                       v
                                                              GitHub Repository
                                                                       |
                                                                  (git pull)
                                                                       v
                                                             back into Local Repository
```

---

## 7. Procedure — Local Repository Basics

### Step 1 — Check Git Installation

**Why:** confirms Git is installed and usable from the terminal before doing anything else.

```bash
git --version
```

**Observe:** a version number should be displayed, in the form:

```text
git version 2.x.x
```

### Step 2 — Configure Git

**Why:** every commit records *who* made it. This only needs to be done once per computer.

```bash
git config --global user.name "<your-name>"
git config --global user.email "<your-email>"
git config --list
```

**Observe:** `user.name` and `user.email` should appear in the `--list` output with the values you set.

### Step 3 — Create a Project Directory

```bash
mkdir git-demo
cd git-demo
```

This folder is now your working directory for the rest of the experiment.

### Step 4 — Initialize a Repository

**What it does:** `git init` turns an ordinary folder into a Git repository by creating a hidden `.git` folder, where Git will store all history and tracking information.

**Why:** without this, Git has no idea this folder should be tracked at all.

```bash
git init
```

**Observe:** a `.git` folder should now exist inside `git-demo` (it is hidden — use `ls -a` to see it).

**Note:** recent versions of Git name the default branch `main`; older versions may default to `master`. This guide uses `main` throughout — if `git branch` shows a different name on your system, substitute that name wherever `main` appears in the steps below.

### Step 5 — Check Repository Status

**What it does:** `git status` reports the current state of the repository — which branch you're on, and which files are untracked, modified, or staged.

**Why:** this is the command you will run constantly, before and after almost every other command, to see what Git is currently seeing.

```bash
git status
```

**Observe:** with an empty new repository, Git should report the current branch and that there is nothing to commit yet.

### Step 6 — Create a File

```bash
echo "Git and GitHub Experiment" > README.txt
git status
```

**Observe:** `README.txt` should be listed as an **untracked file** — Git sees it exists but is not yet tracking it. A new file always starts here, before it can be staged or committed.

### Step 7 — Stage the File

**What it does:** `git add` moves a change from the working directory into the staging area.

**Why:** staging lets you deliberately choose what goes into your next commit, rather than committing every changed file at once.

```bash
git add README.txt
git status
```

**Observe:** `README.txt` should now appear under changes staged for commit.

To stage more than one file, or everything at once:

```bash
git add file1.txt file2.txt
git add .
```

(`.` means "everything changed in the current directory.") Run `git status` afterward to confirm exactly what got staged.

### Step 8 — Commit the Staged Changes

**What it does:** `git commit` permanently records the staged changes as a checkpoint in the repository's history.

**Why:** this is the actual "save point" — staging alone does not save anything to history.

```bash
git commit -m "Add README file"
```

The `-m` message should describe *what changed*, not just say "changes" — this is what makes history readable later:

| Style | Example |
|---|---|
| Good | `Add event registration form` |
| Not useful | `changes` |

**Observe:** running `git status` again should report that the working tree is clean, with nothing left to commit.

### Step 9 — View Commit History

```bash
git log
git log --oneline
```

`git log` shows full commit details (author, date, message, commit ID); `--oneline` compresses each commit to a single line — useful once a project has many commits.

**Observe:** the commit created in Step 8 should appear, most recent first.

### Step 10 — View Changes with `git diff`

```bash
git diff            # changes not yet staged
git diff --staged   # changes already staged, about to be committed
```

Use these to review *exactly* what you're about to stage or commit, before you do it.

**Observe:** immediately after Step 8, both commands should show no output — this is expected, since there is nothing staged or modified beyond what was just committed.

---

## 8. Working with Branches

A branch is a separate line of development off the main history, so a feature can be built without touching `main` until it's ready.

```text
main
 |
 +---- feature-login
```

### Step 11 — View Branches

```bash
git branch
```

**Observe:** the current branch should be marked with `*`, for example `* main`.

### Step 12 — Create and Switch to a Branch

```bash
git branch feature-login     # creates the branch (does not switch to it)
git switch feature-login     # switches to it
```

Or do both in one command:

```bash
git switch -c feature-login
```

**Observe:** `git branch` should now show `* feature-login`.

### Step 13 — Merge a Branch

**Why:** once work on a branch is ready, its commits need to be brought into another branch (usually `main`).

Switch to the branch that should *receive* the changes, then merge:

```bash
git switch main
git merge feature-login
```

```text
feature-login --(git merge)--> main
```

**Observe:** `git log --oneline` on `main` should now include the commit(s) made on `feature-login`.

---

## 9. Working with GitHub

So far, everything has happened only on your computer. This section connects the local repository to a remote one on GitHub.

### Step 14 — Create a Repository on GitHub

1. Sign in to GitHub.
2. Create a new repository and give it a name.
3. Create it **without** a README, `.gitignore`, or license file — leave it empty. Your local repository already has commits (from Section 7), and an empty remote avoids a conflict when pushing in Step 17.
4. Copy the repository's URL — it will look like `https://github.com/<username>/<repository-name>.git`.

### Step 15 — Connect the Local Repository to GitHub

**What it does:** registers a remote repository under a short name (conventionally `origin`).

```bash
git remote add origin <repository-url>
```

### Step 16 — Verify the Remote

```bash
git remote -v
```

**Observe:** the output should show the `origin` name mapped to your repository URL, for both fetch and push:

```text
origin  <repository-url> (fetch)
origin  <repository-url> (push)
```

---

## 10. Push, Pull, and Clone

| Command | Direction | What it does |
|---|---|---|
| `git push` | Local → GitHub | Uploads local commits to the remote repository |
| `git pull` | GitHub → Local | Downloads and merges new remote commits into your *existing* local repository |
| `git clone` | GitHub → Local | Creates a *brand-new* local copy of a repository that doesn't exist on your computer yet |

### Step 17 — Push to GitHub

```bash
git push -u origin main
```

The `-u` flag is only needed the first time you push a branch — it links your local `main` to GitHub's `main`, so future pushes just need `git push`.

**Observe:** after this completes without error, open the repository on GitHub in a browser to confirm the pushed files and commit(s) appear there.

### Step 18 — Pull from GitHub

Use this when the GitHub repository has changes your local copy doesn't have yet (e.g., made by a collaborator):

```bash
git pull origin main
```

**Observe:** if new commits existed on GitHub, they are now merged in and visible via `git log --oneline`. If your local branch was already up to date (as it will be immediately after Step 17), Git reports "Already up to date" — this is the expected, correct result, not an error.

### Step 19 — Clone a Repository

Use this instead of `pull` when the repository doesn't exist locally at all yet:

```bash
git clone <repository-url>
cd <repository-name>
git status
```

`git clone` downloads the full project history and automatically sets up `origin` for you.

**Observe:** `git status` should show a clean working tree with no staging needed — unlike `git init`, cloning sets up the repository and its remote connection automatically.

---

## 11. Verification

Run these commands to confirm the experiment has been carried out correctly:

| Command | Confirms |
|---|---|
| `git status` | Working tree is clean; nothing left uncommitted |
| `git log --oneline` | Commit(s) exist with meaningful messages |
| `git branch` | Expected branches exist |
| `git remote -v` | `origin` points to the correct GitHub repository URL |
| *(browser)* GitHub repository page | Pushed files and commits are visible online |

## 12. Common Beginner Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Running Git commands outside the repo | "not a git repository" error | `pwd` to check location, `cd` into the folder containing `.git` |
| Forgetting to stage changes | File missing from the commit | `git status`, then `git add` before committing |
| Confusing `add` with `commit` | Changes staged but never saved to history | Always follow `git add` with `git commit -m "..."` |
| Forgetting to push | Commits exist locally but not on GitHub | `git push` after committing |
| Editing on the wrong branch | Changes end up on an unintended branch | `git branch` to check, `git switch` to change |
| GitHub repo created with a README/license already present | `git push` fails with "failed to push some refs" / "updates were rejected" | Recreate the GitHub repo empty (Section 9), or run `git pull origin main --allow-unrelated-histories` once to merge the two histories before pushing again |

## 13. Quick Command Reference

| Command | Purpose |
|---|---|
| `git --version` | Check installed Git version |
| `git config` | Set name/email or view configuration |
| `git init` | Initialize a repository |
| `git status` | Check current repository state |
| `git add` | Stage changes |
| `git commit -m` | Save staged changes as a commit |
| `git log` / `git log --oneline` | View commit history |
| `git diff` / `git diff --staged` | View unstaged / staged changes |
| `git branch` | List or create branches |
| `git switch` | Change the current branch |
| `git merge` | Combine another branch into the current one |
| `git remote add` / `git remote -v` | Add / view a remote repository |
| `git push` | Upload commits to the remote |
| `git pull` | Download and merge remote changes |
| `git clone` | Create a local copy of a remote repository |

## 14. Result

This experiment covered the essential Git and GitHub commands and the workflow that connects them: initializing a repository, tracking a file through the staging area and into a commit, viewing commit history and changes, creating and merging a branch, and connecting a local repository to GitHub for pushing, pulling, and cloning. Completing the procedure in Sections 7 to 10 demonstrates each of these operations in sequence.
