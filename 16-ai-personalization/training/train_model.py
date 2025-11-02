#!/usr/bin/env python3
"""
Simple collaborative filtering model training script.

This trains a recommendation model using Matrix Factorization (NMF)
from user purchase history.

Usage:
    python train_model.py
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
import joblib

def train_model():
    print("Loading training data...")
    data = pd.read_csv('sample_data.csv')

    # Create user-item interaction matrix
    print("Creating user-item matrix...")
    matrix = data.pivot_table(
        index='user_id',
        columns='item_id',
        values='purchased',
        fill_value=0
    )

    print(f"Matrix shape: {matrix.shape}")
    print(f"Users: {len(matrix.index)}, Items: {len(matrix.columns)}")

    # Train Matrix Factorization model
    print("\nTraining collaborative filtering model...")
    n_components = min(10, min(matrix.shape) - 1)  # Ensure valid dimensions

    model = NMF(
        n_components=n_components,
        init='random',
        random_state=42,
        max_iter=200,
        verbose=1
    )

    user_features = model.fit_transform(matrix)
    item_features = model.components_

    print(f"\n✅ Model trained!")
    print(f"User features shape: {user_features.shape}")
    print(f"Item features shape: {item_features.shape}")

    # Create item name mapping
    item_names = data[['item_id', 'item_name']].drop_duplicates()
    item_name_dict = dict(zip(item_names['item_id'], item_names['item_name']))

    # Save model components
    print("\nSaving model files...")
    joblib.dump(user_features, 'user_features.pkl')
    joblib.dump(item_features, 'item_features.pkl')
    joblib.dump(matrix.index.tolist(), 'user_ids.pkl')
    joblib.dump(matrix.columns.tolist(), 'item_ids.pkl')
    joblib.dump(item_name_dict, 'item_names.pkl')

    print("✅ Model saved successfully!")
    print("\nGenerated files:")
    print("  - user_features.pkl")
    print("  - item_features.pkl")
    print("  - user_ids.pkl")
    print("  - item_ids.pkl")
    print("  - item_names.pkl")

    return model, user_features, item_features

def test_recommendations(user_features, item_features, user_ids, item_ids, item_names):
    """Test the model with sample recommendations"""
    print("\n" + "="*60)
    print("Testing Recommendations")
    print("="*60)

    # Test for user 1
    test_user_id = 1
    user_idx = user_ids.index(test_user_id)
    user_vector = user_features[user_idx]

    # Compute scores
    scores = np.dot(user_vector, item_features)

    # Get top 5 items
    top_indices = np.argsort(scores)[-5:][::-1]

    print(f"\nTop 5 recommendations for User {test_user_id}:")
    for i, idx in enumerate(top_indices, 1):
        item_id = item_ids[idx]
        score = scores[idx]
        name = item_names[item_id]
        print(f"  {i}. {name} (ID: {item_id}, Score: {score:.3f})")

if __name__ == '__main__':
    # Train model
    model, user_features, item_features = train_model()

    # Load saved components for testing
    user_ids = joblib.load('user_ids.pkl')
    item_ids = joblib.load('item_ids.pkl')
    item_names = joblib.load('item_names.pkl')

    # Test recommendations
    test_recommendations(user_features, item_features, user_ids, item_ids, item_names)
