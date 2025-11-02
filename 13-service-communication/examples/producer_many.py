#!/usr/bin/env python3
"""
RabbitMQ Producer - Multiple Tasks

Sends 20 tasks to demonstrate parallel processing with multiple workers.
Use this with worker.py running in multiple terminals to see work distribution.

Usage:
    python producer_many.py
"""
import pika
import json
import sys

# Connect to RabbitMQ
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
    print(f"[Producer] If testing locally, run: kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672")
    sys.exit(1)

channel.queue_declare(queue='work_queue', durable=True)

# Send 20 messages
print("[Producer] Sending 20 tasks to work queue...")
for i in range(1, 21):
    message = {"task_id": i, "description": f"Task number {i}"}
    channel.basic_publish(
        exchange='',
        routing_key='work_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[Producer] Queued task #{i}")

connection.close()
print("[Producer] Done! 20 tasks queued")
print("[Producer] Run multiple workers with: python worker.py <worker_id>")
