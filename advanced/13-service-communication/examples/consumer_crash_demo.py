#!/usr/bin/env python3
"""
RabbitMQ Crash Recovery Demonstration

This consumer intentionally crashes on message #3 to demonstrate automatic
retry via message acknowledgments. When you restart it, RabbitMQ automatically
redelivers message #3 because no ACK was sent.

This shows the key feature of RabbitMQ: messages are never lost even if
the consumer crashes mid-processing.

Usage:
    1. Run producer_simple.py to send 5 messages
    2. Run this consumer - it will crash on message #3
    3. Restart this consumer - message #3 is automatically redelivered!

    python consumer_crash_demo.py
"""
import pika
import json
import time
import sys

# Connect to RabbitMQ
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
channel.basic_qos(prefetch_count=1)

message_count = 0

def callback(ch, method, properties, body):
    global message_count
    message_count += 1

    data = json.loads(body)
    print(f"\n[Consumer] Received message #{message_count}: {data['task']}")

    # Simulate processing
    print(f"[Consumer] Processing task #{data['id']}...")
    time.sleep(2)

    # CRASH on message #3 to demonstrate redelivery
    if message_count == 3:
        print(f"\n" + "="*60)
        print(f"[Consumer] !!! SIMULATING CRASH on message #3 !!!")
        print(f"[Consumer] !!! NOT sending ACK !!!")
        print(f"[Consumer] Message #{message_count} will be REDELIVERED when service restarts")
        print("="*60 + "\n")
        sys.exit(1)  # Crash the process

    # Normal processing - send ACK
    print(f"[Consumer] ✓ Completed task #{data['id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[Consumer] Sent ACK to RabbitMQ")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

print(f"[Consumer] Waiting for messages...")
print(f"[Consumer] This consumer will CRASH on message #3 to demonstrate auto-retry")
print("[Consumer] Press CTRL+C to exit\n")

channel.start_consuming()
