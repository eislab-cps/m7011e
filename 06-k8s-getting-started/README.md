# Tutorial 6 - Getting started using Kubernetes

This guide connects your computer to the course Kubernetes cluster using `kubectl` and the kubeconfig supplied by the teaching team. You will select a context, check your namespace access, and inspect resources from the terminal.

## Why Use an API Client Instead of Logging into Every Server?

With manual server administration, a deployment can depend on a particular host, shell session, and sequence of commands. Kubernetes instead exposes an API for declaring and observing resources. Controllers and node agents carry out the work. `kubectl` is a client of that API; it is not the cluster itself and does not normally deploy by opening SSH sessions to every node.

This explains why client installation, cluster selection, authentication, and namespace permissions are different steps. Helm is another client-side tool: it packages and renders related resource definitions. Having kubectl or Helm installed does not grant permission to change a cluster, and changing your local directory does not select a new cluster.

## What the Setup Commands Actually Configure

`kubectl` and Helm are clients on your computer. Kubernetes runs elsewhere. A **kubeconfig** tells the clients which API server to contact and which credentials and context to use. Installing the clients and configuring access are separate steps.

| Command below | Meaning and scope |
| --- | --- |
| `kubectl version --client` | Prints the local client version without checking cluster access. |
| `helm version`, `docker --version` | Check that those local programs are installed. They do not prove that a cluster or application is reachable. |
| `mkdir -p "$HOME/.kube"` | Creates the local configuration directory if needed. `-p` also permits an already-existing directory. |
| `chmod 700 "$HOME/.kube"` | Restricts directory access to its owner. |
| `cp ... ~/.kube/m7011e.yaml` | Copies the course configuration to your own machine. Replace the source filename; this does not create cluster resources. |
| `chmod 600 ...` | Allows only the owner to read and write the configuration file. These permissions do not encrypt the credentials in it. |
| `export KUBECONFIG=...` | Selects that file for programs started from the current shell. Another terminal needs its own setting. |
| `kubectl config current-context` | Reads the selected context from local configuration. A context groups a cluster, identity, and optionally a namespace. |
| `kubectl auth can-i list pods -n YOUR_NAMESPACE` | Asks whether your identity may list Pods in the named namespace. Replace the placeholder with your assigned namespace. |
| `kubectl get pods -n YOUR_NAMESPACE` | Reads Pods from the selected cluster and namespace. An empty list can be a successful result. |

![kubectl reads a local file, then asks a remote API. The left column is on your laptop; the right column is what the cluster checks before acting.](./images/kubeconfig-to-api-server.svg)

**Check your understanding:** Before any later `apply`, `install`, or `delete`, identify the selected cluster and namespace. Explain why changing your terminal's directory does not change your Kubernetes context. See [the command guide](../COMMANDS.md) for shell and namespace syntax.

## 1. Install kubectl
Install the `kubectl` command-line tool to interact with and manage Kubernetes clusters.

**Installation:** Follow the official guide at [https://kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/)

## 2. Install Helm
Install `helm`, the package manager for Kubernetes that simplifies application deployment and management.

**Installation:** Follow the official guide at [https://helm.sh/docs/intro/install](https://helm.sh/docs/intro/install/)

## 3. Install Docker or Podman
Use a container tool to build images and run the local examples. The course commands use Docker and Docker Compose. Podman is an alternative, but check command and Compose compatibility if you choose it. These tools are separate from kubectl: connecting to the course API does not run a local container engine.

- **Docker Desktop:** [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- **Podman:** [https://podman.io/getting-started/installation](https://podman.io/getting-started/installation)

## 4. Verify the Local Tools

Run these on your own computer:

```bash
kubectl version --client
helm version
docker --version
```

These print installed client versions. They do not contact the course cluster or prove that Docker's engine is running. If you chose Podman, use `podman --version` for the last check. Use the kubectl version recommended by the teaching team; kubectl should be within one minor version of the API server according to the [version skew policy](https://kubernetes.io/releases/version-skew-policy/#kubectl).

## 5. Obtain the Course Kubeconfig

Follow the teaching team's instructions to obtain your **kubeconfig**, assigned **namespace**, and the **ingress domain** to use in later tutorials. The domain and account examples elsewhere in the repository are placeholders; use the values assigned for this year's course.

A kubeconfig contains cluster connection settings, certificate information, and credentials or a reference to an authentication method. It is not a Kubernetes workload manifest. Keep your copy private and outside the project repository. If the supplied authentication method needs an additional client or login step, follow the instructions that accompany the file.

## 6. Configure kubectl

Keep the course configuration in its own file so it does not replace an existing default `~/.kube/config`. The commands below assume that you saved the supplied file as `m7011e.yaml` in Downloads; adjust the source path to its actual location.

### Linux and macOS

```bash
# Create a private local directory for Kubernetes client configuration.
mkdir -p "$HOME/.kube"
chmod 700 "$HOME/.kube"

# Copy the course kubeconfig; change this source path if necessary.
cp "$HOME/Downloads/m7011e.yaml" "$HOME/.kube/m7011e.yaml"
chmod 600 "$HOME/.kube/m7011e.yaml"

# Select the course file for kubectl and Helm in this terminal.
export KUBECONFIG="$HOME/.kube/m7011e.yaml"
```

`mkdir -p` creates the directory if needed. `cp` copies the file, and `chmod` limits access to your user; it does not encrypt the contents. `export` changes the environment of this shell and programs started from it. None of these commands creates a resource in the cluster.

### Windows (PowerShell)

```powershell
# Create the client configuration directory.
New-Item -Path "$env:USERPROFILE\.kube" -ItemType Directory -Force

# Copy the course kubeconfig; change this source path if necessary.
Copy-Item -Path "$env:USERPROFILE\Downloads\m7011e.yaml" -Destination "$env:USERPROFILE\.kube\m7011e.yaml"

# Select the course file for programs started from this terminal.
$env:KUBECONFIG = "$env:USERPROFILE\.kube\m7011e.yaml"
```

`New-Item` creates the directory, `Copy-Item` copies the file, and `$env:KUBECONFIG` selects it for this PowerShell session. Store it under your own Windows account and restrict access using the file's security settings.

Set `KUBECONFIG` again in each new terminal used for the course, or add the setting to your shell profile. Kubernetes documents [how kubeconfig files and contexts work](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/).

## 7. Check the Selected Context

```bash
kubectl config get-contexts
kubectl config current-context
```

Both commands read local configuration. `get-contexts` lists available contexts and marks the selected one with `*`; `current-context` prints its name. A context groups a cluster, an identity, and optionally a default namespace. Seeing a context name does not yet prove that the API server is reachable.

If the supplied file has several contexts, select the course context. Replace `YOUR_CONTEXT` with its name from the list:

```bash
kubectl config use-context YOUR_CONTEXT
```

This changes which context is selected in the local kubeconfig. It does not log in as a different user unless that context selects different credentials, and it does not create another cluster.

## 8. Verify Access to Your Namespace

Replace `YOUR_NAMESPACE` with the namespace assigned by the teaching team in every command below:

```bash
kubectl auth can-i list pods -n YOUR_NAMESPACE
kubectl get pods -n YOUR_NAMESPACE
kubectl get services -n YOUR_NAMESPACE
```

`auth can-i` checks authorization for the named operation. `get pods` and `get services` send read requests to the API server. The `-n` flag selects the namespace for that request. A successful response can contain resources or say `No resources found`; an empty namespace is not a connection failure. See the [`kubectl auth can-i` reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/).

You can also check the client and server versions after access is configured:

```bash
kubectl version
```

The server version comes from the selected API server. Compare it with your client version using the policy linked above. Listing nodes with `kubectl get nodes` is optional and needs cluster-level permission; a namespace-scoped course account may correctly receive `Forbidden` for that command.

### Interpret a Failed Check

| Result | Meaning and next check |
| --- | --- |
| No current context, or an attempt to contact an unexpected local address | Check `KUBECONFIG` and the context list in this terminal. |
| DNS error, connection refused, or timeout | Check the API address in the supplied configuration, network access, and any course VPN requirement. |
| Certificate validation error | Check the configuration and endpoint with the teaching team. Do not bypass verification as a setup step. |
| Authentication error, often `Unauthorized` | Check the provided credentials or authentication instructions; expired credentials may need renewal. |
| `Forbidden`, or `auth can-i` prints `no` | The operation is not permitted. Check the namespace and assigned access; installing kubectl does not grant permissions. |

Do not paste credentials or a raw kubeconfig into an issue when reporting a problem. Report the command, context name, namespace, and error instead.

## Check Your Understanding

1. Why can `kubectl version --client` succeed while `kubectl get pods` fails?
2. What changes when you open another terminal without setting `KUBECONFIG`?
3. Why can listing Pods in your namespace succeed while listing nodes returns `Forbidden`?
4. Does changing your terminal's working directory change the selected cluster?

## Next Step

Continue with [Tutorial 7: Hello World](../07-k8s-helloworld/README.md). Confirm the selected context and use the namespace and domain assigned for the course before running its deployment commands.
