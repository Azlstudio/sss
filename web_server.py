#!/usr/bin/env python3
"""
LocalAI Assistant - Web Server
Modern ChatGPT-style interface
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from assistant import LocalAIAssistant
import json
import threading

app = Flask(__name__, template_folder='web/public', static_folder='web/public/static')
CORS(app)

# Initialize assistant
assistant = LocalAIAssistant()
current_domain = "general"

@app.route('/')
def index():
    """Serve the main interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    global current_domain

    data = request.json
    query = data.get('query', '')
    domain = data.get('domain', current_domain)

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        result = assistant.chat(query, domain=domain, verbose=False)
        current_domain = result['domain']

        return jsonify({
            'response': result['response'],
            'domain': result['domain'],
            'facts_learned': result['facts_learned'],
            'thinking': result.get('thinking', '')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/domain', methods=['GET', 'POST'])
def set_domain():
    """Get or set current domain"""
    global current_domain

    if request.method == 'GET':
        return jsonify({'domain': current_domain})

    data = request.json
    domain = data.get('domain', 'general')

    domains = assistant.specialization.get_available_domains()
    if domain in domains:
        current_domain = domain
        return jsonify({'domain': domain, 'success': True})
    else:
        return jsonify({'error': f'Unknown domain. Available: {domains}'}), 400

@app.route('/api/domains', methods=['GET'])
def get_domains():
    """Get available domains"""
    domains = assistant.specialization.get_available_domains()
    return jsonify({'domains': domains})

@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Get memory statistics"""
    stats = assistant.memory_status()
    return jsonify(stats)

@app.route('/api/learn', methods=['POST'])
def learn():
    """Learn from a file"""
    data = request.json
    filepath = data.get('filepath', '')

    if not filepath:
        return jsonify({'error': 'No filepath provided'}), 400

    try:
        result = assistant.learn_from_file(filepath)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project', methods=['POST'])
def learn_project():
    """Learn from a project"""
    data = request.json
    project_path = data.get('path', '')
    name = data.get('name')

    if not project_path:
        return jsonify({'error': 'No path provided'}), 400

    try:
        result = assistant.learn_from_project(project_path, name)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preferences', methods=['GET', 'POST'])
def preferences():
    """Get or set preferences"""
    if request.method == 'GET':
        key = request.args.get('key')
        if key:
            value = assistant.get_preference(key)
            return jsonify({'key': key, 'value': value})
        return jsonify({'message': 'Provide key parameter'})

    data = request.json
    key = data.get('key')
    value = data.get('value')

    if key and value:
        assistant.remember_preference(key, value)
        return jsonify({'success': True, 'key': key, 'value': value})

    return jsonify({'error': 'Missing key or value'}), 400

@app.route('/api/export', methods=['POST'])
def export_memory():
    """Export memory"""
    data = request.json
    output_dir = data.get('path', './memory_export')

    try:
        assistant.export_memory(output_dir)
        return jsonify({'success': True, 'path': output_dir})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 LocalAI Assistant - Web Server")
    print("="*70)
    print("Starting on: http://localhost:5000")
    print("API Documentation: http://localhost:5000/api/docs")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
