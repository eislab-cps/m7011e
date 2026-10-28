# Tutorial 19 - Deploying MongoDB on Kubernetes

## What is MongoDB?

MongoDB is a popular open-source NoSQL document database. Unlike traditional relational databases (like PostgreSQL or MySQL) that store data in tables with rows and columns, MongoDB stores data as flexible JSON-like documents called BSON (Binary JSON).

**Key characteristics:**

- **Document-oriented**: Data is stored in flexible, JSON-like documents where fields can vary from document to document
- **Schema-less**: No need to define a rigid schema upfront; documents in the same collection can have different structures
- **Scalable**: Built-in support for horizontal scaling through sharding
- **High performance**: Supports indexing, aggregation pipelines, and in-memory storage
- **Rich query language**: Powerful queries, aggregations, and full-text search

**When to use MongoDB:**

- Applications with rapidly changing requirements
- Content management systems
- Real-time analytics
- IoT applications
- Mobile app backends
- Storing semi-structured or unstructured data

**Document example:**
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
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

This guide contains instructions for deploying MongoDB on Kubernetes.
The provided Helm chart deploys a MongoDB database using a StatefulSet with persistent storage. The chart includes:

- MongoDB deployment via StatefulSet
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
| `DBUser` | MongoDB root username | `admin` |
| `DBPassword` | MongoDB root password | `TODO` |
| `DBName` | Initial database name | `appdb` |
| `DBImage` | Docker image for MongoDB | `mongo:7` |
| `DBResourceLimit` | Enable resource limits | `false` |
| `DBCPU` | CPU limit | `500m` |
| `DBMemory` | Memory limit | `512Mi` |
| `DBStorage` | Storage size for persistent volume | `10Gi` |

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

### Linux (Debian/Ubuntu)

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install mongodb-mongosh
```

### Linux (Fedora/RHEL/CentOS)

```bash
sudo dnf install mongodb-mongosh
```

### Linux (Arch)

```bash
yay -S mongosh-bin
```

### macOS (Homebrew)

```bash
brew install mongosh
```

### Windows (Chocolatey)

```powershell
choco install mongodb-shell
```

### Docker Alternative (Any Platform)

If you prefer not to install locally, use Docker:

```bash
docker run -it --rm --network host mongo:7 mongosh mongodb://localhost:27017
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

Now you can connect using mongosh:

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
kubectl exec -it -n db mongodb-0 -- mongosh -u admin -p your-password --authenticationDatabase admin
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
app.put('/students/:id', async (req, res) => {
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
});
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

**Note**: This will not delete the PersistentVolumeClaim by default. To completely remove all data:

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
kubectl run -it --rm debug --image=mongo:7 --restart=Never -n db -- mongosh mongodb://mongodb-service:27017
```

### Authentication Issues

Check if the credentials in the ConfigMap match your values.yaml:
```bash
kubectl get configmap -n db mongodb-config -o yaml
```

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
