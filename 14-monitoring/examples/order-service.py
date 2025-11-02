#!/usr/bin/env python3
"""
Order Service - Flask API with Prometheus Metrics

This service demonstrates how to instrument a Flask application
with Prometheus metrics for monitoring.

Exposes metrics at http://localhost:8001/metrics

Metrics exposed:
- http_requests_total: Total HTTP requests
- http_request_duration_seconds: HTTP request latency
- orders_created_total: Total orders created
- active_orders: Current number of active orders
"""

from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time
import random

app = Flask(__name__)

# Define Prometheus metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status', 'service']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint', 'service']
)

orders_created = Counter(
    'orders_created_total',
    'Total number of orders created',
    ['service']
)

active_orders = Gauge(
    'active_orders',
    'Number of currently active orders',
    ['service']
)

# Service name for labels
SERVICE_NAME = 'order-service'

# Simulate some active orders
active_orders.labels(service=SERVICE_NAME).set(42)

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(REGISTRY)

@app.route('/health')
def health():
    """Health check endpoint"""
    start_time = time.time()

    response = {'status': 'healthy', 'service': SERVICE_NAME}

    request_count.labels(
        method='GET',
        endpoint='/health',
        status=200,
        service=SERVICE_NAME
    ).inc()

    request_duration.labels(
        method='GET',
        endpoint='/health',
        service=SERVICE_NAME
    ).observe(time.time() - start_time)

    return jsonify(response), 200

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    start_time = time.time()

    try:
        # Simulate fetching orders from database
        time.sleep(random.uniform(0.01, 0.1))

        orders = [
            {'id': 1, 'user_id': 123, 'total': 99.99, 'status': 'completed'},
            {'id': 2, 'user_id': 456, 'total': 149.99, 'status': 'pending'},
            {'id': 3, 'user_id': 789, 'total': 79.99, 'status': 'shipped'}
        ]

        # Record metrics
        request_count.labels(
            method='GET',
            endpoint='/api/orders',
            status=200,
            service=SERVICE_NAME
        ).inc()

        request_duration.labels(
            method='GET',
            endpoint='/api/orders',
            service=SERVICE_NAME
        ).observe(time.time() - start_time)

        return jsonify(orders), 200

    except Exception as e:
        # Record error
        request_count.labels(
            method='GET',
            endpoint='/api/orders',
            status=500,
            service=SERVICE_NAME
        ).inc()

        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    start_time = time.time()

    try:
        data = request.get_json()

        # Simulate order creation (with occasional errors for demo)
        if random.random() < 0.1:  # 10% error rate
            raise Exception("Database connection failed")

        # Simulate processing time
        time.sleep(random.uniform(0.05, 0.2))

        order = {
            'id': random.randint(1000, 9999),
            'user_id': data.get('user_id'),
            'items': data.get('items'),
            'total': data.get('total'),
            'status': 'pending'
        }

        # Update metrics
        orders_created.labels(service=SERVICE_NAME).inc()
        active_orders.labels(service=SERVICE_NAME).inc()

        request_count.labels(
            method='POST',
            endpoint='/api/orders',
            status=201,
            service=SERVICE_NAME
        ).inc()

        request_duration.labels(
            method='POST',
            endpoint='/api/orders',
            service=SERVICE_NAME
        ).observe(time.time() - start_time)

        return jsonify(order), 201

    except Exception as e:
        # Record error metrics
        request_count.labels(
            method='POST',
            endpoint='/api/orders',
            status=500,
            service=SERVICE_NAME
        ).inc()

        request_duration.labels(
            method='POST',
            endpoint='/api/orders',
            service=SERVICE_NAME
        ).observe(time.time() - start_time)

        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order"""
    start_time = time.time()

    try:
        # Simulate slow query occasionally
        if random.random() < 0.2:  # 20% chance of slow query
            time.sleep(random.uniform(0.5, 1.5))
        else:
            time.sleep(random.uniform(0.01, 0.05))

        order = {
            'id': order_id,
            'user_id': 123,
            'total': 99.99,
            'status': 'completed'
        }

        request_count.labels(
            method='GET',
            endpoint='/api/orders/:id',
            status=200,
            service=SERVICE_NAME
        ).inc()

        request_duration.labels(
            method='GET',
            endpoint='/api/orders/:id',
            service=SERVICE_NAME
        ).observe(time.time() - start_time)

        return jsonify(order), 200

    except Exception as e:
        request_count.labels(
            method='GET',
            endpoint='/api/orders/:id',
            status=500,
            service=SERVICE_NAME
        ).inc()

        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"[{SERVICE_NAME}] Starting on http://0.0.0.0:8001")
    print(f"[{SERVICE_NAME}] Metrics available at http://0.0.0.0:8001/metrics")
    print(f"[{SERVICE_NAME}] Health check at http://0.0.0.0:8001/health")
    app.run(host='0.0.0.0', port=8001, debug=False)
