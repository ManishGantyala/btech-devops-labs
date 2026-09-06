# Experiment 02 – Explore Git and GitHub Commands

## Aim

To explore Git and GitHub commands, and to understand how they work together to track changes in a project and collaborate using a remote repository.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain why version control is needed.
- Explain what Git is and what GitHub is, and how they differ.
- Create a GitHub account and configure Git locally with name and email.
- Track a file through the working directory → staging area → commit cycle.
- View commit history and inspect changes.
- Create, switch, and merge branches.
- Create a personal GitHub repository, add the Experiment 01 application to it, and push, pull, and clone it.

## Requirements

- A GitHub account (free). If you do not have one yet, go to `https://github.com`, click **Sign up**, and create an account before continuing. You will need it for the GitHub steps below.
- A computer with Git installed. Install it if needed:

```bash
sudo apt update
sudo apt install git -y
```

- A terminal or command prompt.
- The three Experiment 01 files (`index.html`, `style.css`, `script.js`) that you built in Experiment 01.

**Branch name note:** Recent versions of Git name the default branch `main`; older versions may name it `master`. This guide uses `main` throughout — if your system uses `master`, substitute `master` wherever `main` appears in the steps below.

> **Instructor Reference Repository:** The public repository at `https://github.com/ManishGantyala/btech-devops-labs` shows the expected file structure and commit history for all twelve experiments. Use it as a reference to check your own work at any stage. Do not clone or fork it as your working repository — each student creates and uses their own GitHub repository throughout this series.

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

## 7. Procedure — Part 1: Git Basics (Practice Repository)

Steps 1–13 use a small practice folder called `git-demo` to learn individual commands in isolation. This folder is disposable — its only purpose is to get comfortable with Git commands before you set up your actual working repository in Part 2.

### Step 1 — Check Git Installation

**Why:** confirms Git is installed and usable from the terminal before doing anything else.

```bash
git --version
```

**Observe:** a version number should be displayed, in the form:

```text
git version 2.x.x
```

### Step 2 — Configure Git with Your Name and Email

**Why:** every commit permanently records *who* made it. This only needs to be done once per computer. Use your real name and the email address you used for your GitHub account — this is how GitHub links your commits to your profile.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --list
```

**Observe:** `user.name` and `user.email` should appear in the `--list` output with the values you set.

### Step 3 — Create a Practice Directory

```bash
mkdir git-demo
cd git-demo
```

This folder is your working directory for Steps 3–13 only.

### Step 4 — Initialize a Repository

**What it does:** `git init` turns an ordinary folder into a Git repository by creating a hidden `.git` folder, where Git will store all history and tracking information.

**Why:** without this, Git has no idea this folder should be tracked at all.

```bash
git init
```

**Observe:** Git reports the new repository was initialized. Run `ls -a` to confirm a `.git` folder now exists inside `git-demo`.

### Step 5 — Check Repository Status

**What it does:** `git status` reports the current state of the repository — which branch you're on, and which files are untracked, modified, or staged.

**Why:** this is the command you will run constantly, before and after almost every other command, to see what Git is currently seeing.

```bash
git status
```

**Observe:** with an empty new repository, Git reports the current branch name and that there is nothing to commit yet. This is the expected starting state.

### Step 6 — Create a File

```bash
echo "Git and GitHub Experiment" > README.txt
git status
```

**Observe:** `README.txt` should be listed as an **untracked file** — Git sees it exists but is not tracking it. Every new file starts in this state.

### Step 7 — Stage the File

**What it does:** `git add` moves a change from the working directory into the staging area.

**Why:** staging lets you deliberately choose what goes into your next commit, rather than committing every changed file at once.

```bash
git add README.txt
git status
```

**Observe:** `README.txt` should now appear under "Changes to be committed." It has moved from untracked to staged.

To stage more than one file, or everything at once:

```bash
git add file1.txt file2.txt
git add .
```

(`.` means "everything changed in the current directory.") **Caution:** `git add .` stages *every* changed and untracked file in the current directory tree — including files you may not intend to commit, such as configuration files containing passwords. Run `git status` before using it to review exactly what will be staged.

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

**Observe:** running `git status` again should report that the working tree is clean, with nothing left to commit. The commit is permanently saved.

### Step 9 — View Commit History

```bash
git log
git log --oneline
```

`git log` shows full commit details (author, date, message, commit hash); `--oneline` compresses each commit to a single line — useful once a project has many commits.

**Observe:** the commit created in Step 8 should appear, most recent first.

### Step 10 — View Changes with `git diff`

```bash
git diff            # changes not yet staged
git diff --staged   # changes already staged, about to be committed
```

Run `git diff` before staging to review what you are about to add. Run `git diff --staged` before committing to review exactly what the commit will contain.

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

### Step 13 — Commit Something on the Branch, Then Merge

Make a small change on the branch so there is something to merge:

```bash
echo "Feature work" >> README.txt
git add README.txt
git commit -m "Add feature note on feature-login branch"
```

Switch back to `main` and merge:

```bash
git switch main
git merge feature-login
```

```text
feature-login --(git merge)--> main
```

**Observe:** `git log --oneline` on `main` should now include the commit(s) made on `feature-login`.

---

## 9. Procedure — Part 2: Your Working Repository (Used from Experiment 03 Onwards)

The `git-demo` folder was for practice only. Part 2 creates the repository you will use for all remaining experiments. It contains your Experiment 01 application files, is pushed to your own GitHub account, and is what Experiment 03 continues from directly.

### Step 14 — Create Your GitHub Repository

1. Open `https://github.com` in your browser and sign in to your account.
2. Click the **+** icon at the top-right of the page and select **New repository**.
3. In the **Repository name** field, enter a name — for example, `devops-lab`. This is your personal repository; choose any name you like.
4. Set visibility to **Public** or **Private** — either works for this series.
5. Leave **Add a README file**, **Add .gitignore**, and **Choose a license** all **un-ticked**. The repository must start completely empty so that pushing from your local machine works without conflicts.
6. Click **Create repository**.
7. On the blank repository page, copy the HTTPS URL — it looks like `https://github.com/<your-username>/devops-lab.git`. You will paste this URL in Step 17.

**Confirm:** The repository page shows "This repository is empty." — this is correct.

### Step 15 — Create the Local Working Directory

Move out of the `git-demo` folder and create a new directory for your working repository:

```bash
cd ..
mkdir devops-lab
cd devops-lab
git init
```

**Observe:** `git init` reports a new repository was initialized inside `devops-lab`. Run `ls -a` to confirm the `.git` folder is present.

### Step 16 — Add Your Experiment 01 Files

The Experiment 01 application files go inside an `experiment-01/` subfolder. This folder structure (`experiment-01/`, `experiment-02/`, …) mirrors how the experiments are organized throughout the series.

```bash
mkdir experiment-01
```

Copy your three Experiment 01 files into `experiment-01/`. Adjust the source path to wherever your files are saved:

```bash
cp /path/to/your/index.html experiment-01/
cp /path/to/your/style.css  experiment-01/
cp /path/to/your/script.js  experiment-01/
```

Confirm the files are in place:

```bash
ls experiment-01/
```

**Observe:** `index.html`, `style.css`, and `script.js` are listed inside `experiment-01/`.

### Step 17 — Stage and Commit the Experiment 01 Files

```bash
git add experiment-01/
git commit -m "Add Experiment 01 event registration application"
```

Check the result:

```bash
git status
git log --oneline
```

**Observe:** `git status` reports a clean working tree. `git log --oneline` shows the commit you just made.

### Step 18 — Connect the Local Repository to Your GitHub Repository

Register your GitHub repository as the remote named `origin`:

```bash
git remote add origin <your-repository-url>
```

Replace `<your-repository-url>` with the HTTPS URL copied in Step 14.

Verify the remote was registered:

```bash
git remote -v
```

**Observe:**

```text
origin  https://github.com/<your-username>/devops-lab.git (fetch)
origin  https://github.com/<your-username>/devops-lab.git (push)
```

`(fetch)` is the URL Git uses when *downloading* from GitHub (`git pull`, `git fetch`). `(push)` is the URL Git uses when *uploading* to GitHub (`git push`). Both should show your own GitHub repository URL.

### Step 19 — Push to GitHub

```bash
git push -u origin main
```

The `-u` flag links your local `main` branch to the remote `main` branch, so future pushes in this repository only need `git push`.

**Observe:** after the push completes, open your GitHub repository in a browser. The `experiment-01/` folder and the three files inside it should be visible on the repository's main page. This is your working repository — it is what Experiment 03 continues from.

### Step 20 — Pull from GitHub

`git pull` downloads any new commits from the remote and merges them into your local branch. In a solo workflow you may not have anything new to pull, but the command is essential when collaborators push changes or when you merge a Pull Request on GitHub (as you will do in Experiment 03).

```bash
git pull origin main
```

**Observe:** because you just pushed, Git reports "Already up to date." — this is the correct, expected result.

### Step 21 — Clone a Repository

`git clone` creates a brand-new local copy of a repository from scratch. Use it when a repository exists on GitHub but not yet on your computer. To demonstrate, clone your own repository into a separate folder:

```bash
cd ..
git clone <your-repository-url> devops-lab-clone
cd devops-lab-clone
git status
ls experiment-01/
```

**Observe:** `git status` shows a clean working tree. The `experiment-01/` folder and all three files are present — cloning downloads everything automatically. Unlike `git init`, `git clone` also sets up `origin` automatically: run `git remote -v` to confirm it already points to your GitHub repository.

Return to your main working directory:

```bash
cd ../devops-lab
```

---

## 10. Push, Pull, and Clone — Summary

| Command | Direction | When to use it |
|---|---|---|
| `git push` | Local → GitHub | After committing, to upload your commits to GitHub |
| `git pull` | GitHub → Local | When GitHub has new commits your local copy does not have yet |
| `git clone` | GitHub → New local folder | When you need a fresh local copy of a repository that does not exist on your machine yet |

---

## 11. Verification

Run these commands to confirm the experiment has been carried out correctly:

| Check | What to look for |
|---|---|
| `git status` (in `devops-lab/`) | Working tree is clean; nothing left uncommitted |
| `git log --oneline` (in `devops-lab/`) | At least one commit with a meaningful message |
| `git branch` | `main` branch exists |
| `git remote -v` | `origin` points to your own GitHub repository URL |
| GitHub repository page in browser | `experiment-01/` folder with `index.html`, `style.css`, `script.js` visible |
| `git status` (in `devops-lab-clone/`) | Clean working tree; `experiment-01/` files present |

## 12. Common Beginner Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Running Git commands outside the repo | "not a git repository" error | `pwd` to check location, `cd` into the folder containing `.git` |
| Forgetting to stage changes | File missing from the commit | `git status`, then `git add` before committing |
| Confusing `add` with `commit` | Changes staged but never saved to history | Always follow `git add` with `git commit -m "..."` |
| Forgetting to push | Commits exist locally but not on GitHub | `git push` after committing |
| Editing on the wrong branch | Changes end up on an unintended branch | `git branch` to check, `git switch` to change |
| GitHub repo created with a README/license already present | `git push` fails with "failed to push some refs" / "updates were rejected" | Recreate the GitHub repo empty (all options un-ticked), or run `git pull origin main --allow-unrelated-histories` once to merge the two histories before pushing |
| Using someone else's repository URL instead of your own | You do not have push access | Confirm `git remote -v` shows your own GitHub username in the URL |

## 13. Quick Command Reference

| Command | Purpose |
|---|---|
| `git --version` | Check installed Git version |
| `git config --global user.name` / `user.email` | Set your identity for commits |
| `git init` | Initialize a repository |
| `git status` | Check current repository state |
| `git add` | Stage changes |
| `git commit -m` | Save staged changes as a commit |
| `git log` / `git log --oneline` | View commit history |
| `git diff` / `git diff --staged` | View unstaged / staged changes |
| `git branch` | List or create branches |
| `git switch` | Change the current branch |
| `git switch -c` | Create and switch to a new branch |
| `git merge` | Combine another branch into the current one |
| `git remote add origin` | Register a remote repository |
| `git remote -v` | View registered remotes |
| `git push -u origin main` | Push and link the branch to the remote (first push) |
| `git push` | Push after the first time |
| `git pull` | Download and merge remote changes |
| `git clone` | Create a local copy of a remote repository |

## 14. Result

This experiment covered the essential Git and GitHub commands: configuring Git with a name and email, initializing a local repository, tracking files through the staging area into commits, viewing history and diffs, creating and merging branches, and connecting a local repository to a personal GitHub repository for pushing, pulling, and cloning. By the end of Part 2, a working repository containing the Experiment 01 application files is live on your own GitHub account — this repository is what Experiment 03 continues from.
