# Tutorial 13 - Deploying MongoDB on Kubernetes

## What is MongoDB?

MongoDB is a NoSQL document database. Unlike traditional relational databases (like PostgreSQL or MySQL) that store data in tables with rows and columns, MongoDB stores data as flexible JSON-like documents called BSON (Binary JSON).

**Key characteristics:**

- **Document-oriented**: Data is stored in flexible, JSON-like documents where fields can vary from document to document
- **Schema-less**: No need to define a rigid schema upfront; documents in the same collection can have different structures
- **Scalable**: Built-in support for horizontal scaling through sharding
- **High performance**: Supports indexing, aggregation pipelines, and an in-memory cache for the storage engine
- **Rich query language**: Powerful queries, aggregations, and full-text search

**When to use MongoDB:**

- Applications with rapidly changing requirements
- Content management systems
- Real-time analytics
- IoT applications
- Mobile app backends
- Storing semi-structured or unstructured data

**Document example** (Extended JSON represents the BSON ObjectId with `$oid`):
```json
{
  "_id": {"$oid": "507f1f77bcf86cd799439011"},
  "name": "John Doe",
  "email": "john@example.com",
  "age": 25,
  "courses": ["M7011E", "D7002E"],
  "address": {
    "city": "Luleå",
    "country": "Sweden"
  }
}
```

## Installation Guide

Run commands from `13-mongodb/`. This chart deploys one standalone MongoDB instance, not a replica set or sharded cluster.
The provided Helm chart deploys a MongoDB database using a StatefulSet with persistent storage. The chart includes:

- MongoDB deployment via StatefulSet
- Persistent Volume Claims for data storage
- ConfigMap for non-sensitive settings and a Secret for root credentials
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
| `DBUser` | MongoDB root username | `admin` |
| `DBPassword` | MongoDB root password | `TODO` |
| `DBName` | Database used by initialization scripts (created on first write) | `appdb` |
| `DBImage` | Docker image for MongoDB | `mongo:7` |
| `DBResourceLimit` | Enable resource limits | `false` |
| `DBCPU` | CPU limit | `500m` |
| `DBMemory` | Memory limit | `512Mi` |
| `DBStorage` | Storage size for persistent volume | `10Gi` |

## Read the Database Commands Before Running Them

MongoDB's server stores documents; `mongosh` is a client that sends operations to that server. A Kubernetes port forward only supplies a route between your local client and the cluster. It does not authenticate you or select which documents to query.

| Command below | Meaning in this setup |
| --- | --- |
| `./install.sh` / `helm install mongodb -f values.yaml -n db .` | Alternative installation paths for this one standalone database instance. The script runs Helm; neither path creates a replica set. |
| `kubectl get pods -n db` / `kubectl get pvc -n db` | Inspect the running database process / its storage claim. A ready Pod and a bound claim answer different questions. |
| `kubectl port-forward -n db svc/mongodb-service 27017:27017` | Open a local-to-cluster tunnel. With `27018:27017`, the local client must use 27018. |
| `mongosh .../appdb?authSource=admin` | Connect to application database `appdb` while authenticating the configured root account against `admin`. The authentication database and data database need not be the same. |
| `kubectl exec ... -- mongosh ...` | Run the client inside the Pod instead of on your laptop. The meaning of `localhost` changes with that execution location. |
| `mongodump ... --archive > backup.archive` through `kubectl exec` | Create an archive inside the remote command's output stream and save it to a local file. The shell performing `>` determines the file's location. |
| `helm upgrade ...` | Update Kubernetes configuration; editing initialization credentials is not itself a password rotation on an initialized database. |

In mongosh, `use appdb` selects the database for subsequent operations; the first write creates it if necessary. `find()` reads matching documents, while `insertOne`, `updateOne`, and `deleteOne` change data. Read the predicate and expected result before executing a write. Deleting a Pod while retaining its volume and deleting the PVC have different persistence consequences.

**Predict and verify:** Insert a document, record its identifier, and read it back. Open a new client session and query the same database. Explain why closing mongosh should leave the document intact, whereas a write to an in-memory Python list would disappear when that API process restarts. See [the command guide](../COMMANDS.md) for ports and redirection.

## Installation

### Step 1: Configure Values

Before installing, edit `values.yaml` to customize your deployment. **Important**: Change the `DBPassword` from `TODO` to a secure password.

```yaml
DBPassword: "your-secure-password-here"
```

### Step 2: Create Namespace

Create the namespace where MongoDB will be deployed:

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
helm install mongodb -f values.yaml -n db .
```

### Step 4: Verify Installation

Check that the MongoDB pod is running:

```bash
kubectl get pods -n db
```

Expected output:
```
NAME         READY   STATUS    RESTARTS   AGE
mongodb-0    1/1     Running   0          1m
```

Check the service:

```bash
kubectl get svc -n db
```

Expected output:
```
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)     AGE
mongodb-service   ClusterIP   10.43.xxx.xxx   <none>        27017/TCP   1m
```

## Installing MongoDB Client Tools

To connect to the database from your local machine, you'll need MongoDB client tools installed.

### Linux

Install mongosh using the [official MongoDB Shell installation guide](https://www.mongodb.com/docs/mongodb-shell/install/) for your distribution and architecture. Configure the matching MongoDB package repository before using apt or dnf; an Ubuntu Jammy repository is not suitable for every Debian/Ubuntu release. Alternatively use the database Pod directly below.

### macOS (Homebrew)

```bash
brew install mongosh
```

### Windows (Chocolatey)

```powershell
choco install mongodb-shell
```

### Docker Alternative (Linux)

With port forwarding active, Docker Engine on Linux can use host networking. Docker Desktop requires host networking to be enabled explicitly. Otherwise use a local client or the direct Pod command below:

```bash
docker run -it --rm --network host mongo:7 mongosh "mongodb://localhost:27017/appdb" -u admin --authenticationDatabase admin
```

### Verify Installation

```bash
mongosh --version
```

## Accessing the Database

### Option 1: Port Forwarding (Development/Testing)

To access the database from your local machine, use `kubectl port-forward`:

```bash
kubectl port-forward -n db svc/mongodb-service 27017:27017
```

This command forwards local port 27017 to the MongoDB service running in Kubernetes. Keep this terminal window open while you need database access.

Now you can connect using mongosh. Replace the example credentials; URL-encode reserved characters when putting a password in a URI. `MONGO_INITDB_DATABASE` does not create a separate application user or populate the database; MongoDB creates the database on its first write:

```bash
mongosh "mongodb://admin:your-password@localhost:27017/appdb?authSource=admin"
```

### Option 2: Port Forwarding with Custom Local Port

If port 27017 is already in use on your local machine, forward to a different port:

```bash
kubectl port-forward -n db svc/mongodb-service 27018:27017
```

Then connect to `localhost:27018` instead.

### Option 3: From Within the Cluster

Applications running in the same Kubernetes cluster can access MongoDB directly using the service DNS name:

```
mongodb-service.db.svc.cluster.local:27017
```

Or simply `mongodb-service` if they're in the same namespace.

### Option 4: Direct Pod Access

To access the database directly from the pod:

```bash
kubectl exec -it -n db mongodb-0 -- mongosh -u admin --authenticationDatabase admin
```

## Example Usage for Students

### Basic CRUD Operations

Once connected to MongoDB, try these basic operations:

```javascript
// Switch to your database
use appdb

// Insert a document
db.students.insertOne({
  name: "John Doe",
  email: "john@example.com",
  age: 22,
  courses: ["M7011E", "D7002E"]
})

// Insert multiple documents
db.students.insertMany([
  { name: "Jane Smith", email: "jane@example.com", age: 23, courses: ["M7011E"] },
  { name: "Bob Wilson", email: "bob@example.com", age: 21, courses: ["M7011E", "D7002E", "D7001E"] }
])

// Find all documents
db.students.find()

// Find with filter
db.students.find({ age: { $gte: 22 } })

// Find one document
db.students.findOne({ name: "John Doe" })

// Update a document
db.students.updateOne(
  { name: "John Doe" },
  { $set: { age: 23 }, $push: { courses: "D7001E" } }
)

// Delete a document
db.students.deleteOne({ name: "Jane Smith" })

// Count documents
db.students.countDocuments()

// Create an index
db.students.createIndex({ email: 1 }, { unique: true })
```

### Python Example (pymongo)

```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://admin:your-password@localhost:27017/appdb?authSource=admin")
db = client.appdb

# Insert a document
result = db.students.insert_one({
    "name": "Alice Brown",
    "email": "alice@example.com",
    "age": 24,
    "courses": ["M7011E"]
})
print(f"Inserted ID: {result.inserted_id}")

# Find documents
for student in db.students.find({"age": {"$gte": 22}}):
    print(student)

# Update a document
db.students.update_one(
    {"name": "Alice Brown"},
    {"$set": {"age": 25}}
)

# Close connection
client.close()
```

Install pymongo:
```bash
pip install pymongo
```

### Node.js Example

```javascript
const { MongoClient } = require('mongodb');

async function main() {
  const uri = "mongodb://admin:your-password@localhost:27017/appdb?authSource=admin";
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db("appdb");

    // Insert a document
    const result = await db.collection("students").insertOne({
      name: "Charlie Davis",
      email: "charlie@example.com",
      age: 22,
      courses: ["M7011E"]
    });
    console.log(`Inserted ID: ${result.insertedId}`);

    // Find documents
    const students = await db.collection("students")
      .find({ age: { $gte: 22 } })
      .toArray();
    console.log(students);

  } finally {
    await client.close();
  }
}

main().catch(console.error);
```

Install mongodb driver:
```bash
npm install mongodb
```

### Express.js API Example

Install `express@5` and `mongodb` with npm. Express 5 forwards rejected async route promises to its error handler. Add application-specific validation before accepting arbitrary request bodies.

```javascript
const express = require('express');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
app.use(express.json());

const uri = "mongodb://admin:your-password@localhost:27017/appdb?authSource=admin";
const client = new MongoClient(uri);

let db;

async function connectDB() {
  await client.connect();
  db = client.db("appdb");
  console.log("Connected to MongoDB");
}

// Validate ObjectId before any route that uses :id.
app.param('id', (req, res, next, id) => {
  if (!ObjectId.isValid(id)) return res.status(400).json({ error: 'Invalid student ID' });
  next();
});

// Get all students
app.get('/students', async (req, res) => {
  const students = await db.collection("students").find().toArray();
  res.json(students);
});

// Get student by ID
app.get('/students/:id', async (req, res) => {
  const student = await db.collection("students").findOne({
    _id: new ObjectId(req.params.id)
  });
  if (!student) return res.status(404).json({ error: "Not found" });
  res.json(student);
});

// Create student
app.post('/students', async (req, res) => {
  const result = await db.collection("students").insertOne(req.body);
  res.status(201).json({ id: result.insertedId });
});

// Update student
app.patch('/students/:id', async (req, res) => {
  await db.collection("students").updateOne(
    { _id: new ObjectId(req.params.id) },
    { $set: req.body }
  );
  res.json({ message: "Updated" });
});

// Delete student
app.delete('/students/:id', async (req, res) => {
  await db.collection("students").deleteOne({
    _id: new ObjectId(req.params.id)
  });
  res.json({ message: "Deleted" });
});

connectDB().then(() => {
  app.listen(3000, () => console.log("Server running on port 3000"));
}).catch(console.error);
```

## Updating the Deployment

To update the deployment after changing `values.yaml`:

```bash
./update.sh
```

Or manually:

```bash
helm upgrade mongodb -f values.yaml -n db .
```

## Uninstallation

To uninstall the chart:

```bash
./uninstall.sh
```

Or manually:

```bash
helm uninstall mongodb -n db
```

**Note**: The PVC is annotated `helm.sh/resource-policy: keep`, so Helm retains it on uninstall. To completely remove all data:

```bash
kubectl delete pvc -n db mongodb-pvc
```

## Troubleshooting

### Pod Not Starting

Check pod logs:
```bash
kubectl logs -n db mongodb-0
```

Describe the pod for events:
```bash
kubectl describe pod -n db mongodb-0
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
kubectl get svc -n db mongodb-service
```

Test connectivity from within the cluster:
```bash
kubectl run -it --rm debug --image=mongo:7 --restart=Never -n db -- mongosh "mongodb://mongodb-service:27017/appdb" -u admin --authenticationDatabase admin
```

### Authentication Issues

Confirm that `mongodb-credentials` was created from your configured values. Root credentials are initialized only when the data directory is empty; changing the Helm values or Secret does not change an existing MongoDB user's password. Update that user through an authenticated mongosh session and then update the Secret to match.

## Data Persistence

Data is persisted using a PersistentVolumeClaim. The data will survive pod restarts and deletions. To backup your data:

```bash
# Dump the database
kubectl exec -n db mongodb-0 -- mongodump --uri="mongodb://admin:your-password@localhost:27017" --archive > backup.archive

# Restore from backup
cat backup.archive | kubectl exec -i -n db mongodb-0 -- mongorestore --uri="mongodb://admin:your-password@localhost:27017" --archive
```

## MongoDB Compass (GUI)

You can also use MongoDB Compass for a graphical interface:

1. Download from: https://www.mongodb.com/products/compass
2. With port-forward active, connect using:
   ```
   mongodb://admin:your-password@localhost:27017/?authSource=admin
   ```
