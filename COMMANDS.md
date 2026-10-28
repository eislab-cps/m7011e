# Understanding the commands

Commands are instructions to particular programs. Understanding which program receives an argument helps you adapt an example to your own machine and explain a failure. Use this guide alongside the command explanations in each tutorial.

## Locate yourself before changing anything

```bash
pwd
ls
```

`pwd` prints your current working directory. `ls` lists the files there. A relative path such as `values.yaml`, `backend/`, or `.` is resolved from that directory. `.` means the current directory; `..` means its parent. `cd backend` changes the directory of your current shell; it does not start the backend.

`./install.sh` runs a script from the current directory. The leading `./` distinguishes it from a program found through `PATH`. Read the script before running it: an installation script can create cluster resources even though the script itself is stored on your laptop.

Do not type the `$` prompt shown in some documentation. Replace placeholders such as `YOUR_USERNAME` and `<pod-name>` with actual values; angle brackets are also shell redirection operators, so a placeholder is not an executable argument.

## Read a command from left to right

Consider this command from Tutorial 7:

```bash
helm install helloworld -f values.yaml -n helloworld .
```

| Part | Meaning |
| --- | --- |
| `helm` | Program to run. |
| `install` | Subcommand: create a Helm release. |
| First `helloworld` | Name of this release. It is an identifier, not a file path. |
| `-f values.yaml` | Read configuration from this local file. |
| `-n helloworld` | Create the release's namespaced resources in this Kubernetes namespace. |
| `.` | Read the chart from the current directory. |

This contacts the cluster selected by your kubeconfig. It does not deploy to a cluster because of the directory's name. `helm template helloworld . -f values.yaml` instead prints rendered YAML locally; rendering does not create resources or prove that the running application will work.

Use `program --help`, or a subcommand such as `kubectl port-forward --help`, to inspect its arguments. The same option letter can mean different things in different programs: `curl -i` includes response headers, while `kubectl exec -i` keeps standard input open.

## Know which computer runs the work

| Command | Where the work happens |
| --- | --- |
| `python3 app.py` | The program runs on your machine, using its Python environment. |
| `docker build ...` | The Docker daemon builds an image from a supplied build context. |
| `kubectl get pods` | Your CLI asks the selected cluster's API server for Pod information. |
| `kubectl exec ... -- psql ...` | Your CLI starts `psql` inside the selected container. |
| `curl http://localhost:8000/api/todos` | Your machine connects to port 8000 on itself. |

`localhost` always refers to the network environment of the process using it. Inside a container or Pod it does not mean your laptop or a different Pod. Use the hostname or Service name appropriate to the caller.

## Understand ports and foreground processes

`docker run -p 8080:80 IMAGE` publishes port 8080 on the Docker host and forwards it to port 80 in the container. The order is **host:container**.

`kubectl port-forward -n db svc/postgres-service 5433:5432` listens locally on port 5433 and tunnels connections through Kubernetes to the Service's port 5432. The order is **local:remote**. Point your local database client at `localhost:5433`; the database still listens on 5432 remotely. By default the listener is local to your machine.

Servers, consumers, port forwards, `kubectl ... -w`, and `... logs -f` keep running in the foreground. Use another terminal for the next independent command. `Ctrl+C` stops the foreground command; stopping a watch or port forward does not delete the deployment it was observing.

## Separate installing, building, and running

| Action | What it changes |
| --- | --- |
| `python3 -m venv .venv` | Creates a local Python environment directory. |
| `source .venv/bin/activate` | Adjusts the current shell so `python` and `pip` use that environment. |
| `python -m pip install -r requirements.txt` | Installs the listed Python dependencies into that interpreter's environment. |
| `npm install` | Resolves and installs JavaScript dependencies; can create or update a lockfile. |
| `npm ci` | Reinstalls dependencies from an existing, matching lockfile. |
| `npm run dev`, `npm start` | Runs a script from `package.json`; inspect that file to see which server starts. |
| `npm run build` | Produces build artifacts; it does not itself deploy them. |

Installing dependencies does not start a server. Building an image does not start a container. Publishing an image does not update a running Deployment unless its deployment mechanism performs that update.

## Understand variables, quoting, pipes, and redirection

`export KEYCLOAK_URL="https://your-domain.example"` sets a variable inherited by programs subsequently started from that shell. It does not edit a Python file or an existing Kubernetes Deployment. A different terminal needs its own environment or configuration.

`$NAME` expands a shell variable. `$(command)` inserts a command's output. Quote expansions such as `"$POD_NAME"` to keep them as one argument. A backslash at the end of a line continues the same shell command onto the next line; it must be the final character.

In `producer | consumer`, the shell sends the first program's standard output into the second program's standard input. For example, `kubectl get secret ... -o jsonpath=... | base64 -d` extracts an encoded field and decodes it. Base64 is an encoding, not encryption; decoding a Secret can reveal a credential.

`command > backup.sql` writes output to a **local** file and replaces that file if it already exists. `command < backup.sql` reads input from a local file. The shell performs these redirections even when `command` starts a program in a remote container. A here-document such as `<<EOF` supplies the following lines as input until the matching delimiter.

`first && second` runs the second command only if the first succeeds. Exit status zero conventionally means success; a nonzero status indicates failure. A successful CLI exit is only one check: an accepted Kubernetes manifest can still produce an unhealthy Pod.

## Read before you change or delete

`kubectl get`, `kubectl describe`, `kubectl logs`, `docker ps`, and `helm list` inspect state. `kubectl apply`, `helm install`, `helm upgrade`, and `kubectl scale` request changes. The controllers then work towards the requested state, so acceptance and readiness are different observations.

`kubectl delete namespace NAME` deletes the namespaced resources in that namespace, including resources from other releases. Deleting a PersistentVolumeClaim can lead to permanent data removal depending on storage configuration. `docker compose down -v` also requests volume removal. Read the cleanup section and identify the data you intend to remove before using these commands.

To diagnose a failure, first identify its layer: command syntax and paths, local process, network connection, TLS, HTTP response, authentication, or application behavior. A connection refusal is different from an HTTP `404`, and a certificate rejection happens before a normal protected HTTP exchange can proceed.
