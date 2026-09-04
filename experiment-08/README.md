# Experiment 08 – Deploy the Dockerized Application to Kubernetes

## Aim

To deploy the Docker image built in Experiment 07 (`techfest-app:v2`) into a local Kubernetes cluster, using a Deployment and a NodePort Service.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain why Kubernetes is introduced after Docker, and what problem it solves that Docker alone does not.
- Explain the relationship between a Docker image, a Pod, and a container running inside that Pod.
- Explain what a Kubernetes Deployment is, and why it is used instead of managing a Pod directly.
- Explain the role of `replicas`, `labels`, and `selectors` in a Deployment.
- Explain what a Kubernetes Service is, why it's needed, and the difference between `port` and `targetPort`.
- Explain what a `NodePort` Service does.
- Explain why `imagePullPolicy: Never` matters when using a local image with a local cluster.
- Read `experiment-08/deployment.yaml` and `experiment-08/service.yaml` and explain what each field configures.

This experiment reuses the image built in Experiment 07 (`techfest-app:v2`) rather than building a new one — Experiment 08 is about deployment, not application changes.

## Requirements

- The Docker image `techfest-app:v2`, built in Experiment 07.
- A local Kubernetes cluster. This experiment's manifests (`imagePullPolicy: Never`, no registry reference on the image) are written for a **local, single-node cluster where the image is already available to the node** — the pattern used by tools such as Kind (Kubernetes in Docker). The exact cluster setup/name used is not part of this experiment's recorded evidence and is not claimed here.
- `kubectl`, configured against that cluster.

## Concept

### Why Kubernetes Comes After Docker

Experiment 07 produced a Docker image and ran it directly as a single container with `docker run`. That works for one container on one machine, but it doesn't handle things like: keeping a container running if it crashes, running more than one copy of it, or giving it a stable way to be reached without hardcoding a specific container's details. **Kubernetes** is introduced at this point to manage *how containers built from an image are run*, rather than running them by hand with `docker run`.

### Docker Image vs. Kubernetes Pod

A Docker **image** (`techfest-app:v2`) is still the same static template it was in Experiment 07. In Kubernetes, that image isn't run directly — it's run inside a **Pod**, which is the smallest unit Kubernetes manages. A Pod wraps one or more containers (here, one) and is what Kubernetes actually schedules, monitors, and restarts if needed.

### What a Deployment Is, and Why Not Just a Pod

A **Deployment** is a Kubernetes object that describes the *desired state* of a set of Pods — which image to run, how many copies, and how to identify them — and continuously works to keep the real state matching that description. Managing a Pod directly means if it dies, it's simply gone; a Deployment notices and creates a replacement automatically. This experiment's Deployment is named `techfest-app`.

### Replicas

`replicas: 1` tells the Deployment to keep exactly one Pod running from this template. Even with just one replica, using a Deployment (rather than a bare Pod) still gets the benefit of Kubernetes recreating it if it fails.

### Labels and Selectors

- The Deployment's Pod template gives each Pod it creates the label `app: techfest-app`.
- The Deployment's `selector.matchLabels` (`app: techfest-app`) tells the Deployment which Pods belong to it — it must match the Pod template's labels, or the Deployment won't recognize its own Pods.
- The Service (below) uses the same label, `app: techfest-app`, as *its* selector — this is how the Service finds which Pods to send traffic to. Labels and selectors are the mechanism connecting the Service to the Deployment's Pods; they aren't linked by name.

### What a Service Is, and Why It's Needed

A Pod's own address can change if it's recreated (for example, if the Deployment replaces it after a failure). A Kubernetes **Service** gives a stable way to reach whichever Pod(s) currently match its selector, without needing to track individual Pod addresses. This experiment's Service is named `techfest-service`.

### `port` vs. `targetPort`

- `targetPort: 80` is the port the *container* is actually listening on (matching `containerPort: 80` in the Deployment — this is Nginx, same as Experiment 07).
- `port: 80` is the port the *Service itself* exposes, for anything routing through the Service, inside the cluster.

### What NodePort Means

`type: NodePort` makes the Service additionally reachable from outside the cluster, on a port opened on the cluster node itself. Kubernetes assigns this NodePort (from a reserved range) unless one is explicitly specified in the manifest — this manifest does not specify one, so the actual assigned NodePort is determined by the cluster at apply time and is not something to assume or fabricate in advance.

### Why `containerPort: 80`

The container image is the same Nginx-based image from Experiment 07, and Nginx listens on port 80 by default inside the container — `containerPort: 80` simply declares that.

### Why This Experiment Reuses `techfest-app:v2`

Experiment 07 already produced a working image with the current application content. Experiment 08's purpose is to deploy that existing image into Kubernetes — it is not about changing the application again, so no new image is built here.

### Why `imagePullPolicy: Never` Matters

By default, Kubernetes tries to *pull* an image from a registry. `techfest-app:v2` was built locally with `docker build` in Experiment 07 and was never pushed anywhere — there is no registry copy to pull. `imagePullPolicy: Never` tells Kubernetes not to attempt a pull at all, and instead expect the image to already exist wherever the Pod is scheduled. In a local setup like Kind, this means the image must already be available to the cluster's node(s) — otherwise the Pod cannot start.

### Overall Architecture

```text
Docker image
    ↓
Kubernetes Deployment
    ↓
Pod
    ↓
Container
    ↓
Kubernetes Service
    ↓
NodePort
    ↓
Application
```

With this experiment's actual names:

```text
techfest-app:v2
    ↓
Deployment: techfest-app
    ↓
1 Pod
    ↓
containerPort: 80
    ↓
Service: techfest-service
    ↓
NodePort
```

## Manifest Explanation

### `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: techfest-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: techfest-app
  template:
    metadata:
      labels:
        app: techfest-app
    spec:
      containers:
        - name: techfest-app
          image: techfest-app:v2
          imagePullPolicy: Never
          ports:
            - containerPort: 80
```

| Field | Value | Meaning |
|---|---|---|
| `metadata.name` | `techfest-app` | Name of the Deployment object |
| `spec.replicas` | `1` | One Pod is kept running |
| `spec.selector.matchLabels` | `app: techfest-app` | How the Deployment identifies Pods as its own |
| `template.metadata.labels` | `app: techfest-app` | Label applied to Pods this Deployment creates |
| `containers[0].image` | `techfest-app:v2` | The Experiment 07 image being deployed |
| `containers[0].imagePullPolicy` | `Never` | Never attempt to pull from a registry; the image must already be local to the node |
| `containers[0].ports[0].containerPort` | `80` | Port Nginx listens on inside the container |

### `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: techfest-service
spec:
  selector:
    app: techfest-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

| Field | Value | Meaning |
|---|---|---|
| `metadata.name` | `techfest-service` | Name of the Service object |
| `spec.selector` | `app: techfest-app` | Selects Pods with this label — matches the Deployment's Pod label |
| `ports[0].protocol` | `TCP` | Transport protocol |
| `ports[0].port` | `80` | Port the Service exposes inside the cluster |
| `ports[0].targetPort` | `80` | Port on the Pod/container that traffic is forwarded to |
| `spec.type` | `NodePort` | Also exposes the Service on a port on the cluster node, for access from outside the cluster |

## Prerequisites — Kind Cluster Setup

This experiment uses **Kind** (Kubernetes in Docker) as the local cluster tool. The cluster must exist and the `techfest-app:v2` image must be loaded into it before applying the manifests.

**Create the Kind cluster** (one-time, if not already created):

```bash
kind create cluster --name experiment-08
```

**Confirm the cluster is running:**

```bash
kubectl get nodes
```

**Expected output:**

```text
NAME                          STATUS   ROLES           AGE
experiment-08-control-plane   Ready    control-plane   ...
```

**Load the image into the Kind node:**

```bash
kind load docker-image techfest-app:v2 --name experiment-08
```

Kind runs its node as a Docker container with its own image store, separate from the host's Docker daemon. `kind load docker-image` makes `techfest-app:v2` available inside the cluster node, which is required because `imagePullPolicy: Never` is set — Kubernetes will not attempt a registry pull.

---

## Procedure

### Step 1 — Confirm `techfest-app:v2` Is Available Locally

**Status:** Conceptual (dependent step; no captured command/output for this specific check in this experiment's record).

**What:** Confirm the `techfest-app:v2` image built in Experiment 07 exists locally, and is available to the Kubernetes node.

**Why:** Because `imagePullPolicy: Never` is set, the Pod will fail to start if this image isn't already present where the Pod is scheduled — this is the precondition the rest of the experiment depends on.

**Action/Command:** Conceptually, `docker images` would confirm `techfest-app:v2` exists; for a Kind cluster specifically, the image additionally needs to be made available to the Kind node (for example, via `kind load docker-image`), since Kind runs its node as a separate Docker container with its own image store.

**Observe:** Not established by the available project evidence — documented at the concept level.

### Step 2 — Apply `deployment.yaml`

**Status:** Conceptual (command implied by the experiment's stated purpose; exact execution output not captured).

**What:** Submit the Deployment manifest to the cluster.

**Why:** This is what actually creates the Deployment object and, through it, the Pod running `techfest-app:v2`.

**Action/Command:**

```bash
kubectl apply -f deployment.yaml
```

**Observe:** Not established by the available project evidence — no captured `kubectl` output is recorded for this step.

### Step 3 — Apply `service.yaml`

**Status:** Conceptual (command implied by the experiment's stated purpose; exact execution output not captured).

**What:** Submit the Service manifest to the cluster.

**Why:** This creates `techfest-service`, giving the Pod(s) matching `app: techfest-app` a stable, NodePort-exposed access point.

**Action/Command:**

```bash
kubectl apply -f service.yaml
```

**Observe:** Not established by the available project evidence.

### Step 4 — Check the Deployment and Pod

**Status:** Conceptual — no captured output recorded.

**What:** Check that the Deployment created its Pod, and that the Pod is running.

**Why:** Confirms the Deployment's desired state (1 replica of `techfest-app:v2`) was actually achieved.

**Action/Command:**

```bash
kubectl get deployments
kubectl get pods
```

**Observe:** No specific Pod name or status output from this experiment's own work is recorded here.

### Step 5 — Check the Service

**Status:** Conceptual — no captured output recorded.

**What:** Check the Service and the NodePort Kubernetes assigned it.

**Why:** The actual NodePort is assigned by Kubernetes at apply time (since none is specified in `service.yaml`), so it can only be known by checking the running Service, not assumed in advance.

**Action/Command:**

```bash
kubectl get service techfest-service
```

**Observe:** No specific NodePort value from this experiment's own work is recorded here.

### Step 6 — Access/Verify the Application

**Status:** Conceptual — no captured output recorded.

**What:** Reach the application through the cluster node's IP/hostname and the NodePort from Step 5.

**Why:** This is the final confirmation that the Deployment and Service together make the application reachable, matching the architecture diagram above.

**Action/Command:** Conceptually, open `http://<node-address>:<node-port>` in a browser.

**Observe:** No specific IP address, NodePort number, or browser result from this experiment's own work is recorded here.

## Observation / Verification

| Check | Evidence | Confirms |
|---|---|---|
| Deployment named `techfest-app`, 1 replica, image `techfest-app:v2` | `experiment-08/deployment.yaml` (configuration evidence) | Deployment is correctly configured to run the Experiment 07 image |
| `imagePullPolicy: Never` set | `experiment-08/deployment.yaml` (configuration evidence) | Cluster is expected to use the already-local image, not pull one |
| Pod label `app: techfest-app` matches Deployment selector | `experiment-08/deployment.yaml` (configuration evidence) | Deployment will correctly recognize its own Pods |
| Service selector `app: techfest-app` matches Pod label | `experiment-08/service.yaml` (configuration evidence) | Service will correctly route to the Deployment's Pod(s) |
| Service `targetPort: 80` matches container's `containerPort: 80` | Both manifests (configuration evidence) | Traffic forwarded by the Service reaches the port Nginx listens on |
| Service `type: NodePort` | `experiment-08/service.yaml` (configuration evidence) | Service is configured for external, node-level access |
| Deployment/Pod actually running in the cluster | *(runtime evidence — see Experiment 09)* | Experiment 09's Step 1 baseline check shows `techfest-app` Deployment at `1/1`, Pod `techfest-app-6c98cc6db8-bzlvx` `Running`, on node `experiment-08-control-plane` |
| Service assigned a working NodePort, application reachable | *(runtime evidence — see Experiment 09)* | Experiment 09's Step 1 shows `techfest-service` with NodePort `80:30576/TCP`, Cluster-IP `10.96.184.50` |

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `techfest-app:v2` not available to the Kind node | Pod stuck in `ImagePullBackOff` or `ErrImageNeverPull` | Ensure the image is loaded into the Kind node (e.g. `kind load docker-image`) before applying the Deployment |
| Misunderstanding `imagePullPolicy: Never` | Assuming Kubernetes will fetch the image automatically | `Never` means Kubernetes will not pull under any circumstance — the image must already be local to the node |
| Deployment image name/tag mismatch | Pod fails to start, or runs an unexpected version | Confirm `image: techfest-app:v2` matches the image actually built/loaded |
| Deployment selector and Pod template labels not matching | Deployment reports 0 matching Pods despite Pods existing | Keep `spec.selector.matchLabels` and `template.metadata.labels` identical (`app: techfest-app`, as here) |
| Service selector not matching Pod labels | Service has no endpoints; application unreachable through it | Keep the Service's `selector` identical to the Pod's labels (`app: techfest-app`, as here) |
| Confusing `port` and `targetPort` | Requests reach the Service but not the container, or vice versa | `port` is the Service's own port; `targetPort` is the container's port — here both happen to be 80 |
| Assuming NodePort is externally port 80 | Trying to access the app on port 80 directly and failing | NodePort is a separate, Kubernetes-assigned port (unless explicitly set) — it must be looked up with `kubectl get service`, not assumed |
| Expecting Kubernetes to rebuild the image after a source change | Editing application files and expecting the Deployment to reflect it | As in Experiment 07, a new image must be built (and a new tag/rollout used) — Kubernetes only runs the image it's told to |

## Quick Reference

| Resource / Command | Purpose |
|---|---|
| `deployment.yaml` | Defines the `techfest-app` Deployment (1 replica, `techfest-app:v2`, `imagePullPolicy: Never`) |
| `service.yaml` | Defines the `techfest-service` NodePort Service (port 80 → targetPort 80) |
| `kubectl apply -f deployment.yaml` | Create/update the Deployment from the manifest |
| `kubectl apply -f service.yaml` | Create/update the Service from the manifest |
| `kubectl get deployments` | Check Deployment status |
| `kubectl get pods` | Check Pod status |
| `kubectl get service techfest-service` | Check the Service and its assigned NodePort |

## Result

The Docker image `techfest-app:v2`, built in Experiment 07, was configured for deployment to a local Kubernetes cluster using a Deployment named `techfest-app` (1 replica, `imagePullPolicy: Never`, `containerPort: 80`) and a `NodePort` Service named `techfest-service` (selecting `app: techfest-app`, `port: 80` → `targetPort: 80`), as defined in `experiment-08/deployment.yaml` and `experiment-08/service.yaml`. These manifests are consistent with each other — the Service's selector matches the Deployment's Pod labels, and its `targetPort` matches the container's `containerPort`. Actual cluster application (`kubectl apply`), the resulting Pod's status, the Service's assigned NodePort, and a verified application access result are not established by the available project evidence and are documented above at the concept level rather than claimed as performed.
