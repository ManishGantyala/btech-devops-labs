# Experiment 04 – Jenkins Installation and Setup

## Aim

To install Jenkins, start it as a running service, complete its initial setup, and reach a working Jenkins dashboard with an admin account.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain what Jenkins is and why it needs a specific Java version to run.
- Add the Jenkins package repository and install Jenkins via the package manager.
- Start, enable, and check the status of the Jenkins service.
- Unlock Jenkins using its initial admin password and complete the setup wizard.
- Reach and confirm a working Jenkins dashboard.

This experiment ends the moment the Jenkins dashboard is reached with an admin account created. Creating jobs, writing pipelines or Jenkinsfiles, and connecting Jenkins to GitHub are **not** part of this experiment — they belong to Experiment 05.

## Requirements

- A Linux system (Ubuntu/Debian-based) with `sudo` access and internet connectivity.
- A terminal or command prompt.
- A web browser, to complete the setup wizard.

## Concept — What Jenkins Is and Why It Is Needed

**Jenkins** is an open-source **automation server**, most commonly used to automatically build, test, and deploy software whenever code changes — this overall practice is called CI/CD (Continuous Integration / Continuous Deployment). *How* Jenkins runs those automated jobs is the subject of Experiment 05. This experiment only gets Jenkins installed and reachable, so that later work has something to build on.

A few facts about Jenkins shape every step below:

- **Jenkins is a Java application.** It runs inside a Java process, so a compatible Java Development Kit (JDK) must exist on the machine before Jenkins can even start.
- **Jenkins is operated through a web interface**, not the terminal. Once installed, almost everything — including finishing the install itself — happens in a browser, by default on port `8080`.
- **Jenkins runs as a background service**, managed like any other Linux service (`systemctl`), so it keeps running independently of any single terminal session.
- **The first time Jenkins starts, it locks itself** and writes a one-time random password to a local file. This is a security measure — it proves whoever is completing the setup has file access on the machine Jenkins is running on, not just network access to port 8080.
- **Plugins are how Jenkins gains functionality.** A fresh Jenkins install can do very little on its own; the setup wizard's "install suggested plugins" step installs the standard baseline plugin set. No specific plugin behavior is used or configured in this experiment.

```text
Java installed --> Jenkins installed --> Jenkins service running --> Unlock Jenkins (browser)
                                                                              |
                                                                     Install plugins
                                                                              |
                                                                     Create admin user
                                                                              |
                                                                      Jenkins dashboard
```

## Procedure

### Step 1 — Check/Install the Java Prerequisite

**What:** Confirm a Jenkins-compatible JDK is installed, or install one.

**Why:** Jenkins is a Java application and will refuse to run without a supported JDK already present on the machine.

**Command:**

```bash
java -version
```

If Java is missing or the version is unsupported, install a supported LTS JDK (Jenkins currently supports Java 17 and Java 21):

```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre
```

**Observe:** `java -version` reports an installed version in the range Jenkins supports.

### Step 2 — Add the Jenkins Package Repository

**What:** Add Jenkins's own package repository and its signing key to the system.

**Why:** Jenkins is not part of the default OS package repositories, so `apt` has no way to find it until this repository is added.

**Command:**

```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
```

**Observe:** `apt update` completes without errors referencing the Jenkins repository, and `jenkins` becomes available as an installable package (`apt-cache policy jenkins`).

### Step 3 — Install Jenkins

**What:** Install the Jenkins package.

**Why:** This is the actual installation step — everything before it was only preparing the system to allow it.

**Command:**

```bash
sudo apt install jenkins
```

**Observe:** The install completes without errors, and the Jenkins service is created (visible via `systemctl status jenkins` in the next step).

### Step 4 — Start and Enable the Jenkins Service

**What:** Start the Jenkins service now, and enable it to start automatically on future boots.

**Why:** Jenkins needs to be actively running before it can be reached in a browser, and enabling it avoids having to start it manually after every reboot.

**Command:**

```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

**Observe:** Both commands complete without error output.

### Step 5 — Check the Jenkins Service Status

**What:** Confirm Jenkins is actually running before trying to open it in a browser.

**Why:** Checking service status first avoids confusing a "service failed to start" problem with a "wrong URL/port" problem later.

**Command:**

```bash
sudo systemctl status jenkins
```

**Observe:** The status reports `active (running)`. If it instead shows `failed` or `inactive`, this must be resolved (see Common Mistakes) before continuing.

### Step 6 — Open Jenkins on Port 8080

**What:** Access the Jenkins web interface from a browser.

**Why:** From this point on, setup is completed through the web UI, not the terminal.

**Action:** Open a browser and navigate to:

```text
http://localhost:8080
```

**Observe:** An **"Unlock Jenkins"** page loads, asking for an administrator password.

### Step 7 — Retrieve the Initial Admin Password

**What:** Read the one-time password Jenkins generated on first startup.

**Why:** This password is what proves the setup is being completed by someone with access to the server's filesystem, and it is required to get past the unlock screen.

**Command:**

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

**Action:** Copy the printed value and paste it into the "Unlock Jenkins" page.

**Observe:** Submitting the password moves the wizard forward to the plugin selection screen. An incorrect or incomplete value is rejected.

### Step 8 — Install Suggested Plugins

**What:** Choose "Install suggested plugins" on the setup wizard.

**Why:** This installs Jenkins's standard baseline plugin set, which a fresh install needs to be usable at all. No individual plugin is being configured or used here.

**Action:** Click **"Install suggested plugins"** and wait for the installation progress screen to finish.

**Observe:** A progress screen lists each plugin as it installs, ending with all items marked complete (or, occasionally, some marked failed — see Common Mistakes).

### Step 9 — Create the First Admin User

**What:** Replace the temporary unlock password with a real administrator account.

**Why:** The initial password from Step 7 is a one-time setup credential, not meant for ongoing logins — a proper admin user is needed for normal use.

**Action:** Fill in the requested username, password, full name, and email address on the "Create First Admin User" screen, then continue.

**Observe:** The wizard proceeds to the instance configuration screen without validation errors.

### Step 10 — Confirm the Jenkins URL

**What:** Accept (or adjust) the Jenkins URL shown on the "Instance Configuration" screen.

**Why:** This URL is what Jenkins will use to refer to itself (for example, in links it generates); the default is normally correct for a local install.

**Action:** Leave the pre-filled URL as-is (typically `http://localhost:8080/`) and click **Save and Finish**.

**Observe:** A "Jenkins is ready!" confirmation screen appears.

### Step 11 — Reach the Jenkins Dashboard

**What:** Enter Jenkins for the first time as the admin user.

**Why:** This is the completion point of this experiment — a working, logged-in Jenkins instance.

**Action:** Click **Start using Jenkins**.

**Observe:** The Jenkins dashboard loads, showing an empty job list and the left-hand navigation menu (New Item, Manage Jenkins, etc.).

## Observation / Verification

| Check | Where | Confirms |
|---|---|---|
| `java -version` | Terminal | A Jenkins-supported JDK is installed |
| `systemctl status jenkins` | Terminal | Jenkins service is `active (running)` |
| `http://localhost:8080` loads | Browser | Jenkins web server is reachable |
| Initial admin password file exists and is accepted | Terminal + Browser | Setup wizard can be unlocked |
| Suggested plugins finish installing | Browser | Baseline Jenkins functionality is present |
| Login with the created admin user succeeds | Browser | Admin account was created correctly |
| Jenkins dashboard loads with empty job list | Browser | Installation and setup completed successfully |
| `Manage Jenkins → System Information` shows a Jenkins version | Browser | Confirms the installed version end-to-end |

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Skipping or mismatching the Java version | Jenkins service fails to start | Install a supported LTS JDK (Step 1) before installing Jenkins |
| Forgetting to run `apt update` after adding the repository | `apt install jenkins` reports "package not found" | Run `sudo apt update` after adding the Jenkins repository |
| Checking the browser before checking service status | Browser shows "connection refused" with no explanation | Run `systemctl status jenkins` first; only open the browser once it is `active (running)` |
| Looking for the password in the wrong location | "No such file or directory" when reading the password | Use the exact path `/var/lib/jenkins/secrets/initialAdminPassword`, with `sudo` |
| Closing the browser mid-setup-wizard | Setup appears "stuck" or incomplete on reopening | Reopen `http://localhost:8080`; Jenkins resumes the wizard where it left off |
| Treating a failed plugin in Step 8 as a fatal error | Wizard shows one or two plugins failed | Jenkins allows continuing; failed plugins can be retried later from **Manage Jenkins → Plugins** — this is not part of this experiment's scope |

## Quick Reference

| Command / Action | Purpose |
|---|---|
| `java -version` | Check the installed Java version |
| Add Jenkins key + repo, then `apt update` | Make the `jenkins` package installable |
| `sudo apt install jenkins` | Install Jenkins |
| `sudo systemctl start jenkins` | Start the Jenkins service |
| `sudo systemctl enable jenkins` | Enable Jenkins to start on boot |
| `sudo systemctl status jenkins` | Check whether Jenkins is running |
| `http://localhost:8080` | Open the Jenkins web interface |
| `sudo cat /var/lib/jenkins/secrets/initialAdminPassword` | Retrieve the initial unlock password |
| Setup wizard → Install suggested plugins | Install Jenkins's standard baseline plugins |
| Setup wizard → Create First Admin User | Create a real login, replacing the one-time password |

## Result

Jenkins was installed and configured up to a working state: the Java prerequisite was satisfied, the Jenkins package repository was added, Jenkins was installed and started as a service, the initial admin password was used to unlock the setup wizard, the suggested plugins were installed, the first admin user was created, and the Jenkins dashboard was successfully reached. No jobs, pipelines, Jenkinsfiles, or GitHub integration were created — that work belongs to Experiment 05.
