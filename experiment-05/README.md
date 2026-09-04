# Experiment 05 – Demonstrate CI/CD Using Jenkins

## Aim

To demonstrate Continuous Integration and Continuous Deployment (CI/CD) using a Jenkins Pipeline connected to this project's GitHub repository — first run manually, then extended to trigger automatically on a push to `main`.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain why a GitHub Personal Access Token (PAT) is needed for Jenkins to access a GitHub repository over HTTPS.
- Create a Jenkins **Pipeline** job connected to a GitHub repository.
- Define pipeline stages that check out, validate, deploy, and verify an application.
- Trigger a pipeline manually and confirm successful execution from its console output.
- Explain why a locally running Jenkins instance (inside WSL2) cannot directly receive a GitHub webhook, and how a tool like ngrok addresses that.
- Configure a GitHub webhook so a push to `main` automatically triggers the Jenkins pipeline, and distinguish a webhook-triggered build from a manually triggered one using its console output.

This experiment assumes Jenkins is already installed, running, and reachable at its dashboard — that is Experiment 04, and is not repeated here.

## Requirements

- A running Jenkins instance (Experiment 04), running locally inside WSL2.
- This project's GitHub repository, with a GitHub Personal Access Token (PAT) for Jenkins to authenticate against it.
- Nginx installed on the Jenkins host, used to serve the deployed application.
- Write access to the deployment target directory, `/var/www/jenkins-demo`.
- For Part B only: ngrok, used to expose the local Jenkins instance to the internet for GitHub webhook delivery.

## Concept — CI/CD Using Jenkins

A Jenkins **Pipeline** job defines an ordered sequence of stages that Jenkins runs every time the job executes. In this experiment, the pipeline's stages are:

```text
Checkout --> Validate --> Deploy --> Verify
```

- **Checkout** — pulls the latest source from the GitHub repository.
- **Validate** — checks the pulled source before it is used further.
- **Deploy** — publishes the application to `/var/www/jenkins-demo`, served by Nginx.
- **Verify** — confirms the deployment succeeded.

Separately from *what* the pipeline does is *what starts it* — its **trigger**. This experiment was carried out in two parts, in the order they were actually done:

- **Part A** — the pipeline above, started manually (**Build Now**). This was the original working implementation and is what proves the CI/CD stages themselves work correctly.
- **Part B** — the same goal extended so a `git push` to `main` on GitHub starts the pipeline automatically, with no manual click. This was added *after* Part A was already working, as a second, automatic trigger for the same underlying pipeline.

## Prerequisites — Before Part A

Before running any pipeline, confirm the following are in place on the Jenkins host (WSL2):

**1. Nginx installed:**

```bash
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

**2. Deployment directory created with correct permissions:**

```bash
sudo mkdir -p /var/www/jenkins-demo
sudo chown -R jenkins:jenkins /var/www/jenkins-demo
```

`/var/www/jenkins-demo` is the directory the Deploy stage writes to. The `jenkins` user (which runs the pipeline) must own it, or the Deploy stage will fail with a permission error.

---

## Part A — Configure Jenkins for the GitHub Repository

*(Original, manually-triggered implementation.)*

### Step 1 — Configure GitHub PAT Credentials

**What:** Create a GitHub Personal Access Token and add it to Jenkins as a credential.

**Why:** GitHub no longer accepts an account password for Git operations over HTTPS; Jenkins needs a PAT in its place to authenticate when it checks out the repository.

**Creating the PAT on GitHub:**

1. Sign in to GitHub and go to **Settings** (top-right avatar menu).
2. Scroll down to **Developer settings** (bottom of the left sidebar).
3. Select **Personal access tokens → Tokens (classic)**.
4. Click **Generate new token (classic)**.
5. Set a note (e.g., `Jenkins CI`) and an expiration.
6. Under **Select scopes**, tick **repo** (grants read access to private repositories). For a public repository, `public_repo` is sufficient.
7. Click **Generate token** and copy the value — it will not be shown again.

**Adding the PAT to Jenkins:**

1. Go to **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**.
2. Set **Kind** to `Username with password`.
3. Enter your GitHub username and paste the PAT as the password.
4. Give it an ID of `e.g., github-btech-devops` and save.

**Observe:** The credential appears in Jenkins's credentials list and is selectable when configuring the pipeline's source.

### Step 2 — Configure the Jenkins Pipeline

**What:** Create a new Jenkins job of type **Pipeline**, and connect it to this project's GitHub repository using the PAT credential from Step 1.

**Why:** A Pipeline job (rather than a single build step) is what allows a defined, ordered sequence of stages — matching the Checkout/Validate/Deploy/Verify flow this experiment uses.

**Action:** Create the Pipeline job, and configure it with the GitHub repository as its source, authenticating with the credential configured in Step 1. The four-stage pipeline is defined in `experiment-05/Jenkinsfile` in this repository — that file is the actual pipeline script used for this experiment.

**Observe:** The pipeline job's configuration shows the GitHub repository connected via the PAT credential.

### Step 3 — Configure Pipeline Stages

**What:** Define the pipeline's four stages: **Checkout**, **Validate**, **Deploy**, **Verify**.

**Why:** Each stage represents one part of the CI/CD flow — Checkout retrieves the source, Validate checks it, Deploy publishes it, and Verify confirms the deployment.

**Action:** The **Deploy** stage was configured to publish the application to `/var/www/jenkins-demo`, from where Nginx serves it.

**Observe:** The pipeline's stage view lists all four stages in order: Checkout → Validate → Deploy → Verify.

**Note on the pipeline script:** The actual pipeline script is `experiment-05/Jenkinsfile` in this repository. It defines the four stages — Checkout, Validate, Deploy, and Verify — matching the flow described in the Concept section. The credential ID used in the Jenkinsfile's Checkout stage is `github-btech-devops`, which must match the credential created in Step 1.

### Step 4 — Run the Pipeline Manually

**What:** Trigger the pipeline using Jenkins's **Build Now**.

**Why:** This was the original trigger used to confirm the pipeline itself worked correctly, before attempting to automate how it gets triggered (Part B).

**Action:** Click **Build Now** on the pipeline job.

**Observe:** The build starts, and the stage view shows Checkout, Validate, Deploy, and Verify executing in sequence.

### Step 5 — Verify the Pipeline Execution

**What:** Confirm the manually triggered build completed successfully.

**Why:** This closes the loop for Part A — the pipeline stages must be confirmed working before Part B's automatic trigger is layered on top.

**Action:** Open the build's console output, and confirm the deployed files are present at `/var/www/jenkins-demo` and served by Nginx.

**Observe:** The console output shows all four stages completing, ending in:

```text
Finished: SUCCESS
```

## Part B — Automatic Trigger on GitHub Push (Alternative/Extension)

*(Added after Part A was already working.)*

### Step 1 — Requirement for Automatic Trigger

**What:** After the manual pipeline (Part A) was working, the next goal was to have the same pipeline start automatically whenever code was pushed to `main`, instead of requiring a manual **Build Now** click each time.

**Why:** A manually triggered build proves the pipeline works, but genuine CI/CD reacts to a push on its own — this is the piece Part A was missing.

**Observe:** Because Jenkins was running locally inside WSL2, it has no public address that GitHub can reach to deliver a webhook — this is the specific obstacle Part B had to solve.

### Step 2 — Introduce ngrok for Local WSL2 Jenkins

**What:** Use ngrok to create a temporary public tunnel to the local Jenkins instance.

**Why:** GitHub's webhook delivery requires a publicly reachable URL. ngrok was introduced *specifically* to solve this for a Jenkins instance running locally under WSL2 — it was not needed for Part A, and is not a requirement of Experiment 05's core CI/CD demonstration.

**Installing ngrok (one-time):**

```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

Sign up at ngrok.com, then add your auth token:

```bash
ngrok config add-authtoken <your-token>
```

**Running ngrok** (in a separate terminal, keep it open):

```bash
ngrok http 8080
```

**Observe:** ngrok reports an active public forwarding URL in the form `https://<random-subdomain>.ngrok-free.app` mapped to `http://localhost:8080`. Copy this URL — it is used as the base of the webhook payload URL in Step 3.

### Step 3 — Configure GitHub Webhook

**What:** Add a webhook in the GitHub repository's settings, pointing at the Jenkins GitHub-webhook endpoint via the ngrok URL, and enable Jenkins's GitHub push trigger on the pipeline job.

**Why:** The webhook is what tells GitHub to notify Jenkins on a push; the corresponding trigger option must also be enabled on the Jenkins side, or an incoming webhook call has nothing to start.

**Action:**

1. In GitHub, go to the repository → **Settings → Webhooks → Add webhook**.
2. Set **Payload URL** to `<ngrok-forwarding-url>/github-webhook/` (include the trailing slash and the `/github-webhook/` path — this is the specific Jenkins endpoint that handles GitHub events).
3. Set **Content type** to `application/json`.
4. Leave **Which events** as **Just the push event**.
5. Click **Add webhook**.
6. In Jenkins, open the pipeline job → **Configure → Build Triggers**, and tick **GitHub hook trigger for GITScm polling**. Save.

**Observe:** The webhook is listed under the repository's Webhooks settings. The Jenkins pipeline job shows **GitHub hook trigger for GITScm polling** enabled under Build Triggers.

### Step 4 — Push to `main`

**What:** Push a commit to the `main` branch on GitHub.

**Why:** This is the actual event the webhook and ngrok tunnel exist to react to.

**Command:**

```bash
git push origin main
```

**Observe:** The new commit appears on `main` on GitHub.

### Step 5 — Verify Automatic Jenkins Trigger

**What:** Confirm Jenkins started a new build on its own, without a manual **Build Now** click.

**Why:** This is the evidence that the webhook → ngrok → Jenkins chain actually worked end-to-end, rather than just being configured.

**Action:** Open the new build's console output in Jenkins.

**Observe:** The console output began with:

```text
Started by GitHub push by ManishGantyala
```

This line is the key evidence distinguishing an automatic, webhook-triggered build from a manually triggered one.

### Step 6 — Verify Successful Pipeline Execution

**What:** Confirm the automatically triggered build ran through the full pipeline and completed successfully.

**Why:** This shows the automatic trigger produces the same working CI/CD result as the manual run in Part A, not just that it started.

**Action:** Review the console output/stage view for Checkout, Validate, Deploy, and Verify, and confirm the deployed files at `/var/www/jenkins-demo` reflect the pushed change.

**Observe:** The console output ended with:

```text
Finished: SUCCESS
```

## Observation / Verification

| Check | Where | Confirms |
|---|---|---|
| PAT credential listed in Jenkins | Manage Jenkins → Credentials | Jenkins can authenticate to GitHub |
| Pipeline stage view shows Checkout, Validate, Deploy, Verify | Pipeline job page | Stages are configured as intended |
| Manual build (Part A) console output ends `Finished: SUCCESS` | Console Output | The core pipeline works correctly, independent of trigger |
| Deployed files present at `/var/www/jenkins-demo`, served via Nginx | Jenkins host | Deploy stage actually published the application |
| ngrok shows an active public forwarding URL | ngrok terminal | The local Jenkins instance is reachable from the internet |
| Webhook listed under GitHub repository Webhooks settings | GitHub → Settings → Webhooks | GitHub is configured to notify Jenkins on push |
| New build appears in Jenkins without clicking Build Now | Jenkins build history | The webhook actually triggered a build |
| Build console output begins `Started by GitHub push by ManishGantyala` | Console Output | Confirms the build was webhook-triggered, not manual |
| Automatically triggered build also ends `Finished: SUCCESS` | Console Output | The automatic trigger produces a fully working pipeline run |

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Using a GitHub account password instead of a PAT | Jenkins fails to authenticate/checkout the repository | Use a PAT as the credential, not a password |
| Assuming a webhook alone is enough | Push to `main` doesn't trigger a build | The pipeline job also needs its GitHub push trigger option enabled in Jenkins |
| ngrok tunnel restarted | Webhook deliveries start failing after previously working | ngrok's free-tier URL changes on restart; update the webhook's payload URL in GitHub to match |
| Missing the webhook path on the payload URL | GitHub reports the delivery as sent, but Jenkins never reacts | Confirm the payload URL points at Jenkins's GitHub-webhook endpoint |
| Deploy stage fails from permission errors | Deploy stage fails writing to `/var/www/jenkins-demo` | Confirm the Jenkins process has write access to the deployment directory |
| Confusing a manual build with a webhook-triggered one | Assuming automatic triggering works without checking | Check the console output's "Started by" line — it differs between a manual build and a GitHub push-triggered one |

## Quick Reference

| Action | Purpose |
|---|---|
| GitHub → PAT → Jenkins Credentials | Let Jenkins authenticate to the GitHub repository |
| New Item → Pipeline | Create the Jenkins pipeline job |
| Pipeline stages: Checkout, Validate, Deploy, Verify | Define the CI/CD flow |
| **Build Now** | Manually trigger the pipeline (Part A) |
| Deploy target: `/var/www/jenkins-demo`, served by Nginx | Where the application is deployed |
| ngrok → local Jenkins port | Expose local WSL2 Jenkins publicly (Part B only) |
| GitHub → Settings → Webhooks | Notify Jenkins of pushes to `main` |
| Jenkins pipeline job → GitHub push trigger option | Let Jenkins act on the incoming webhook |
| `git push origin main` | Trigger event for the automatic pipeline run |
| Console Output: `Started by GitHub push by ManishGantyala` | Evidence of an automatic, webhook-triggered build |
| Console Output: `Finished: SUCCESS` | Evidence the pipeline completed successfully |

## Result

CI/CD was demonstrated successfully using a Jenkins Pipeline connected to this project's GitHub repository. In Part A, the pipeline — Checkout, Validate, Deploy, Verify — was configured and run manually via **Build Now**, deploying the application to `/var/www/jenkins-demo` behind Nginx, with the console output ending in `Finished: SUCCESS`. In Part B, automatic triggering on a push to `main` was subsequently added and verified using a GitHub webhook tunneled through ngrok (required because Jenkins runs locally inside WSL2); the resulting build's console output began with `Started by GitHub push by ManishGantyala` and again ended in `Finished: SUCCESS`, confirming the automatic trigger produced a fully successful pipeline run.
