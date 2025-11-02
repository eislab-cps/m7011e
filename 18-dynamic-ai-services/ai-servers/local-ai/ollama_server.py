#!/usr/bin/env python3
"""
Local AI Server using Ollama - Run AI models locally

This server provides AI capabilities using locally-run models via Ollama.
No API keys needed, no costs, data stays on your machine.
"""

from flask import Flask, jsonify, request
import os
import requests
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

# Configuration
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
DEFAULT_MODEL = os.getenv('AI_MODEL', 'llama3.2')  # or llama2, mistral, phi, etc.

# Metrics
ai_calls = Counter('ai_calls_total', 'Total AI API calls', ['tool', 'model'])
ai_tokens = Counter('ai_tokens_total', 'Total tokens used', ['type', 'model'])
ai_api_latency = Histogram('ai_api_latency_seconds', 'AI API latency', ['model'])

def generate_with_ollama(prompt: str, model: str = DEFAULT_MODEL):
    """Generate content using Ollama"""
    try:
        with ai_api_latency.labels(model=model).time():
            response = requests.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60  # Longer timeout for local models
            )
            response.raise_for_status()

        data = response.json()

        # Estimate tokens (Ollama doesn't always provide this)
        content = data.get('response', '')
        estimated_input_tokens = len(prompt.split())
        estimated_output_tokens = len(content.split())

        ai_tokens.labels(type='input', model=model).inc(estimated_input_tokens)
        ai_tokens.labels(type='output', model=model).inc(estimated_output_tokens)

        return {
            'success': True,
            'content': content,
            'model': model,
            'tokens': {
                'input': estimated_input_tokens,
                'output': estimated_output_tokens
            }
        }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timeout - local model may need more time'
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': f'Cannot connect to Ollama at {OLLAMA_HOST}. Is it running?'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/health')
def health():
    """Health check - also verifies Ollama is accessible"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get('models', [])

        return jsonify({
            'status': 'healthy',
            'service': 'local-ai (Ollama)',
            'ollama_host': OLLAMA_HOST,
            'available_models': [m['name'] for m in models],
            'default_model': DEFAULT_MODEL
        })
    except:
        return jsonify({
            'status': 'unhealthy',
            'service': 'local-ai (Ollama)',
            'error': 'Cannot connect to Ollama'
        }), 503

@app.route('/call_tool', methods=['POST'])
def call_tool():
    """Handle tool calls from services"""

    data = request.json
    tool_name = data.get('tool')
    arguments = data.get('arguments', {})
    model = data.get('model', DEFAULT_MODEL)

    ai_calls.labels(tool=tool_name, model=model).inc()

    if tool_name == 'generate_blog_topics':
        interests = arguments.get('interests', [])
        past_topics = arguments.get('past_topics', [])
        count = arguments.get('count', 5)

        prompt = f"""Generate {count} engaging blog post topic ideas for someone interested in: {', '.join(interests)}.

They've previously written about: {', '.join(past_topics) if past_topics else 'nothing yet'}.

Requirements:
- Each topic should be specific and actionable
- Topics should be relevant to the interests
- Avoid duplicating past topics
- Make them engaging and clickable

Return ONLY a JSON array of topic strings, like: ["Topic 1", "Topic 2", ...]
No other text, no explanations, just the JSON array."""

        result = generate_with_ollama(prompt, model)

        if result['success']:
            try:
                import json
                import re

                content = result['content'].strip()

                # Try to extract JSON array from response
                # Some models wrap it in markdown code blocks
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    topics = json.loads(json_match.group())
                else:
                    # Fallback: split by newlines and clean up
                    topics = [
                        line.strip().strip('"-•*123456789.').strip()
                        for line in content.split('\n')
                        if line.strip() and not line.strip().startswith('[')
                    ]
                    topics = [t for t in topics if len(t) > 10][:count]

                return jsonify({
                    'topics': topics[:count],
                    'model': result['model'],
                    'tokens': result['tokens']
                })
            except Exception as e:
                # If parsing fails, return raw output split by lines
                topics = [
                    line.strip()
                    for line in result['content'].split('\n')
                    if line.strip()
                ][:count]
                return jsonify({
                    'topics': topics,
                    'model': result['model'],
                    'tokens': result['tokens'],
                    'note': 'Parsed from raw output'
                })
        else:
            return jsonify({'error': result['error']}), 500

    elif tool_name == 'generate_blog_outline':
        topic = arguments.get('topic')
        audience = arguments.get('audience', 'general')
        length = arguments.get('length', 'medium')

        prompt = f"""Create a detailed blog post outline for the topic: "{topic}"

Target audience: {audience}
Desired length: {length}

Return a JSON object with this exact structure:
{{
  "introduction": "Brief intro description",
  "main_points": ["Point 1", "Point 2", "Point 3", "Point 4"],
  "conclusion": "Conclusion description"
}}

No other text, just the JSON object."""

        result = generate_with_ollama(prompt, model)

        if result['success']:
            try:
                import json
                import re

                content = result['content'].strip()

                # Try to extract JSON object
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    outline = json.loads(json_match.group())
                else:
                    # Fallback outline
                    outline = {
                        "introduction": f"Introduction to {topic}",
                        "main_points": [
                            "Background and overview",
                            "Key concepts and principles",
                            "Practical examples",
                            "Best practices"
                        ],
                        "conclusion": "Summary and next steps"
                    }

                return jsonify({
                    'outline': outline,
                    'model': result['model'],
                    'tokens': result['tokens']
                })
            except:
                # Return structured fallback
                return jsonify({
                    'outline': {
                        "introduction": f"Introduction to {topic}",
                        "main_points": [
                            "Overview and context",
                            "Core concepts",
                            "Practical application",
                            "Conclusion"
                        ],
                        "conclusion": "Summary and takeaways"
                    },
                    'model': result['model'],
                    'tokens': result['tokens'],
                    'note': 'Fallback outline due to parsing error'
                })
        else:
            return jsonify({'error': result['error']}), 500

    else:
        return jsonify({'error': f'Unknown tool: {tool_name}'}), 400

@app.route('/moderate', methods=['POST'])
def moderate():
    """Moderate content using local model"""

    data = request.json
    text = data.get('text', '')
    context = data.get('context', 'general')
    model = data.get('model', DEFAULT_MODEL)

    if not text:
        return jsonify({'error': 'Text required'}), 400

    ai_calls.labels(tool='moderate', model=model).inc()

    prompt = f"""Analyze this {context} content for policy violations.

Content: "{text}"

Check for:
- Spam or promotional content
- Hate speech or harassment
- Explicit or adult content
- Misinformation
- Personal information

Respond with JSON only:
{{
  "safe": true or false,
  "confidence": 0.0-1.0,
  "violations": ["type1", "type2"] or [],
  "reason": "brief explanation"
}}

No other text."""

    result = generate_with_ollama(prompt, model)

    if result['success']:
        try:
            import json
            import re

            content = result['content'].strip()

            # Try to extract JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                moderation_result = json.loads(json_match.group())
            else:
                # Fallback: safe by default for local models
                # (better to be permissive than overly strict)
                moderation_result = {
                    "safe": True,
                    "confidence": 0.5,
                    "violations": [],
                    "reason": "Local model - default safe"
                }

            return jsonify({
                'safe': moderation_result.get('safe', True),
                'confidence': moderation_result.get('confidence', 0.5),
                'violations': moderation_result.get('violations', []),
                'reason': moderation_result.get('reason', ''),
                'source': 'local-ai',
                'model': result['model']
            })
        except:
            # Fail safe
            return jsonify({
                'safe': True,  # Default to safe for local models
                'confidence': 0.3,
                'violations': [],
                'reason': 'Local moderation - parsing error',
                'source': 'local-ai'
            })
    else:
        # If AI fails, default to safe (permissive)
        return jsonify({
            'safe': True,
            'confidence': 0.0,
            'reason': f'Local AI error: {result["error"]}',
            'source': 'error'
        })

@app.route('/models')
def list_models():
    """List available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get('models', [])

        return jsonify({
            'models': [
                {
                    'name': m['name'],
                    'size': m.get('size', 0),
                    'modified': m.get('modified_at', '')
                }
                for m in models
            ],
            'default': DEFAULT_MODEL
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Local AI Server (Ollama) Starting")
    print("="*60)
    print(f"Ollama Host: {OLLAMA_HOST}")
    print(f"Default Model: {DEFAULT_MODEL}")
    print("")
    print("Make sure Ollama is running:")
    print("  brew install ollama  # or download from ollama.ai")
    print("  ollama serve")
    print("  ollama pull llama3.2  # or llama2, mistral, phi, etc.")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=8081, debug=False)
