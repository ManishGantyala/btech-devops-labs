# Experiment 09 – Automate the Process of Running the Containerized Application (Exercise 7) Using Kubernetes

## Aim

To use Kubernetes to automate the running of the Exercise 7 containerized application (`techfest-app:v2`), by reusing the Deployment defined in Experiment 08 and observing how Kubernetes maintains that Deployment's desired state automatically, rather than the application being started and monitored manually.

## Learning Objectives

By the end of this experiment, a student should be able to:

- Explain the difference between running a container manually (`docker run`) and having Kubernetes manage that container's execution.
- Explain what "desired state" means in Kubernetes, and how a Deployment describes it.
- Explain how a Deployment automates Pod management, including the role of `replicas`.
- Explain Kubernetes's self-healing behavior — what a Deployment does when a Pod it manages disappears.
- Explain how this experiment builds directly on the Docker image from Experiment 07 and the Kubernetes manifests from Experiment 08, without changing either.
- Use `kubectl` to observe whether the cluster's actual state matches a Deployment's desired state.

## Requirements

- The Docker image `techfest-app:v2` (Experiment 07).
- The Kubernetes manifests from Experiment 08 — `experiment-08/deployment.yaml` and `experiment-08/service.yaml`. Experiment 09 does not define new manifests; it reuses these as-is.
- A local Kubernetes cluster with `kubectl` configured, as described in Experiment 08.

**Prerequisite:** Complete Experiment 08 first. The `techfest-app` Deployment and `techfest-service` Service must already be applied to the cluster (`kubectl apply -f deployment.yaml`, `kubectl apply -f service.yaml`) and the `techfest-app:v2` image must be loaded into the Kind node before running the steps below.

**Note on current status:** the practical steps below have been actually performed and verified against a running cluster. The Deployment and Service from Experiment 08 were already present in the cluster (5 days old at the time of this experiment), so Experiment 09's own work consisted of checking their state, deliberately deleting the running Pod, and observing Kubernetes recreate it automatically.

## Concept

### Why Kubernetes Automation Is Needed

In Experiment 07, the container was started with a single `docker run` command. That command runs the container once — if it crashes or is stopped, nothing restarts it, and nothing is watching it. Running it "automatically," in the Kubernetes sense, means something else is continuously responsible for keeping it running, without a person re-issuing `docker run` by hand.

### Docker Container Execution vs. Kubernetes-Managed Execution

- **Docker container execution** (`docker run ...`) is a one-time, imperative action: start this container, from this image, now. Once it's running, Docker doesn't do anything further to keep it that way.
- **Kubernetes-managed execution** is declarative: a Deployment describes what *should* be running, and Kubernetes continuously works to make the actual cluster match that description — including restarting things if they stop matching it.

### Desired State

"Desired state" is what a Deployment's spec declares should exist — for `techfest-app`, that is exactly one Pod running the `techfest-app:v2` image (`replicas: 1`, as set in Experiment 08's `deployment.yaml`). Kubernetes doesn't just create that Pod once; it keeps comparing the real state of the cluster against this description on an ongoing basis.

### How a Deployment Automates Pod Management

The `techfest-app` Deployment (from Experiment 08) is the object responsible for this automation. It doesn't just cause a Pod to be created — it keeps watching, and if the actual number of matching Pods (identified via the `app: techfest-app` label, as covered in Experiment 08) ever drops below what `replicas` specifies, it creates a new one to make up the difference.

### Replicas

`replicas: 1` sets the desired Pod count to one. This experiment does not change that value or demonstrate running more than one replica — but it is the same field that drives Kubernetes's automation, so understanding it here is what makes the self-healing behavior below meaningful, even at a replica count of one.

### Self-Healing — Recreation of Pods

If a Pod managed by a Deployment is deleted (or crashes), the Deployment notices that the actual Pod count no longer matches the desired count and creates a replacement Pod automatically — without anyone running `docker run` or `kubectl create` again. This replacement is a **new** Pod, not the original one restarted; it will typically get a new Pod name. This specific behavior — a Pod disappearing and Kubernetes replacing it on its own — is what this experiment's practical steps are built around observing.

### How Kubernetes Maintains Desired State

The mechanism above is often described as a *control loop*: Kubernetes repeatedly checks "does the current state match the desired state?" and, whenever it doesn't, takes action to close that gap. This runs continuously, not just once at deployment time — which is why a Pod being deleted after the Deployment is already running still gets corrected automatically.

### How This Builds on Experiments 07 and 08

- **Experiment 07** produced the Docker image, `techfest-app:v2`.
- **Experiment 08** defined how that image should run in Kubernetes — a Deployment (`techfest-app`, `replicas: 1`) and a Service (`techfest-service`, NodePort).
- **Experiment 09** does not build a new image or write new manifests. It uses that same Deployment to demonstrate the automation Kubernetes provides on top of it — specifically, that the Deployment keeps its one replica running even if the current Pod goes away.

### Architecture / Flow

```text
techfest-app:v2 (Experiment 07 image)
        ↓
Deployment: techfest-app (Experiment 08 manifest, reused)
        ↓
Kubernetes maintains desired state (replicas: 1)
        ↓
Pod is deleted/crashes  →  actual state no longer matches desired state
        ↓
Deployment automatically creates a replacement Pod
        ↓
Desired state (1 running Pod) restored
```

## Procedure

**Central demonstration of this experiment:**

```text
Pod before deletion:
techfest-app-6c98cc6db8-bzlvx

        ↓ intentional deletion (kubectl delete pod)

Pod after deletion:
techfest-app-6c98cc6db8-fcms2
1/1 Running
```

The steps below record how this was actually carried out and verified.

### Step 1 — Baseline Check

**Status:** Actually performed.

**What:** Check the cluster node, the `techfest-app` Deployment, its Pod, and the `techfest-service` Service, before making any change.

**Why:** This establishes the actual starting state — a Deployment already at its desired replica count, with one Pod running — so that the effect of deleting the Pod in Step 2 can be judged against a known baseline.

**Command/Action:**

```bash
kubectl get nodes
kubectl get deployments
kubectl get pods
kubectl get services
```

**Observe:**

```text
NODE
experiment-08-control-plane   Ready   control-plane   v1.30.0

DEPLOYMENT
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
techfest-app   1/1     1            1           5d

POD
NAME                            READY   STATUS    RESTARTS      AGE
techfest-app-6c98cc6db8-bzlvx   1/1     Running   1 (4d ago)    4d23h

SERVICE
NAME              TYPE       CLUSTER-IP     PORT(S)        AGE
techfest-service  NodePort   10.96.184.50   80:30576/TCP   5d
```

**Verification:** Confirmed — the node is `Ready`, the Deployment is at `1/1`, and the existing Pod (`techfest-app-6c98cc6db8-bzlvx`) is `Running`, matching the `techfest-app` Deployment and `techfest-service` Service already established in Experiment 08.

### Step 2 — Delete the Running Pod to Trigger Self-Healing

**Status:** Actually performed.

**What:** Manually delete the Pod identified in Step 1 (`techfest-app-6c98cc6db8-bzlvx`), which is managed by the `techfest-app` Deployment.

**Why:** This is the actual test of Kubernetes automation — deleting the Pod removes it from the cluster's actual state, which then no longer matches the Deployment's desired state of 1 running replica.

**Command/Action:**

```bash
kubectl delete pod techfest-app-6c98cc6db8-bzlvx
```

**Note:** `techfest-app-6c98cc6db8-bzlvx` is the Pod name from this experiment's recorded run. When you run Step 1, your Pod will have a **different name** generated by Kubernetes — substitute your actual Pod name from the Step 1 output. Do not copy this name literally.

**Observe:**

```text
pod "techfest-app-6c98cc6db8-bzlvx" deleted
```

**Verification:** Confirmed — the delete command completed and reported the Pod as deleted.

### Step 3 — Confirm Kubernetes Automatically Recreated the Pod

**Status:** Actually performed.

**What:** Check the Pod list immediately after the deletion in Step 2.

**Why:** This is where the self-healing behavior described in the Concept section is actually observed — a new Pod appearing on its own, without any `kubectl create`/`docker run` command, is the evidence of Kubernetes automation.

**Command/Action:**

```bash
kubectl get pods
```

**Observe:**

```text
NAME                            READY   STATUS    RESTARTS   AGE
techfest-app-6c98cc6db8-fcms2   1/1     Running   0          5s
```

**Verification:** Confirmed — a **new** Pod, `techfest-app-6c98cc6db8-fcms2` (a different name from the deleted `techfest-app-6c98cc6db8-bzlvx`), was already `Running` and `1/1` only 5 seconds after the deletion, with no manual command creating it.

### Step 4 — Confirm the Deployment's Desired State Is Restored

**Status:** Actually performed.

**What:** Check the Deployment's replica status and Pod list again, slightly later.

**Why:** This closes the loop — confirming that after the disruption in Step 2 and the automatic recovery in Step 3, the Deployment is still matching its declared `replicas: 1`, on a stable, running Pod.

**Command/Action:**

```bash
kubectl get deployments
kubectl get pods
```

**Observe:**

```text
DEPLOYMENT
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
techfest-app   1/1     1            1           5d

POD
NAME                            READY   STATUS    RESTARTS   AGE
techfest-app-6c98cc6db8-fcms2   1/1     Running   0          41s
```

**Verification:** Confirmed — the Deployment remained at `1/1`, and the replacement Pod (`techfest-app-6c98cc6db8-fcms2`) was still `Running` and `1/1` at 41 seconds old, with zero restarts, confirming a clean, stable recreation rather than a crash-looping replacement.

### What This Result Demonstrates

- The `techfest-app` Deployment's desired state is 1 replica — confirmed both before and after the disruption.
- The original Pod, `techfest-app-6c98cc6db8-bzlvx`, was intentionally deleted.
- Kubernetes automatically created a replacement Pod, `techfest-app-6c98cc6db8-fcms2`, without any manual create/run command.
- The replacement Pod reached `1/1 Running` within seconds.
- The Deployment remained at `1/1` throughout.
- Together, this is actual, observed evidence of Kubernetes automatically maintaining a Deployment's desired state — the core behavior this experiment set out to demonstrate. No scaling, rolling update, or application change was performed or is claimed here.

## Observation / Verification

| Check | Evidence type | Confirms | Status |
|---|---|---|---|
| `techfest-app` Deployment sets `replicas: 1` | Configuration (`experiment-08/deployment.yaml`) | Desired state is declared as 1 running Pod | Established |
| Node `experiment-08-control-plane` is `Ready`; Deployment `1/1`; Pod `techfest-app-6c98cc6db8-bzlvx` `Running`; Service `techfest-service` `NodePort` on `80:30576/TCP` | Runtime (Step 1 — `kubectl get nodes/deployments/pods/services`) | Baseline desired-state match, before disruption | Actually performed |
| `pod "techfest-app-6c98cc6db8-bzlvx" deleted` | Runtime (Step 2 — `kubectl delete pod`) | The original Pod was intentionally removed, diverging actual state from desired state | Actually performed |
| New Pod `techfest-app-6c98cc6db8-fcms2`, `1/1 Running`, 5s old | Runtime (Step 3 — `kubectl get pods`) | Kubernetes automatically created a replacement Pod | Actually performed |
| Deployment `1/1`; Pod `techfest-app-6c98cc6db8-fcms2` `1/1 Running`, 0 restarts, 41s old | Runtime (Step 4 — `kubectl get deployments/pods`) | Desired state restored and stable after automatic recreation | Actually performed |

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `techfest-app:v2` not available to the cluster node | New Pod fails to start after deletion (`ImagePullBackOff` / `ErrImageNeverPull`) | Confirm the image is available to the node, as covered in Experiment 08, before testing self-healing |
| Assuming the same Pod "restarts" | Looking for the original Pod name after deletion | A replacement Pod is a **new** Pod with a new name — self-healing recreates, it does not restore the same instance |
| Running `kubectl delete pod` with a stale Pod name | "pod not found" error | Re-check `kubectl get pods` immediately before deleting, since the name is Kubernetes-generated |
| Confusing this with scaling or rolling updates | Expecting multiple replicas or a version change | This experiment only demonstrates self-healing at `replicas: 1`; scaling and rolling updates were not performed and are not claimed here |
| Misreading the restart count on the original Pod as caused by this experiment | `RESTARTS: 1 (4d ago)` on `techfest-app-6c98cc6db8-bzlvx` predates the deletion in Step 2 | That restart happened 4 days before this experiment's own work; only the deletion in Step 2 and its outcome are attributed to Experiment 09 |

## Quick Reference

| Command | Purpose |
|---|---|
| `kubectl get nodes` | Check the cluster node's status |
| `kubectl get deployments` | Check the Deployment's desired vs. actual replica count |
| `kubectl get pods` | List current Pods and their names/status |
| `kubectl get services` | Check the Service's type, cluster IP, and exposed port |
| `kubectl delete pod <pod-name>` | Deliberately remove the running Pod, to test self-healing |

## Result

Kubernetes automation of the Exercise 7 containerized application was demonstrated and verified. Using the `techfest-app` Deployment and `techfest-service` Service already established in Experiment 08 (running the Experiment 07 image, `techfest-app:v2`), a baseline check (`kubectl get nodes/deployments/pods/services`) confirmed the Deployment at `1/1` with its Pod, `techfest-app-6c98cc6db8-bzlvx`, running.

That Pod was then intentionally deleted with `kubectl delete pod techfest-app-6c98cc6db8-bzlvx`, which reported `pod "techfest-app-6c98cc6db8-bzlvx" deleted`. Immediately afterward, `kubectl get pods` showed Kubernetes had automatically created a replacement Pod, `techfest-app-6c98cc6db8-fcms2`, already `1/1 Running` at 5 seconds old. A final check (`kubectl get deployments`, `kubectl get pods`) confirmed the Deployment remained at `1/1` and the replacement Pod was still `1/1 Running` with zero restarts at 41 seconds old.

This is actual, observed evidence that Kubernetes automatically maintains a Deployment's desired state — recreating a deleted Pod without manual intervention — building directly on the Docker image from Experiment 07 and the Deployment/Service manifests from Experiment 08, without modifying either. No scaling, rolling update, or application change was performed or is claimed as part of this result.
