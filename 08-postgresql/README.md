# Tutorial 7 - Deploying a PostgreSQL database on Kubernetes

This guide contains instructions how to deploying PostgreSQL on Kubernetes.
The provided Helm chart deploys a PostgreSQL database using a StatefulSet with persistent storage. The chart includes:

- PostgreSQL deployment via StatefulSet
- Persistent Volume Claims for data storage
- ConfigMap for database configuration
- Service for database access

## Prerequisites

- Kubernetes cluster (v1.19+)
- Helm 3.x
- kubectl configured to communicate with your cluster
- A StorageClass available in your cluster (default: `local-path`)

## Configuration

The following table lists the configurable parameters in `values.yaml`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `StorageClassName` | Storage class for persistent volume | `local-path` |
| `Timezone` | Database timezone | `Europe/Stockholm` |
| `DBUser` | PostgreSQL username | `postgres` |
| `DBPassword` | PostgreSQL password | `TODO` |
| `DBImage` | Docker image for PostgreSQL | `postgres:16` |
| `DBResourceLimit` | Enable resource limits | `false` |
| `DBCPU` | CPU limit | `1000m` |
| `DBMemory` | Memory limit | `1000Mi` |
| `DBStorage` | Storage size for persistent volume | `10Gi` |

## Installation

### Step 1: Configure Values

Before installing, edit `values.yaml` to customize your deployment. **Important**: Change the `DBPassword` from `TODO` to a secure password.

```yaml
DBPassword: "your-secure-password-here"
```

### Step 2: Create Namespace

Create the namespace where PostgreSQL will be deployed:

```bash
./create_namespace.sh
```

Or manually:

```bash
kubectl create namespace db
```

### Step 3: Install the Chart

Install the chart using the provided script:

```bash
./install.sh
```

Or manually with Helm:

```bash
helm install postgresql -f values.yaml -n db .
```

### Step 4: Verify Installation

Check that the PostgreSQL pod is running:

```bash
kubectl get pods -n db
```

Expected output:
```
NAME           READY   STATUS    RESTARTS   AGE
postgres-0     1/1     Running   0          1m
```

Check the service:

```bash
kubectl get svc -n db
```

Expected output:
```
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
postgres-service   ClusterIP   10.43.xxx.xxx   <none>        5432/TCP   1m
```

## Installing PostgreSQL Client (psql)

To connect to the database from your local machine, you'll need the PostgreSQL client tools installed.

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install postgresql-client
```

### Linux (Fedora/RHEL/CentOS)

```bash
sudo dnf install postgresql
```

### Linux (Arch)

```bash
sudo pacman -S postgresql-libs
```

### macOS (Homebrew)

```bash
brew install postgresql
```

### Windows (Chocolatey)

```powershell
choco install postgresql
```

### Docker Alternative (Any Platform)

If you prefer not to install locally, use Docker:

```bash
docker run -it --rm --network host postgres:16 psql -h localhost -U postgres
```

### Verify Installation

```bash
psql --version
```

Expected output: `psql (PostgreSQL) 16.x`

## Accessing the Database

### Option 1: Port Forwarding (Development/Testing)

To access the database from your local machine, use `kubectl port-forward`:

```bash
kubectl port-forward -n db svc/postgres-service 5432:5432
```

This command forwards local port 5432 to the PostgreSQL service running in Kubernetes. Keep this terminal window open while you need database access.

Now you can connect using any PostgreSQL client:

```bash
psql -h localhost -p 5432 -U postgres
```

Or using a connection string:
```
postgresql://postgres:your-password@localhost:5432/postgres
```

### Option 2: Port Forwarding with Custom Local Port

If port 5432 is already in use on your local machine, forward to a different port:

```bash
kubectl port-forward -n db svc/postgres-service 5433:5432
```

Then connect to `localhost:5433` instead.

### Option 3: From Within the Cluster

Applications running in the same Kubernetes cluster can access PostgreSQL directly using the service DNS name:

```
postgres-service.db.svc.cluster.local:5432
```

Or simply `postgres-service` if they're in the same namespace.

### Option 4: Direct Pod Access

To access the database directly from the pod:

```bash
kubectl exec -it -n db postgres-0 -- psql -U postgres
```

## Connecting with Different Clients

### psql (Command Line)

With port-forward active:
```bash
PGPASSWORD=your-password psql -h localhost -p 5432 -U postgres -d postgres
```

### Python (psycopg2)

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="your-password",
    database="postgres"
)
```

### Node.js (pg)

```javascript
const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5432,
  user: 'postgres',
  password: 'your-password',
  database: 'postgres'
});

await client.connect();
```

### DBeaver / pgAdmin

- Host: `localhost`
- Port: `5432` (or your custom port)
- Database: `postgres`
- Username: `postgres`
- Password: (your configured password)

## Updating the Deployment

To update the deployment after changing `values.yaml`:

```bash
./update.sh
```

Or manually:

```bash
helm upgrade postgresql -f values.yaml -n db .
```

## Uninstallation

To uninstall the chart:

```bash
./uninstall.sh
```

Or manually:

```bash
helm uninstall postgresql -n db
```

**Note**: This will not delete the PersistentVolumeClaim by default. To completely remove all data:

```bash
kubectl delete pvc -n db --all
```

## Troubleshooting

### Pod Not Starting

Check pod logs:
```bash
kubectl logs -n db postgres-0
```

Describe the pod for events:
```bash
kubectl describe pod -n db postgres-0
```

### Storage Issues

Check PVC status:
```bash
kubectl get pvc -n db
```

Ensure your StorageClass exists:
```bash
kubectl get storageclass
```

### Connection Issues

Verify the service is running:
```bash
kubectl get svc -n db postgres-service
```

Test connectivity from within the cluster:
```bash
kubectl run -it --rm debug --image=postgres:16 --restart=Never -n db -- psql -h postgres-service -U postgres
```

### Password Not Working

Check if the password in the ConfigMap matches your values.yaml:
```bash
kubectl get configmap -n db postgres-config -o yaml
```

## Data Persistence

Data is persisted using a PersistentVolumeClaim. The data will survive pod restarts and deletions. To backup your data:

```bash
# Dump the database
kubectl exec -n db postgres-0 -- pg_dump -U postgres postgres > backup.sql

# Restore from backup
cat backup.sql | kubectl exec -i -n db postgres-0 -- psql -U postgres
```
