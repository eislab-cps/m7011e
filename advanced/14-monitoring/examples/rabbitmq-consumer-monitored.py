#!/usr/bin/env python3
"""
RabbitMQ Consumer with Prometheus Metrics

This consumer processes messages from RabbitMQ and exposes
Prometheus metrics about message processing.

Exposes metrics at http://localhost:8000/metrics

Metrics exposed:
- rabbitmq_messages_received_total: Total messages received
- rabbitmq_messages_processed_total: Successfully processed messages
- rabbitmq_messages_failed_total: Failed messages
- rabbitmq_message_processing_seconds: Processing time histogram
- rabbitmq_consumer_queue_depth: Current queue depth
"""

import pika
import json
import time
import sys
import os
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import random

# Start Prometheus metrics HTTP server on port 8000
start_http_server(8000)

# Define Prometheus metrics
messages_received = Counter(
    'rabbitmq_messages_received_total',
    'Total messages received from RabbitMQ',
    ['queue', 'service']
)

messages_processed = Counter(
    'rabbitmq_messages_processed_total',
    'Total messages processed successfully',
    ['queue', 'service']
)

messages_failed = Counter(
    'rabbitmq_messages_failed_total',
    'Total messages that failed processing',
    ['queue', 'service']
)

processing_time = Histogram(
    'rabbitmq_message_processing_seconds',
    'Time spent processing messages',
    ['queue', 'service']
)

queue_depth = Gauge(
    'rabbitmq_consumer_queue_depth',
    'Current number of messages in queue',
    ['queue', 'service']
)

# Configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')  # Defaults to localhost, set via env var in K8s
QUEUE_NAME = 'email_notifications'
SERVICE_NAME = os.getenv('SERVICE_NAME', 'notification-consumer')

def send_email(email, order_id):
    """Simulate sending email (with occasional failures for demo)"""
    # Simulate processing time
    time.sleep(random.uniform(0.5, 2.0))

    # Simulate occasional failures (10% error rate)
    if random.random() < 0.1:
        raise Exception(f"Email service unavailable")

    print(f"[{SERVICE_NAME}] ✓ Sent email to {email} for order {order_id}")

def callback(ch, method, properties, body):
    """Process received message"""
    # Record that we received a message
    messages_received.labels(queue=QUEUE_NAME, service=SERVICE_NAME).inc()

    start_time = time.time()

    try:
        # Parse message
        data = json.loads(body)
        print(f"\n[{SERVICE_NAME}] Processing message: {data}")

        # Process the message (send email)
        send_email(data.get('email'), data.get('order_id'))

        # Record successful processing
        duration = time.time() - start_time
        processing_time.labels(queue=QUEUE_NAME, service=SERVICE_NAME).observe(duration)
        messages_processed.labels(queue=QUEUE_NAME, service=SERVICE_NAME).inc()

        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[{SERVICE_NAME}] Message processed in {duration:.2f}s")

    except Exception as e:
        # Record failed processing
        messages_failed.labels(queue=QUEUE_NAME, service=SERVICE_NAME).inc()

        print(f"[{SERVICE_NAME}] ✗ Error processing message: {e}")

        # NACK and requeue for retry
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        print(f"[{SERVICE_NAME}] Message requeued for retry")

def update_queue_depth(channel):
    """Update queue depth metric"""
    try:
        method = channel.queue_declare(queue=QUEUE_NAME, passive=True)
        depth = method.method.message_count
        queue_depth.labels(queue=QUEUE_NAME, service=SERVICE_NAME).set(depth)
        print(f"[{SERVICE_NAME}] Queue depth: {depth} messages")
    except Exception as e:
        print(f"[{SERVICE_NAME}] Could not get queue depth: {e}")

# Connect to RabbitMQ with retry logic
print(f"[{SERVICE_NAME}] Connecting to RabbitMQ at {RABBITMQ_HOST}...")
max_retries = 30
retry_delay = 2

connection = None
for attempt in range(1, max_retries + 1):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                credentials=pika.PlainCredentials('admin', 'changeme123'),
                connection_attempts=3,
                retry_delay=1
            )
        )
        channel = connection.channel()
        print(f"[{SERVICE_NAME}] Connected successfully!")
        break
    except Exception as e:
        if attempt < max_retries:
            print(f"[{SERVICE_NAME}] Connection attempt {attempt}/{max_retries} failed: {e}")
            print(f"[{SERVICE_NAME}] Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"[{SERVICE_NAME}] ERROR: Could not connect to RabbitMQ after {max_retries} attempts: {e}")
            print(f"[{SERVICE_NAME}] Make sure RabbitMQ is running and accessible")
            print(f"[{SERVICE_NAME}] If testing locally, run: kubectl port-forward -n monitoring svc/rabbitmq 5672:5672")
            sys.exit(1)

if connection is None:
    print(f"[{SERVICE_NAME}] ERROR: Failed to establish connection")
    sys.exit(1)

# Declare queue
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Set prefetch count for fair dispatch
channel.basic_qos(prefetch_count=1)

# Get initial queue depth
update_queue_depth(channel)

# Start consuming messages
channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
    auto_ack=False  # Manual acknowledgment
)

print(f"\n{'='*60}")
print(f"[{SERVICE_NAME}] Started successfully!")
print(f"[{SERVICE_NAME}] Listening to queue: '{QUEUE_NAME}'")
print(f"[{SERVICE_NAME}] Metrics available at: http://localhost:8000/metrics")
print(f"[{SERVICE_NAME}] Press CTRL+C to exit")
print(f"{'='*60}\n")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\n[{SERVICE_NAME}] Shutting down...")
    channel.stop_consuming()
    connection.close()
    print(f"[{SERVICE_NAME}] Stopped")
