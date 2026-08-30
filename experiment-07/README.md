# Experiment 07 – Build and Run an Application Using a Dockerfile, Then Create a New Image Version After Modifying the Application

## Aim

To containerize an application using a Dockerfile, build and run it as a Docker image/container, then modify the application and build a new image version to reflect that change.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain what a Dockerfile is and how it turns application source into a Docker image.
- Explain why this experiment's application is served using Nginx.
- Build a Docker image from a Dockerfile and run a container from it.
- Explain why an already-built image does not automatically reflect a later source change.
- Build a new, separately tagged image version after modifying the application, and run it as a new container.
- Verify two different versions of the same application, served from two different containers on different ports.

This experiment follows Experiment 06 (exploring Docker content-management commands) and applies those ideas to a real build-and-version workflow.

## Requirements

- Docker (as set up and explored in Experiment 06 — Docker Desktop with WSL2).
- The application source used in earlier experiments (`index.html`, `style.css`, `script.js`) and a `Dockerfile`, present in this experiment's directory.
- A web browser, to verify the running application.

## Concept

### Why a Dockerfile Is Needed

A Docker image has to be built from *something* — a set of instructions describing what base environment to start from and what application files to include. A **Dockerfile** is that set of instructions: a plain text file that Docker reads to build an image automatically, instead of a person manually installing a web server and copying files into it every time.

### What a Dockerfile Is, and How It Becomes an Image

This experiment's Dockerfile is:

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
```

- `FROM nginx:alpine` starts the image from an existing, pre-built Nginx image, rather than building a web server from scratch.
- Each `COPY` instruction places one of the application's files into Nginx's default folder for served content (`/usr/share/nginx/html/`).

Running `docker build` against this file produces a Docker **image** — a fixed snapshot containing Nginx plus this application's files, ready to be run.

### Why Nginx

Nginx is used here as the web server that actually serves the application's static files (`index.html`, `style.css`, `script.js`) once the container is running. The application itself (from earlier experiments) is a static HTML/CSS/JS page with no server-side logic, so a plain web server is all that's needed to make it reachable over HTTP.

### From Image to Container

An **image** is a static template; a **container** is a running instance created from it with `docker run`. Multiple containers can be run from the same image, and — as this experiment shows — a new image version produces a container that behaves differently from one made from an older image version.

### Image Versioning with Tags

Each image build in this experiment is given a version **tag** — `v1`, then later `v2` — as part of its name (`techfest-app:v1`, `techfest-app:v2`). This keeps the two builds distinguishable and lets both exist locally at the same time, rather than one silently overwriting the other.

### Why Changing the Application Does Not Change an Existing Image

An image is a snapshot taken at build time. Editing `index.html`, `style.css`, or `script.js` afterward changes only the files on disk — it does **not** change any image already built from them, and it does **not** change any container already running from that image. The only way for the change to reach an image is to run `docker build` again, which is why this experiment builds a second, separately tagged image (`v2`) after modifying the application, rather than expecting the `v1` container to somehow pick up the change.

### Overall Flow of This Experiment

**Initial build and run:**

```text
Application Source
      ↓
Dockerfile
      ↓
docker build
      ↓
techfest-app:v1
      ↓
docker run
      ↓
techfest-container
      ↓
Application served by Nginx
```

**After modifying the application:**

```text
Modify Application
      ↓
docker build
      ↓
techfest-app:v2
      ↓
docker run
      ↓
techfest-container-v2
      ↓
Updated Application on port 8081
```

## Procedure

### Step 1 — Prepare the Application and Dockerfile

**What:** Place the application files (`index.html`, `style.css`, `script.js`) and the `Dockerfile` above together in the experiment's directory.

**Why:** `docker build` needs the Dockerfile and the files it references (via `COPY`) to be available together, in the same build context.

**Action/Command:** No build command yet — this step is the file layout the later `docker build` commands depend on.

**Observe:** `experiment-07/` contains `Dockerfile`, `index.html`, `style.css`, and `script.js`.

### Step 2 — Build `techfest-app:v1`

**What:** Build the first Docker image from the Dockerfile.

**Why:** This turns the application source and the Dockerfile's instructions into a runnable image, tagged `v1`.

**Action/Command:**

```bash
docker build -t techfest-app:v1 .
```

**Observe:** The build completes, and `techfest-app:v1` appears in the local image list (`docker images`).

### Step 3 — Run `techfest-container`

**What:** Run a container from the `techfest-app:v1` image, named `techfest-container`.

**Why:** This is what actually starts Nginx and makes the application reachable, rather than just having it as an unstarted image.

**Action/Command:**

```bash
docker run -d --name techfest-container -p <host-port>:80 techfest-app:v1
```

*(Nginx listens on port 80 inside the container by default; the specific host-side port mapped for `techfest-container` is not part of the supplied record and is left as `<host-port>` here rather than invented.)*

**Observe:** `techfest-container` appears as a running container (`docker ps`).

### Step 4 — Verify the Application Through Nginx

**What:** Open the application in a browser, through the running `techfest-container`.

**Why:** Confirms the image build and container run actually produced a working, servable application — not just a container that exists.

**Action/Command:** Open the mapped host port for `techfest-container` in a browser.

**Observe:** The registration page loads, served by Nginx from inside the container.

### Step 5 — Modify the Application

**What:** Change the application's source.

**Why:** This is the change that the next image version (`v2`) needs to be built to reflect.

**Action/Command:** No command — this is an edit to the application source files.

**Observe:** Comparing the application files against their earlier form (as in Experiment 01), the page heading was changed:

```text
- TechFest 2026 - Event Registration
+ TechFest 2026 - Docker Containerized Application
```

This is the modification reflected in the current `index.html` in this experiment's directory.

### Step 6 — Build `techfest-app:v2`

**What:** Build a new image from the same Dockerfile, now reading the modified application files, tagged `v2`.

**Why:** As established in the Concept section, the running `techfest-container` (from `v1`) does not pick up this change on its own — a new image has to be built from the updated source.

**Action/Command:**

```bash
docker build -t techfest-app:v2 .
```

**Observe:** The build completes, and `techfest-app:v2` appears in the local image list alongside `techfest-app:v1`.

### Step 7 — Run `techfest-container-v2`

**What:** Run a new container from the `techfest-app:v2` image, named `techfest-container-v2`, mapped to port 8081.

**Why:** A new container is needed to actually run the new image version; mapping it to a different host port (8081) lets it run alongside `techfest-container` without a port conflict.

**Action/Command:**

```bash
docker run -d --name techfest-container-v2 -p 8081:80 techfest-app:v2
```

**Observe:** `techfest-container-v2` appears as a running container (`docker ps`), separate from `techfest-container`.

### Step 8 — Verify Port 8081 Mapping

**What:** Confirm `techfest-container-v2` is reachable on port 8081.

**Why:** This is what proves the `-p 8081:80` mapping in Step 7 actually took effect.

**Action/Command:** Open `http://localhost:8081` in a browser.

**Observe:** The application loads via port 8081.

### Step 9 — Verify the Updated Application Is Being Served

**What:** Confirm the page loaded on port 8081 reflects the Step 5 modification.

**Why:** This is the final check that `v2` genuinely serves the updated application, and not a stale copy.

**Action/Command:** Inspect the loaded page's heading at `http://localhost:8081`.

**Observe:** The heading reads "TechFest 2026 - Docker Containerized Application," matching the modified `index.html`, confirming `techfest-container-v2` is serving the updated application.

## Observation / Verification

| Check | Where | Confirms |
|---|---|---|
| `techfest-app:v1` exists | `docker images` | The first image was built successfully |
| `techfest-container` runs | `docker ps` | A container was started from `techfest-app:v1` |
| Application is served (v1) | Browser, via `techfest-container` | Nginx is serving the application from the `v1` image |
| Application source modified | `experiment-07/index.html` | Heading changed to "TechFest 2026 - Docker Containerized Application" |
| `techfest-app:v2` exists | `docker images` | A second image was built after the modification |
| `techfest-container-v2` runs | `docker ps` | A new container was started from `techfest-app:v2` |
| Port 8081 serves the updated application | Browser, `http://localhost:8081` | `techfest-container-v2` correctly serves the modified application |

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Rebuilding an image without changing the tag | The old version is silently overwritten, with no way to compare v1 and v2 | Give each build a distinct tag, as with `v1` and `v2` here |
| Expecting `techfest-container` to show the modified application | The running v1 container still serves the old heading after editing the source | A running container does not re-read the source; a new image must be built and run |
| Confusing an image with a container | Trying to "run" or "access" `techfest-app:v2` directly as if it were live | An image must be started with `docker run` to become a running container |
| Port conflicts | `docker run` for `techfest-container-v2` fails if its host port is already in use | Map `techfest-container-v2` to a free port (8081, as used here), separate from `techfest-container`'s port |
| Running the wrong image version | Port 8081 unexpectedly shows the old heading | Confirm the container was run from `techfest-app:v2`, not `techfest-app:v1` |
| Skipping verification after the rebuild | Assuming the update worked without checking | Always reload the page and check the content, as in Steps 4 and 9 |

## Quick Reference

| Command | Purpose |
|---|---|
| `docker build -t techfest-app:v1 .` | Build the first image version from the Dockerfile |
| `docker run -d --name techfest-container -p <port>:80 techfest-app:v1` | Run a container from the v1 image |
| `docker build -t techfest-app:v2 .` | Build a new image version after modifying the application |
| `docker run -d --name techfest-container-v2 -p 8081:80 techfest-app:v2` | Run a new container from the v2 image, on port 8081 |
| `docker images` | Confirm both `techfest-app:v1` and `techfest-app:v2` exist locally |
| `docker ps` | Confirm `techfest-container` and `techfest-container-v2` are both running |

## Result

The application from earlier experiments was containerized using a Dockerfile based on `nginx:alpine`, and built into a first image, `techfest-app:v1`. A container, `techfest-container`, was run from that image, and the application was verified as being served through Nginx. The application source was then modified — the page heading was changed to "TechFest 2026 - Docker Containerized Application" — and, because the running `v1` container does not reflect source changes on its own, a new image, `techfest-app:v2`, was built from the updated source. A new container, `techfest-container-v2`, was run from that image on port 8081, and the updated application was verified as being correctly served at `http://localhost:8081`, demonstrating the full flow from application source through a Dockerfile to a versioned image and container, and how that flow repeats after a source change.
