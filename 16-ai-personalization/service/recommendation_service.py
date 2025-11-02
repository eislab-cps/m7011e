#!/usr/bin/env python3
"""
Recommendation Service - ML-powered product recommendations

This microservice serves personalized recommendations using a pre-trained
collaborative filtering model. It includes Redis caching and Prometheus metrics.

Usage:
    python recommendation_service.py
"""

from flask import Flask, jsonify, request
import joblib
import numpy as np
import redis
import json
import os
from prometheus_client import Counter, Histogram, Gauge, generate_latest

app = Flask(__name__)

# Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour

# Redis client
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
        socket_connect_timeout=5
    )
    redis_client.ping()
    print(f"✅ Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    print(f"⚠️  Redis not available: {e}")
    redis_client = None

# Load pre-trained model
print("Loading ML model...")
user_features = joblib.load('user_features.pkl')
item_features = joblib.load('item_features.pkl')
user_ids = joblib.load('user_ids.pkl')
item_ids = joblib.load('item_ids.pkl')
item_names = joblib.load('item_names.pkl')
print(f"✅ Model loaded: {len(user_ids)} users, {len(item_ids)} items")

# Prometheus metrics
requests_total = Counter(
    'recommendation_requests_total',
    'Total recommendation requests',
    ['endpoint']
)
cache_hits = Counter(
    'recommendation_cache_hits_total',
    'Number of cache hits'
)
cache_misses = Counter(
    'recommendation_cache_misses_total',
    'Number of cache misses'
)
latency = Histogram(
    'recommendation_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)
model_predictions = Counter(
    'recommendation_model_predictions_total',
    'Number of times model was invoked'
)
active_users = Gauge(
    'recommendation_active_users',
    'Number of users with cached recommendations'
)

def get_recommendations(user_id, top_n=5):
    """Generate recommendations for a user"""
    try:
        user_idx = user_ids.index(int(user_id))
    except (ValueError, IndexError):
        # User not in training data - return popular items
        return get_popular_items(top_n)

    # Get user's feature vector
    user_vector = user_features[user_idx]

    # Compute scores for all items
    scores = np.dot(user_vector, item_features)

    # Get top N items
    top_indices = np.argsort(scores)[-top_n:][::-1]

    recommendations = []
    for idx in top_indices:
        item_id = item_ids[idx]
        score = float(scores[idx])
        name = item_names.get(item_id, f"Item {item_id}")

        recommendations.append({
            'item_id': str(item_id),
            'item_name': name,
            'score': round(score, 3)
        })

    return recommendations

def get_popular_items(top_n=5):
    """Fallback: return most popular items"""
    # Simple fallback - return first N items
    popular = []
    for item_id in list(item_ids)[:top_n]:
        popular.append({
            'item_id': str(item_id),
            'item_name': item_names.get(item_id, f"Item {item_id}"),
            'score': 0.5
        })
    return popular

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'recommendation-service'})

@app.route('/api/recommendations/<user_id>')
def api_recommendations(user_id):
    """Get personalized recommendations for a user"""
    with latency.labels(endpoint='recommendations').time():
        requests_total.labels(endpoint='recommendations').inc()

        # Check cache
        cache_key = f"recs:{user_id}"
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    cache_hits.inc()
                    return cached, 200, {'Content-Type': 'application/json'}
            except Exception as e:
                print(f"Cache read error: {e}")

        # Cache miss - generate recommendations
        cache_misses.inc()
        model_predictions.inc()

        top_n = request.args.get('top_n', default=5, type=int)
        top_n = min(top_n, 20)  # Max 20 recommendations

        recommendations = get_recommendations(user_id, top_n)

        result = {
            'user_id': user_id,
            'recommendations': recommendations,
            'cached': False
        }

        response_json = json.dumps(result)

        # Cache result
        if redis_client:
            try:
                redis_client.setex(cache_key, CACHE_TTL, response_json)
            except Exception as e:
                print(f"Cache write error: {e}")

        return response_json, 200, {'Content-Type': 'application/json'}

@app.route('/api/popular')
def api_popular():
    """Get popular items (no personalization)"""
    with latency.labels(endpoint='popular').time():
        requests_total.labels(endpoint='popular').inc()

        top_n = request.args.get('top_n', default=10, type=int)
        popular = get_popular_items(min(top_n, 20))

        return jsonify({
            'popular_items': popular
        })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    # Update active users gauge
    if redis_client:
        try:
            # Count keys matching "recs:*"
            cursor = 0
            count = 0
            while True:
                cursor, keys = redis_client.scan(cursor, match='recs:*', count=100)
                count += len(keys)
                if cursor == 0:
                    break
            active_users.set(count)
        except:
            pass

    return generate_latest()

@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'service': 'Recommendation Service',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/recommendations/<user_id>': 'Get personalized recommendations',
            'GET /api/popular': 'Get popular items',
            'GET /health': 'Health check',
            'GET /metrics': 'Prometheus metrics'
        },
        'model_info': {
            'users': len(user_ids),
            'items': len(item_ids),
            'algorithm': 'Collaborative Filtering (NMF)'
        }
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Recommendation Service Starting")
    print("="*60)
    print(f"Model: {len(user_ids)} users, {len(item_ids)} items")
    print(f"Redis: {REDIS_HOST}:{REDIS_PORT}")
    print(f"Cache TTL: {CACHE_TTL} seconds")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=8080, debug=False)
