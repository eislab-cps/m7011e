# RabbitMQ Examples - Quick Start

These examples demonstrate RabbitMQ message queues with **automatic retry on crash** using message acknowledgments.

## Prerequisites

1. **Deploy RabbitMQ** to your Kubernetes cluster (see main Tutorial 12 README)
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Port-forward RabbitMQ** (if testing locally):
   ```bash
   kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672
   ```

## Example 1: Simple Producer and Consumer

**Basic message queue with acknowledgments.**

```bash
# Terminal 1: Start consumer first
python consumer_simple.py

# Terminal 2: Send 5 messages
python producer_simple.py
```

**What you'll see:** Consumer receives and processes each message, sending ACK after completion.

## Example 2: Crash Recovery (THE KEY FEATURE)

**Demonstrates automatic retry when consumer crashes without sending ACK.**

```bash
# Step 1: Send 5 messages to the queue
python producer_simple.py

# Step 2: Run consumer that crashes on message #3
python consumer_crash_demo.py
# Output: Processes messages #1, #2, then CRASHES on #3 (no ACK sent)

# Step 3: Restart consumer - message #3 is automatically redelivered!
python consumer_crash_demo.py
# Output: Immediately receives message #3 again (RabbitMQ redelivered it)
```

**Key observation:** Message #3 was never lost even though the consumer crashed. RabbitMQ automatically retried delivery.

**To complete:** Edit `consumer_crash_demo.py` and comment out the crash logic (lines 59-64), then run again to process all remaining messages.

## Example 3: Multiple Workers (Parallel Processing)

**See how RabbitMQ distributes work across multiple consumers.**

```bash
# Terminal 1: Worker 1
python worker.py 1

# Terminal 2: Worker 2
python worker.py 2

# Terminal 3: Worker 3
python worker.py 3

# Terminal 4: Send 20 tasks
python producer_many.py
```

**What you'll see:** All 3 workers receive tasks in parallel. RabbitMQ distributes fairly using `prefetch_count=1`.

## Files

- `producer_simple.py` - Sends 5 test messages
- `consumer_simple.py` - Basic consumer with ACK
- `consumer_crash_demo.py` - **Demonstrates crash recovery and automatic retry**
- `producer_many.py` - Sends 20 tasks for parallel processing
- `worker.py` - Worker that accepts worker ID parameter
- `requirements.txt` - Python dependencies (pika)

## Configuration

**Running inside Kubernetes cluster:**
- Change `RABBITMQ_HOST = 'localhost'` to `RABBITMQ_HOST = 'rabbitmq-service-api'`

**RabbitMQ credentials:**

Default credentials (configured in `values.yaml`):
- Username: `admin`
- Password: `changeme123`

**⚠️ IMPORTANT:** Change these in `values.yaml` for production!

## Troubleshooting

**Connection refused:**
```bash
# Check RabbitMQ is running
kubectl get pods -n rabbitmq

# Ensure port-forward is active (if testing locally)
kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672
```

**Authentication failed:**
- Check credentials in `rabbitmq-configmap.yaml`
- Default is `admin` / `changeme123`

**Messages not delivered:**
- Ensure `auto_ack=False` and calling `ch.basic_ack()`
- Check queue names match between producer and consumer
- View queues in management UI: `https://rabbitmq.ltu-m7011e-YOUR-NAME.se`

## Next Steps

See the main Tutorial 12 README for:
- Dead letter queues
- Production best practices
- Deploying consumers to Kubernetes
- Advanced patterns (pub/sub, topic routing, RPC)
