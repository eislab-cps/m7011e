#!/usr/bin/env python3
"""
Simple RabbitMQ Consumer Example

Receives messages from a queue and processes them with acknowledgments.
Run producer_simple.py first to send messages to the queue.

Usage:
    python consumer_simple.py
"""
import pika
import json
import time
import sys

# Connect to RabbitMQ
# If running locally or via port-forward: use 'localhost'
# If running inside Kubernetes cluster: use 'rabbitmq-service-api'
RABBITMQ_HOST = 'localhost'  # Change to 'rabbitmq-service-api' if inside K8s

print(f"[Consumer] Connecting to RabbitMQ at {RABBITMQ_HOST}...")
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials('admin', 'changeme123')
        )
    )
    channel = connection.channel()
except Exception as e:
    print(f"[Consumer] ERROR: Could not connect to RabbitMQ: {e}")
    print(f"[Consumer] Make sure RabbitMQ is running and accessible at {RABBITMQ_HOST}")
    print(f"[Consumer] If testing locally, run: kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672")
    sys.exit(1)

queue_name = 'test_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Fair dispatch - only get one message at a time
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"\n[Consumer] Received: {data['task']}")

    # Simulate processing work
    print(f"[Consumer] Processing task #{data['id']}...")
    time.sleep(2)  # Simulate 2 seconds of work

    print(f"[Consumer] ✓ Completed task #{data['id']}")

    # Send acknowledgment - VERY IMPORTANT!
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[Consumer] Sent ACK to RabbitMQ\n")

# Start consuming with manual acknowledgment
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False  # Manual acknowledgment
)

print(f"[Consumer] Waiting for messages from '{queue_name}'...")
print("[Consumer] Press CTRL+C to exit\n")
channel.start_consuming()
