#!/usr/bin/env python3
"""
RabbitMQ Worker - Parallel Processing Demo

Processes tasks from the work queue. Run multiple instances to see how
RabbitMQ distributes work across workers using fair dispatch.

Usage:
    python worker.py <worker_id>

Examples:
    # Terminal 1
    python worker.py 1

    # Terminal 2
    python worker.py 2

    # Terminal 3
    python worker.py 3

Then run producer_many.py to send 20 tasks and watch them being
distributed across all workers!
"""
import pika
import json
import time
import os
import sys

# Get worker ID from command line argument
WORKER_ID = sys.argv[1] if len(sys.argv) > 1 else "1"
RABBITMQ_HOST = 'localhost'  # Change to 'rabbitmq-service-api' if inside K8s

print(f"[Worker {WORKER_ID}] Starting...")
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials('admin', 'changeme123')
        )
    )
    channel = connection.channel()
except Exception as e:
    print(f"[Worker {WORKER_ID}] ERROR: Could not connect to RabbitMQ: {e}")
    print(f"[Worker {WORKER_ID}] If testing locally, run: kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672")
    sys.exit(1)

channel.queue_declare(queue='work_queue', durable=True)
channel.basic_qos(prefetch_count=1)  # Fair dispatch

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[Worker {WORKER_ID}] Got task #{data['task_id']}")

    # Simulate variable processing time (1-3 seconds)
    time.sleep(1 + (data['task_id'] % 3))

    print(f"[Worker {WORKER_ID}] ✓ Completed task #{data['task_id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='work_queue', on_message_callback=callback, auto_ack=False)
print(f"[Worker {WORKER_ID}] Ready! Waiting for tasks...")
print(f"[Worker {WORKER_ID}] Press CTRL+C to exit\n")
channel.start_consuming()
