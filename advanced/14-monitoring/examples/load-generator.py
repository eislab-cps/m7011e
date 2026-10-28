#!/usr/bin/env python3
"""
Load Generator for Testing Monitoring

Generates traffic to the Order Service API and RabbitMQ
to produce metrics for visualization in Grafana.

Usage:
    python load-generator.py
"""

import requests
import pika
import json
import time
import random
import os
from threading import Thread

# Configuration
# Can be overridden with environment variables:
# - ORDER_SERVICE_URL: URL to order service (default: http://localhost:8001)
# - RABBITMQ_HOST: RabbitMQ host (default: localhost)
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://localhost:8001')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

def generate_http_traffic():
    """Generate HTTP requests to Order Service"""
    print("[Load Generator] Starting HTTP traffic generation...")

    while True:
        try:
            # GET /api/orders (most common)
            if random.random() < 0.6:
                response = requests.get(f"{ORDER_SERVICE_URL}/api/orders")
                print(f"[HTTP] GET /api/orders -> {response.status_code}")

            # POST /api/orders (create order)
            elif random.random() < 0.3:
                order_data = {
                    'user_id': random.randint(100, 999),
                    'items': ['item1', 'item2'],
                    'total': random.uniform(50, 500)
                }
                response = requests.post(
                    f"{ORDER_SERVICE_URL}/api/orders",
                    json=order_data
                )
                print(f"[HTTP] POST /api/orders -> {response.status_code}")

            # GET /api/orders/:id
            else:
                order_id = random.randint(1, 100)
                response = requests.get(f"{ORDER_SERVICE_URL}/api/orders/{order_id}")
                print(f"[HTTP] GET /api/orders/{order_id} -> {response.status_code}")

            # Random delay between requests
            time.sleep(random.uniform(0.1, 2.0))

        except Exception as e:
            print(f"[HTTP] Error: {e}")
            time.sleep(5)

def generate_rabbitmq_traffic():
    """Generate messages to RabbitMQ"""
    print("[Load Generator] Starting RabbitMQ traffic generation...")

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                credentials=pika.PlainCredentials('admin', 'changeme123')
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='email_notifications', durable=True)

        message_id = 1
        while True:
            try:
                message = {
                    'email': f'user{random.randint(1, 1000)}@example.com',
                    'order_id': random.randint(10000, 99999),
                    'message': f'Your order has been confirmed'
                }

                channel.basic_publish(
                    exchange='',
                    routing_key='email_notifications',
                    body=json.dumps(message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )

                print(f"[RabbitMQ] Published message #{message_id}")
                message_id += 1

                # Random delay between messages
                time.sleep(random.uniform(0.5, 3.0))

            except Exception as e:
                print(f"[RabbitMQ] Error: {e}")
                time.sleep(5)

    except Exception as e:
        print(f"[RabbitMQ] Connection error: {e}")
        print(f"[RabbitMQ] Make sure RabbitMQ is accessible")

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║           Load Generator for Monitoring Demo                 ║
╚══════════════════════════════════════════════════════════════╝

This script generates:
  • HTTP traffic to Order Service (http://localhost:5000)
  • Messages to RabbitMQ queue 'email_notifications'

Make sure the following are running:
  1. Order Service: python order-service.py
  2. RabbitMQ Consumer: python rabbitmq-consumer-monitored.py
  3. Port-forward: kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672

Metrics endpoints:
  • Order Service: http://localhost:5000/metrics
  • Consumer: http://localhost:8000/metrics
  • Prometheus: http://localhost:9090
  • Grafana: http://localhost:3000

Press CTRL+C to stop
""")

    # Start HTTP traffic generator in a thread
    http_thread = Thread(target=generate_http_traffic, daemon=True)
    http_thread.start()

    # Start RabbitMQ traffic generator in a thread
    rabbitmq_thread = Thread(target=generate_rabbitmq_traffic, daemon=True)
    rabbitmq_thread.start()

    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Load Generator] Stopping...")
        print("[Load Generator] Stopped")
