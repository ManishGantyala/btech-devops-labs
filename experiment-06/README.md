# Experiment 06 – Explore Docker Commands for Content Management

## Aim

To explore Docker commands used for content management — obtaining images, creating and running containers, viewing and controlling container state, accessing and copying content, and removing containers and images.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain why Docker exists and what problem it solves compared to running an application directly on a machine.
- Explain what a Docker image and a Docker container are, and how they relate to each other.
- Explain how Docker was accessed in this experiment (Docker Desktop on Windows, via WSL2), and how that differs from a native Linux setup.
- Explain what "content management" means for a Docker image/container, in terms of the commands explored.
- Describe the purpose of each command explored: `docker --version`, `docker pull`, `docker images`, `docker run`, `docker ps`, `docker ps -a`, `docker exec`, `docker cp`, `docker inspect`, `docker logs`, `docker stop`, `docker start`, `docker rm`, `docker rmi`.
- Confirm, from this experiment's own work, that an image (`ubuntu:24.04`) was actually pulled and verified locally.

This experiment is scoped to Docker content-management commands only. Dockerfiles, Docker Compose, image publishing, orchestration, and in-depth networking/volumes are not part of this experiment.

## Requirements

- Windows with WSL2 enabled.
- Docker Desktop, using Docker version **29.6.2**.
- A terminal with Docker CLI access (via WSL2).

**Starting environment:** before this experiment's work began, the Docker environment already had other project work present on it — **4 containers (3 running, 1 stopped)** and **21 images**. The containers included (among others) `ad-agency-postgres`, `ad-agency-dev-control-plane`, and `petclinic-dev-control-plane`. These belong to other project work already on the machine — they were **not created for this experiment** and are noted here only because they were visible in the output of the commands used to check container/image state.

## Concept — Docker and Content Management

### Why Docker Exists

An application usually depends on a particular set of software, libraries, and configuration — a specific runtime version, particular system packages, specific environment variables. When an application is developed on one machine and then run on another (a teammate's machine, a test server, a production server), differences in that underlying setup can cause the application to behave differently or fail entirely, even though the application's own code hasn't changed. This is often summarized as "it works on my machine, but not on theirs."

**Docker** exists to address this problem. It lets an application be packaged together with the environment it needs — as a self-contained, isolated unit — so that it can run consistently regardless of what else is installed on the underlying machine.

### What Docker Is

Docker is a platform for building, running, and managing applications inside lightweight, isolated units. It has two parts a user interacts with:

- **Docker Engine** — the background service that actually creates and runs these isolated units on the machine.
- **Docker CLI** — the command-line tool (`docker ...`) used to instruct the Docker Engine — every command explored in this experiment is a Docker CLI command.

Two objects are central to this experiment:

- **Docker Image** — a read-only template containing an application (or, as in this experiment, a base operating system) and everything it needs to run. Images are typically obtained from a registry such as Docker Hub.
- **Docker Container** — a running (or stopped) instance created *from* an image. A container has its own writable layer on top of the image it came from, so changes made inside it don't alter the original image.

```text
Docker Image
      ↓
Docker Container
```

An image is the template; a container is what you get when that template is actually run.

### Environment Used for This Experiment

Docker can be used through more than one kind of setup, and this experiment's environment was one specific choice among them — not the only way Docker is used.

**Environment actually used in this experiment:**

```text
Windows
   ↓
WSL2
   ↕
Docker Desktop
   ↓
Docker Engine / Docker CLI
   ↓
Images / Containers
```

Here, Docker Desktop runs on Windows and uses WSL2 (Windows Subsystem for Linux) to provide the Linux environment Docker Engine needs. Docker CLI commands were run from a terminal, reaching the same Docker Engine underneath.

**Alternative: native Linux setup**, for contrast:

```text
Linux machine
      ↓
Docker Engine
      ↓
Docker CLI
      ↓
Images / Containers
```

A student working directly on a Linux machine would install Docker Engine natively, without needing WSL2 or Docker Desktop as an intermediate layer. Either way, the Docker CLI commands explored in this experiment — and what they mean for images and containers — are the same.

Installing/setting up Docker itself is a separate concern from this experiment; this experiment assumes Docker is already available (as it was here, via Docker Desktop + WSL2) and focuses only on exploring content-management commands against it.

### What "Content Management" Means in This Experiment

With images and containers established, "content management" refers to the set of operations used to obtain, run, inspect, move, and clean up that content:

| Concern | Role | Relevant command(s) |
|---|---|---|
| Obtaining an image | Downloading a template from a registry | `docker pull` |
| Viewing images | Seeing what image templates already exist locally | `docker images` |
| Creating/running a container | Turning an image into a live instance | `docker run` |
| Viewing container state | Seeing which containers are running or stopped | `docker ps`, `docker ps -a` |
| Accessing a running container | Running commands directly inside a live container | `docker exec` |
| Copying content | Moving files between the host machine and a container | `docker cp` |
| Inspecting Docker objects | Viewing detailed configuration/metadata of an image or container | `docker inspect` |
| Viewing container logs | Reviewing a container's process output | `docker logs` |
| Stopping/starting containers | Controlling a container's running state without removing it | `docker stop`, `docker start` |
| Removing containers | Deleting a container that is no longer needed | `docker rm` |
| Removing images | Deleting an image that is no longer needed | `docker rmi` |

The practical procedure below walks through these, in the order they were explored, checking the CLI version first (`docker --version`).

## Procedure

Steps 1–5 were **actually performed** — they have real commands and real observed output from this experiment. Steps 6, 7, and 9–12 are marked **"Explored conceptually"** — they document what each command does and when it is used, but no specific invocation or container name was recorded for this experiment's session. Step 8 (`docker cp`) was partially carried out: `content.txt` in this experiment's directory is a real artifact from working with content transfer between host and container, but the exact commands and container name were not recorded — Step 8's status label reflects this. When working through this experiment yourself, try each conceptual command against the `ubuntu:24.04` container you create, so you see the real output rather than only reading the description.

### Step 1 — Check the Docker Version

**Status:** Actually performed.

**What:** Confirm the Docker CLI is available and check its version.

**Why:** A baseline check before running any other Docker command.

**Command/Action:**

```bash
docker --version
```

**Observe:** Docker reported version **29.6.2** in this environment.

### Step 2 — View the Existing Local Images

**Status:** Actually performed.

**What:** List the images already present locally, before pulling anything new.

**Why:** Establishes the starting point, so a later pull can be seen as an actual change rather than assumed.

**Command/Action:**

```bash
docker images
```

**Observe:** **21 images** were already present locally, from other project work on this machine — not images created by this experiment. The count on your own machine will differ; what matters is noting the count *before* the pull in Step 4, so you can confirm exactly one new image was added afterward.

### Step 3 — View the Existing Containers

**Status:** Actually performed.

**What:** List all containers, both running and stopped.

**Why:** `docker ps` alone only shows running containers; `docker ps -a` is needed to see the full picture, including stopped ones.

**Command/Action:**

```bash
docker ps
docker ps -a
```

**Observe:** **4 containers** existed at this point — **3 running, 1 stopped** — including (among others) `ad-agency-postgres`, `ad-agency-dev-control-plane`, and `petclinic-dev-control-plane`. These belong to other project work already on the machine, not to this experiment. Your own output will show different containers depending on what is already running on your system.

### Step 4 — Pull the Ubuntu 24.04 Image

**Status:** Actually performed.

**What:** Download the Ubuntu 24.04 image from Docker Hub.

**Why:** This is the concrete "obtaining an image" operation for this experiment, demonstrating `docker pull` for real rather than as a conceptual example.

**Command/Action:**

```bash
docker pull ubuntu:24.04
```

**Observe:** The pull completed successfully. Docker reported download progress on the order of **119 MB / 31.7 MB** during the operation. The first number is the uncompressed size of the image content; the second is the compressed size actually transferred over the network — Docker stores and transmits images in compressed layers and decompresses them locally. The resulting local image was:

```text
Repository: ubuntu
Tag:        24.04
Image ID:   33ceb71981b6...
```

### Step 5 — Confirm the Pulled Image Locally

**Status:** Actually performed.

**What:** List local images again to confirm the pull.

**Why:** Verifies the new image is now stored locally, alongside the 21 that were already present.

**Command/Action:**

```bash
docker images
```

**Observe:** The `ubuntu:24.04` image, with image ID beginning `33ceb71981b6`, now appears in the local image list.

### Step 6 — `docker run`

**Status:** Explored conceptually — no specific execution captured in this experiment's record.

**What:** `docker run` creates and starts a new container from a local image.

**Why:** This is how an image (a static template) becomes a container (a live instance) — the step that turns "having an image" into "having something to work with."

**Command/Action:** Conceptually, `docker run <image>` creates a container from the given image and starts it, optionally with flags controlling interactivity, naming, and other options.

**Observe:** No specific `docker run` invocation, container name, or resulting container ID from this experiment's own work is recorded here.

### Step 7 — `docker exec`

**Status:** Explored conceptually — no specific execution captured in this experiment's record.

**What:** `docker exec` runs a command inside an already-running container, most commonly to open a shell into it.

**Why:** This is how content *inside* a running container is accessed directly, without stopping or restarting it.

**Command/Action:** Conceptually, `docker exec -it <container> <command>` runs `<command>` inside the named/ID'd running container.

**Observe:** No specific container name or session output from this experiment's own work is recorded here.

### Step 8 — `docker cp`

**Status:** Explored conceptually, with one supporting artifact.

**What:** `docker cp` copies files or directories between the host machine and a container's filesystem, in either direction.

**Why:** This is the main mechanism for moving content in or out of a container without going through the container's own running processes.

**Command/Action:** Conceptually, `docker cp <src> <container>:<dest>` (host → container) or `docker cp <container>:<src> <dest>` (container → host).

**Observe:** This experiment's directory contains `content.txt`, whose content —

```text
Docker Content Management Experiment
Updated from Docker host
```

— is an artifact from exploring content transfer between the host and a container. The workflow that produced it was:

```bash
# Copy content.txt from the host into a running container
docker cp content.txt <container-name>:/tmp/content.txt

# Verify it arrived inside the container
docker exec <container-name> cat /tmp/content.txt

# Copy it back out again
docker cp <container-name>:/tmp/content.txt ./content_from_container.txt
```

Replace `<container-name>` with the name or ID of your running container (visible in `docker ps`). The exact container name used in this experiment's own session was not recorded, so the commands above use a placeholder.

### Step 9 — `docker inspect`

**Status:** Explored conceptually — no specific execution captured in this experiment's record.

**What:** `docker inspect` returns detailed, low-level metadata about an image or container — configuration, filesystem layers, and other settings.

**Why:** This is the command used to look inside an image's or container's configuration, beyond what `docker images`/`docker ps` summarize.

**Command/Action:** Conceptually, `docker inspect <image-or-container>`.

**Observe:** No specific inspect output from this experiment's own work is recorded here.

### Step 10 — `docker logs`

**Status:** Explored conceptually — no specific execution captured in this experiment's record.

**What:** `docker logs` displays the output a container's main process has produced.

**Why:** This is how a container's activity is reviewed without needing to `exec` into it.

**Command/Action:** Conceptually, `docker logs <container>`.

**Observe:** No specific log output from this experiment's own work is recorded here.

### Step 11 — `docker stop` / `docker start`

**Status:** Explored conceptually — no specific execution captured in this experiment's record.

**What:** `docker stop` halts a running container; `docker start` restarts a stopped one without recreating it.

**Why:** These commands control a container's running state, distinct from creating (`docker run`) or removing (`docker rm`) it.

**Command/Action:** Conceptually, `docker stop <container>` and `docker start <container>`.

**Observe:** No specific container was stopped/started as a captured result of this experiment's own work.

### Step 12 — `docker rm` / `docker rmi`

**Status:** Explored conceptually — no specific execution captured in this experiment's record.

**What:** `docker rm` removes a (stopped) container; `docker rmi` removes an image.

**Why:** These are the cleanup commands. Both have a dependency rule: a running container must be stopped before it can be removed, and an image still used by a container can't be removed until that container is gone.

**Command/Action:** Conceptually, `docker rm <container>` and `docker rmi <image>`.

**Observe:** No container or image was removed as a captured result of this experiment's own work.

## Observation / Verification

| Check | Where | Confirms |
|---|---|---|
| Docker CLI available | `docker --version` | Reported version 29.6.2 |
| Starting image count | `docker images` | 21 images present before the pull |
| Starting container state | `docker ps` / `docker ps -a` | 4 containers total — 3 running, 1 stopped |
| Ubuntu image pulled | `docker pull ubuntu:24.04` | Completed successfully, ~119 MB / 31.7 MB reported |
| Pulled image present locally | `docker images` | `ubuntu`, tag `24.04`, image ID beginning `33ceb71981b6` |
| Host↔container content transfer | *(concept, with artifact)* | `content.txt` in this experiment's directory reflects work done on this topic |

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Using `docker ps` alone to check for containers | Stopped containers appear to not exist | Use `docker ps -a` to include stopped containers |
| Confusing `docker images` with `docker ps` | Looking for a container in the image list, or vice versa | Images are templates (`docker images`); containers are running/stopped instances (`docker ps`/`docker ps -a`) |
| Trying to `docker rm` a running container | "container is running" error | Stop it first with `docker stop`, then `docker rm` |
| Trying to `docker rmi` an image still in use | "image is being used by a container" error | Remove the dependent container first, then remove the image |
| Assuming a fresh environment | Miscounting new work against unrelated pre-existing containers/images | Check `docker ps -a` / `docker images` first to see what already exists, as in Steps 2–3 |

## Quick Reference

| Command / Action | Purpose |
|---|---|
| `docker --version` | Check the installed Docker CLI version |
| `docker pull <image>` | Download an image from a registry |
| `docker images` | List locally stored images |
| `docker run <image>` | Create and start a container from an image |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers, including stopped ones |
| `docker exec -it <container> <cmd>` | Run a command inside a running container |
| `docker cp <src> <dest>` | Copy content between host and container |
| `docker inspect <target>` | View detailed metadata about an image or container |
| `docker logs <container>` | View a container's output |
| `docker stop <container>` | Stop a running container |
| `docker start <container>` | Start a stopped container |
| `docker rm <container>` | Remove a container |
| `docker rmi <image>` | Remove an image |

## Result

The Docker environment used for this experiment (Docker Desktop with WSL2 on Windows, Docker version 29.6.2) already contained 4 containers (3 running, 1 stopped) and 21 images from other project work, confirmed via `docker ps` / `docker ps -a` and `docker images` before any new work began. The Ubuntu 24.04 image was then actually pulled with `docker pull ubuntu:24.04`, completing successfully and adding `ubuntu:24.04` (image ID beginning `33ceb71981b6`) to the local image list, confirmed by re-running `docker images`. The remaining content-management commands — `docker run`, `docker exec`, `docker cp`, `docker inspect`, `docker logs`, `docker stop`, `docker start`, `docker rm`, and `docker rmi` — were explored at the concept level as documented above; beyond the `content.txt` artifact tied to the `docker cp` topic, no specific invocations, container names, or outputs for these commands are part of this experiment's recorded results.
