#!/usr/bin/env python3
"""
Documentation Validation Script

Validates generated documentation for quality and completeness.

Usage:
    python validate_docs.py <docs_directory>

Example:
    python validate_docs.py docs/user_service
"""

import sys
import re
from pathlib import Path
import yaml

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def validate_mermaid(file_path: Path) -> list:
    """Validate Mermaid diagram syntax"""
    errors = []

    try:
        content = file_path.read_text()

        # Check for common Mermaid diagram types
        valid_types = ['graph', 'sequenceDiagram', 'classDiagram', 'stateDiagram', 'erDiagram', 'flowchart']
        has_type = any(diagram_type in content for diagram_type in valid_types)

        if not has_type:
            errors.append(f"No valid diagram type found (expected: {', '.join(valid_types)})")

        # Check for basic syntax issues
        if 'graph' in content:
            # Check for direction
            if not re.search(r'graph\s+(TB|TD|BT|RL|LR)', content):
                errors.append("Graph missing direction (TB, TD, BT, RL, or LR)")

        # Check for empty content
        if len(content.strip()) < 20:
            errors.append("Diagram content seems too short")

        # Check for unclosed brackets
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        if open_brackets != close_brackets:
            errors.append(f"Mismatched brackets: {open_brackets} open, {close_brackets} close")

        # Check for arrows
        if 'graph' in content or 'flowchart' in content:
            if not any(arrow in content for arrow in ['-->', '---', '-.->', '==>']):
                errors.append("No arrows found in diagram")

    except Exception as e:
        errors.append(f"Failed to read file: {e}")

    return errors

def validate_openapi(file_path: Path) -> list:
    """Validate OpenAPI specification"""
    errors = []

    try:
        content = file_path.read_text()
        spec = yaml.safe_load(content)

        # Check required fields
        required_fields = ['openapi', 'info', 'paths']
        for field in required_fields:
            if field not in spec:
                errors.append(f"Missing required field: {field}")

        # Check OpenAPI version
        if 'openapi' in spec:
            version = spec['openapi']
            if not version.startswith('3.'):
                errors.append(f"OpenAPI version should be 3.x, got: {version}")

        # Check info section
        if 'info' in spec:
            info = spec['info']
            if 'title' not in info:
                errors.append("Missing info.title")
            if 'version' not in info:
                errors.append("Missing info.version")

        # Check paths
        if 'paths' in spec:
            if len(spec['paths']) == 0:
                errors.append("No paths defined")
            else:
                # Check each path has methods
                for path, methods in spec['paths'].items():
                    if not isinstance(methods, dict):
                        errors.append(f"Invalid path definition: {path}")
                    elif len(methods) == 0:
                        errors.append(f"Path {path} has no methods")

    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML syntax: {e}")
    except Exception as e:
        errors.append(f"Validation error: {e}")

    return errors

def validate_readme(file_path: Path) -> list:
    """Validate README.md content"""
    errors = []
    warnings = []

    try:
        content = file_path.read_text()

        # Check for required sections (case-insensitive)
        required_sections = ['features', 'setup', 'usage', 'api']
        for section in required_sections:
            if not re.search(f'#{1,3}\\s+{section}', content, re.IGNORECASE):
                warnings.append(f"Recommended section not found: {section}")

        # Check for title
        if not content.startswith('#'):
            errors.append("README should start with a # title")

        # Check minimum length
        if len(content) < 200:
            errors.append("README seems too short (< 200 characters)")

        # Check for code examples
        if '```' not in content:
            warnings.append("No code examples found")

        # Check for architecture diagram
        if 'mermaid' not in content.lower():
            warnings.append("No Mermaid diagram found")

        # Check for broken links (basic check)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        for link_text, link_url in markdown_links:
            if link_url.startswith('http'):
                # External link - we won't validate
                pass
            elif link_url.startswith('#'):
                # Anchor link - should exist in document
                anchor = link_url[1:].lower().replace(' ', '-')
                if anchor not in content.lower():
                    warnings.append(f"Broken anchor link: {link_url}")

    except Exception as e:
        errors.append(f"Failed to read file: {e}")

    return errors, warnings

def validate_directory(docs_dir: Path) -> dict:
    """Validate all documentation in directory"""
    results = {
        'total_files': 0,
        'files_checked': 0,
        'errors': 0,
        'warnings': 0,
        'details': []
    }

    # Check if directory exists
    if not docs_dir.exists():
        print(f"{Colors.RED}✗{Colors.RESET} Directory not found: {docs_dir}")
        return results

    # Get all documentation files
    files_to_check = {
        'mermaid': list(docs_dir.glob('*.mmd')),
        'openapi': list(docs_dir.glob('openapi.yaml')) + list(docs_dir.glob('openapi.yml')),
        'readme': list(docs_dir.glob('README.md'))
    }

    results['total_files'] = sum(len(files) for files in files_to_check.values())

    # Validate each file type
    for mermaid_file in files_to_check['mermaid']:
        results['files_checked'] += 1
        errors = validate_mermaid(mermaid_file)

        if errors:
            results['errors'] += len(errors)
            results['details'].append({
                'file': mermaid_file.name,
                'type': 'error',
                'messages': errors
            })
        else:
            results['details'].append({
                'file': mermaid_file.name,
                'type': 'success',
                'messages': ['Valid Mermaid diagram']
            })

    for openapi_file in files_to_check['openapi']:
        results['files_checked'] += 1
        errors = validate_openapi(openapi_file)

        if errors:
            results['errors'] += len(errors)
            results['details'].append({
                'file': openapi_file.name,
                'type': 'error',
                'messages': errors
            })
        else:
            results['details'].append({
                'file': openapi_file.name,
                'type': 'success',
                'messages': ['Valid OpenAPI specification']
            })

    for readme_file in files_to_check['readme']:
        results['files_checked'] += 1
        errors, warnings = validate_readme(readme_file)

        if errors:
            results['errors'] += len(errors)
            results['details'].append({
                'file': readme_file.name,
                'type': 'error',
                'messages': errors
            })

        if warnings:
            results['warnings'] += len(warnings)
            results['details'].append({
                'file': readme_file.name,
                'type': 'warning',
                'messages': warnings
            })

        if not errors and not warnings:
            results['details'].append({
                'file': readme_file.name,
                'type': 'success',
                'messages': ['Well-structured README']
            })

    return results

def print_results(results: dict):
    """Print validation results"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Documentation Validation Results{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    # Print summary
    print(f"Files checked: {results['files_checked']}/{results['total_files']}")
    print(f"Errors: {results['errors']}")
    print(f"Warnings: {results['warnings']}")
    print()

    # Print details
    for detail in results['details']:
        if detail['type'] == 'success':
            print(f"{Colors.GREEN}✓{Colors.RESET} {detail['file']}")
            for msg in detail['messages']:
                print(f"  {msg}")
        elif detail['type'] == 'warning':
            print(f"{Colors.YELLOW}⚠{Colors.RESET} {detail['file']}")
            for msg in detail['messages']:
                print(f"  {Colors.YELLOW}Warning:{Colors.RESET} {msg}")
        elif detail['type'] == 'error':
            print(f"{Colors.RED}✗{Colors.RESET} {detail['file']}")
            for msg in detail['messages']:
                print(f"  {Colors.RED}Error:{Colors.RESET} {msg}")
        print()

    # Print final verdict
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    if results['errors'] == 0:
        if results['warnings'] == 0:
            print(f"{Colors.GREEN}✓ All documentation is valid!{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}✓ Documentation is valid with {results['warnings']} warning(s){Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}✗ Documentation has {results['errors']} error(s){Colors.RESET}")
        return 1

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python validate_docs.py <docs_directory>")
        print("Example: python validate_docs.py docs/user_service")
        sys.exit(1)

    docs_dir = Path(sys.argv[1])

    print(f"\n🔍 Validating documentation in: {docs_dir}\n")

    results = validate_directory(docs_dir)
    exit_code = print_results(results)

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
