#!/usr/bin/env python3
"""
Documentation Generation Script

Automatically generate documentation from code using AI.

Usage:
    python generate_docs.py <code_file.py>

Example:
    python generate_docs.py examples/user_service.py

Requirements:
    - AI server running (Ollama or cloud)
    - AI_SERVER_URL environment variable (defaults to http://localhost:8081)
"""

import requests
import json
import sys
import os
from pathlib import Path

# Configuration
AI_SERVER_URL = os.getenv('AI_SERVER_URL', 'http://localhost:8081')
OUTPUT_DIR = Path('docs')

def call_ai(prompt: str, model: str = None) -> dict:
    """Call AI server to generate content"""
    try:
        payload = {
            'tool_name': 'generate_content',
            'arguments': {
                'prompt': prompt
            }
        }

        if model:
            payload['model'] = model

        response = requests.post(
            f"{AI_SERVER_URL}/call_tool",
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        if not result.get('success'):
            raise Exception(f"AI call failed: {result.get('error', 'Unknown error')}")

        return result

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to AI server at {AI_SERVER_URL}")
        print(f"   Error: {e}")
        print(f"\n💡 Make sure AI server is running:")
        print(f"   - Ollama: cd ai-servers/local-ai && python ollama_server.py")
        print(f"   - Cloud: cd ai-servers/content-ai && python server.py")
        sys.exit(1)

def read_code_file(file_path: str) -> str:
    """Read code file contents"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

def extract_mermaid(content: str) -> str:
    """Extract Mermaid code from AI response"""
    # Look for ```mermaid ... ``` blocks
    if '```mermaid' in content:
        start = content.find('```mermaid') + len('```mermaid')
        end = content.find('```', start)
        return content[start:end].strip()

    # If no code block, assume the entire content is Mermaid
    return content.strip()

def extract_yaml(content: str) -> str:
    """Extract YAML from AI response"""
    # Look for ```yaml ... ``` blocks
    if '```yaml' in content:
        start = content.find('```yaml') + len('```yaml')
        end = content.find('```', start)
        return content[start:end].strip()

    # If no code block, assume the entire content is YAML
    return content.strip()

def extract_markdown(content: str) -> str:
    """Extract markdown from AI response"""
    # Look for ```markdown ... ``` blocks
    if '```markdown' in content:
        start = content.find('```markdown') + len('```markdown')
        end = content.find('```', start)
        return content[start:end].strip()

    # If no code block, assume the entire content is markdown
    return content.strip()

def generate_architecture_diagram(code: str, service_name: str) -> str:
    """Generate Mermaid architecture diagram from code"""
    print("  Generating architecture diagram...")

    prompt = f"""Analyze this {service_name} code and generate a Mermaid architecture diagram.

Show:
- External dependencies (databases, caches, APIs)
- Main components and their relationships
- Data flow between components
- API endpoints grouped by functionality

Code:
```python
{code}
```

Return ONLY the Mermaid diagram code (use graph TB layout), no explanations or markdown formatting."""

    result = call_ai(prompt)
    content = result.get('content', '')

    # Extract Mermaid code
    mermaid_code = extract_mermaid(content)

    return mermaid_code

def generate_sequence_diagram(code: str, service_name: str, flow_name: str) -> str:
    """Generate Mermaid sequence diagram for a specific flow"""
    print(f"  Generating sequence diagram for {flow_name}...")

    prompt = f"""Analyze this {service_name} code and generate a Mermaid sequence diagram for the {flow_name} flow.

Show:
- Step-by-step interaction between components
- Database queries
- Cache operations
- Success and error paths

Code:
```python
{code}
```

Return ONLY the Mermaid sequence diagram code, no explanations or markdown formatting."""

    result = call_ai(prompt)
    content = result.get('content', '')

    return extract_mermaid(content)

def generate_openapi_spec(code: str, service_name: str) -> str:
    """Generate OpenAPI specification from code"""
    print("  Generating OpenAPI specification...")

    prompt = f"""Analyze this {service_name} Flask service and generate an OpenAPI 3.0 specification.

Include:
- All endpoints with methods
- Request/response schemas
- Authentication requirements
- Error responses
- Example values

Code:
```python
{code}
```

Return ONLY valid YAML for OpenAPI 3.0 specification, no explanations."""

    result = call_ai(prompt)
    content = result.get('content', '')

    return extract_yaml(content)

def generate_readme(code: str, service_name: str, architecture_diagram: str) -> str:
    """Generate README.md from code"""
    print("  Generating README...")

    prompt = f"""Generate a comprehensive README.md for this {service_name}.

Include:
1. Brief description
2. Features (bullet list)
3. Architecture section with the Mermaid diagram below
4. API Endpoints (table format)
5. Setup instructions
6. Usage examples with curl commands
7. Environment variables
8. Dependencies

Architecture diagram to include:
```mermaid
{architecture_diagram}
```

Code to document:
```python
{code}
```

Return ONLY the markdown content, starting with # {service_name}"""

    result = call_ai(prompt)
    content = result.get('content', '')

    return extract_markdown(content)

def save_documentation(service_name: str, docs: dict):
    """Save generated documentation to files"""
    # Create output directory
    service_dir = OUTPUT_DIR / service_name
    service_dir.mkdir(parents=True, exist_ok=True)

    # Save each document
    for filename, content in docs.items():
        file_path = service_dir / filename

        with open(file_path, 'w') as f:
            f.write(content)

        print(f"   ✅ {file_path}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python generate_docs.py <code_file.py>")
        print("Example: python generate_docs.py examples/user_service.py")
        sys.exit(1)

    code_file = sys.argv[1]
    service_name = Path(code_file).stem  # e.g., "user_service" from "user_service.py"

    print(f"\n📚 Generating documentation for {service_name}...")
    print(f"Using AI server: {AI_SERVER_URL}\n")

    # Read code
    code = read_code_file(code_file)

    # Generate documentation
    docs = {}

    # 1. Architecture diagram
    architecture = generate_architecture_diagram(code, service_name)
    docs['architecture.mmd'] = architecture

    # 2. Sequence diagrams
    registration_seq = generate_sequence_diagram(code, service_name, "user registration")
    docs['sequence-registration.mmd'] = registration_seq

    login_seq = generate_sequence_diagram(code, service_name, "user login")
    docs['sequence-login.mmd'] = login_seq

    # 3. OpenAPI spec
    openapi = generate_openapi_spec(code, service_name)
    docs['openapi.yaml'] = openapi

    # 4. README
    readme = generate_readme(code, service_name, architecture)
    docs['README.md'] = readme

    # Save all documentation
    print("\n💾 Saving documentation...")
    save_documentation(service_name, docs)

    print(f"\n✅ Documentation generated in {OUTPUT_DIR / service_name}/")
    print("\nGenerated files:")
    print("   - README.md (service documentation)")
    print("   - architecture.mmd (architecture diagram)")
    print("   - sequence-*.mmd (sequence diagrams)")
    print("   - openapi.yaml (API specification)")
    print("\n💡 View Mermaid diagrams:")
    print("   - GitHub/GitLab (renders automatically)")
    print("   - VS Code (with Mermaid extension)")
    print("   - https://mermaid.live")
    print("\n🚀 Next steps:")
    print(f"   1. Review generated docs: cat {OUTPUT_DIR / service_name}/README.md")
    print(f"   2. Customize as needed")
    print(f"   3. Commit to repository")

if __name__ == '__main__':
    main()
