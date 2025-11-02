#!/usr/bin/env python3
"""
Simple RabbitMQ Producer Example

Sends 5 messages to a queue. Run this first, then run consumer_simple.py
to see the messages being processed.

Usage:
    python producer_simple.py
"""
import pika
import json
import sys

# Connect to RabbitMQ
# If running locally or via port-forward: use 'localhost'
# If running inside Kubernetes cluster: use 'rabbitmq-service-api'
RABBITMQ_HOST = 'localhost'  # Change to 'rabbitmq-service-api' if inside K8s

print(f"[Producer] Connecting to RabbitMQ at {RABBITMQ_HOST}...")
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials('admin', 'changeme123')
        )
    )
    channel = connection.channel()
except Exception as e:
    print(f"[Producer] ERROR: Could not connect to RabbitMQ: {e}")
    print(f"[Producer] Make sure RabbitMQ is running and accessible at {RABBITMQ_HOST}")
    print(f"[Producer] If testing locally, run: kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672")
    sys.exit(1)

# Declare a durable queue (survives RabbitMQ restart)
queue_name = 'test_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Send 5 messages
print(f"[Producer] Sending 5 messages to queue '{queue_name}'...\n")
for i in range(1, 6):
    message = {
        "id": i,
        "task": f"Process task #{i}",
        "data": f"Some data for task {i}"
    }

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    print(f"[Producer] ✓ Sent message #{i}: {message['task']}")

connection.close()
print(f"\n[Producer] Done! Sent 5 messages to queue '{queue_name}'")
print(f"[Producer] Run 'python consumer_simple.py' to process these messages")
