# RabbitMQ Examples - Quick Start

Run commands from `advanced/14-service-communication/examples/`. These examples demonstrate RabbitMQ message queues with **automatic retry on crash** using message acknowledgments.

## What Each Process Does

`pip install -r requirements.txt` installs the Python AMQP client dependencies; it does not start a broker. `kubectl port-forward ... 5672:5672` keeps a local connection path to the cluster's broker open. Run producers and consumers in separate terminals with that path available.

`consumer_simple.py` waits for deliveries. `producer_simple.py` publishes and exits. The crash demo intentionally ends a consumer before some work is acknowledged; inspect ready and unacknowledged queue counts before and after reconnecting a consumer. A worker identifier labels a process; it does not create a separate queue automatically.

**Explain the result:** Why can a consumer legitimately wait without printing more output? Why does redelivery after a crash not imply that its side effect could never have happened already? Read the [main command explanations](../README.md#understand-what-the-broker-and-example-commands-start) and [shell guide](../../../COMMANDS.md) before running the experiment.

## Prerequisites

1. **Deploy RabbitMQ** to your Kubernetes cluster (see main Tutorial 14 README)
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

**To complete:** Stop other consumers before the crash demo. The script crashes on the first delivery of task ID 3 and processes it normally when it is redelivered; the restarted script continues with the remaining tasks.

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
- Set `RABBITMQ_HOST=rabbitmq-service-api` in the same namespace, or `rabbitmq-service-api.rabbitmq.svc.cluster.local` from another namespace. Set `RABBITMQ_PORT`, `RABBITMQ_USER`, and `RABBITMQ_PASSWORD` to override defaults.

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
- Check credentials configured in the `rabbitmq-credentials` Secret
- Default is `admin` / `changeme123`

**Messages not delivered:**
- Ensure `auto_ack=False` and calling `ch.basic_ack()`
- Check queue names match between producer and consumer
- View queues in management UI: `http://localhost:15672` after forwarding `svc/rabbitmq-service-management`

## Next Steps

See the main Tutorial 14 README for:
- Dead letter queues
- Production best practices
- Deploying consumers to Kubernetes
- Advanced patterns (pub/sub, topic routing, RPC)
