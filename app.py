from flask import Flask, render_template, request, jsonify, send_file
import hashlib
import hmac
import secrets
import os
import json
from datetime import datetime
import base64

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

class MACImplementation:
    """Custom MAC implementation for educational purposes"""
    
    @staticmethod
    def simple_mac(message, key, hash_func=hashlib.sha256):
        """Simple MAC: MAC = H(key || message)"""
        combined = key.encode() + message.encode()
        return hash_func(combined).hexdigest()
    
    @staticmethod
    def improved_mac(message, key, hash_func=hashlib.sha256):
        """Improved MAC: MAC = H(key || H(message))"""
        message_hash = hash_func(message.encode()).digest()
        combined = key.encode() + message_hash
        return hash_func(combined).hexdigest()

class HMACImplementation:
    """Custom HMAC implementation following RFC 2104"""
    
    @staticmethod
    def custom_hmac(message, key, hash_func=hashlib.sha256):
        """Custom HMAC implementation"""
        block_size = 64  # SHA-256 block size
        
        # If key is longer than block size, hash it
        if len(key) > block_size:
            key = hash_func(key.encode()).digest()
        else:
            key = key.encode()
        
        # Pad key to block size
        if len(key) < block_size:
            key = key + b'\x00' * (block_size - len(key))
        
        # Create inner and outer padding
        ipad = bytes([0x36] * block_size)
        opad = bytes([0x5C] * block_size)
        
        # XOR key with padding
        inner_key = bytes([k ^ i for k, i in zip(key, ipad)])
        outer_key = bytes([k ^ o for k, o in zip(key, opad)])
        
        # Calculate HMAC
        inner_hash = hash_func(inner_key + message.encode()).digest()
        hmac_result = hash_func(outer_key + inner_hash).hexdigest()
        
        return hmac_result

class CryptoAnalyzer:
    """Analyze and compare different MAC/HMAC implementations"""
    
    def __init__(self):
        self.mac_impl = MACImplementation()
        self.hmac_impl = HMACImplementation()
    
    def generate_all_macs(self, message, key):
        """Generate MACs using different methods and algorithms"""
        results = {}
        
        # Hash algorithms to test
        hash_algorithms = {
            'MD5': hashlib.md5,
            'SHA-1': hashlib.sha1,
            'SHA-256': hashlib.sha256,
            'SHA-512': hashlib.sha512
        }
        
        for alg_name, hash_func in hash_algorithms.items():
            results[alg_name] = {
                'simple_mac': self.mac_impl.simple_mac(message, key, hash_func),
                'improved_mac': self.mac_impl.improved_mac(message, key, hash_func),
                'custom_hmac': self.hmac_impl.custom_hmac(message, key, hash_func),
                'builtin_hmac': hmac.new(key.encode(), message.encode(), hash_func).hexdigest()
            }
        
        return results
    
    def verify_mac(self, message, key, mac_value, mac_type, hash_algorithm):
        """Verify MAC authenticity"""
        hash_func = getattr(hashlib, hash_algorithm.lower().replace('-', ''))
        
        if mac_type == 'simple_mac':
            calculated_mac = self.mac_impl.simple_mac(message, key, hash_func)
        elif mac_type == 'improved_mac':
            calculated_mac = self.mac_impl.improved_mac(message, key, hash_func)
        elif mac_type == 'custom_hmac':
            calculated_mac = self.hmac_impl.custom_hmac(message, key, hash_func)
        elif mac_type == 'builtin_hmac':
            calculated_mac = hmac.new(key.encode(), message.encode(), hash_func).hexdigest()
        else:
            return False, "Unknown MAC type"
        
        is_valid = hmac.compare_digest(calculated_mac, mac_value)
        return is_valid, calculated_mac

# Initialize analyzer
analyzer = CryptoAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_mac', methods=['POST'])
def generate_mac():
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        
        if not message or not key:
            return jsonify({'error': 'Message and key are required'}), 400
        
        # Generate all MAC variants
        results = analyzer.generate_all_macs(message, key)
        
        # Add metadata
        response = {
            'message': message,
            'key': key,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_mac', methods=['POST'])
def verify_mac():
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        mac_value = data.get('mac_value', '')
        mac_type = data.get('mac_type', '')
        hash_algorithm = data.get('hash_algorithm', '')
        
        if not all([message, key, mac_value, mac_type, hash_algorithm]):
            return jsonify({'error': 'All fields are required'}), 400
        
        is_valid, calculated_mac = analyzer.verify_mac(
            message, key, mac_value, mac_type, hash_algorithm
        )
        
        response = {
            'is_valid': is_valid,
            'calculated_mac': calculated_mac,
            'provided_mac': mac_value,
            'message': message,
            'key': key,
            'mac_type': mac_type,
            'hash_algorithm': hash_algorithm,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file_integrity', methods=['POST'])
def file_integrity():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        key = request.form.get('key', '')
        
        if not key:
            return jsonify({'error': 'Key is required'}), 400
        
        # Read file content
        file_content = file.read().decode('utf-8', errors='ignore')
        file.seek(0)  # Reset file pointer
        
        # Generate MAC for file
        results = analyzer.generate_all_macs(file_content, key)
        
        response = {
            'filename': file.filename,
            'file_size': len(file_content),
            'key': key,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare_algorithms')
def compare_algorithms():
    """Compare different hash algorithms performance"""
    test_message = "This is a test message for algorithm comparison"
    test_key = "secret_key_123"
    
    results = analyzer.generate_all_macs(test_message, test_key)
    
    # Add algorithm information
    algorithm_info = {
        'MD5': {
            'output_size': '128 bits (32 hex chars)',
            'security': 'Broken - Not recommended',
            'speed': 'Very Fast'
        },
        'SHA-1': {
            'output_size': '160 bits (40 hex chars)',
            'security': 'Deprecated - Not recommended',
            'speed': 'Fast'
        },
        'SHA-256': {
            'output_size': '256 bits (64 hex chars)',
            'security': 'Secure - Recommended',
            'speed': 'Moderate'
        },
        'SHA-512': {
            'output_size': '512 bits (128 hex chars)',
            'security': 'Very Secure - Recommended',
            'speed': 'Slower'
        }
    }
    
    return jsonify({
        'test_message': test_message,
        'test_key': test_key,
        'results': results,
        'algorithm_info': algorithm_info
    })

@app.route('/educational')
def educational():
    return render_template('educational.html')

@app.route('/file_hash_all_types', methods=['POST'])
def file_hash_all_types():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        key = request.form.get('key', '')
        file_content = file.read()
        file.seek(0)
        if key:
            key_bytes = key.encode()
            data = key_bytes + file_content
        else:
            data = file_content
        hashes = {
            'MD5': hashlib.md5(data).hexdigest(),
            'SHA-1': hashlib.sha1(data).hexdigest(),
            'SHA-256': hashlib.sha256(data).hexdigest(),
            'SHA-512': hashlib.sha512(data).hexdigest(),
        }
        response = {
            'filename': file.filename,
            'file_size': len(file_content),
            'hashes': hashes
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_file_hash_all_types', methods=['POST'])
def verify_file_hash_all_types():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        key = request.form.get('key', '')
        hash_value = request.form.get('hash_value', '')
        algorithm = request.form.get('algorithm', 'SHA-256')
        file_content = file.read()
        file.seek(0)
        if key:
            key_bytes = key.encode()
            data = key_bytes + file_content
        else:
            data = file_content
        hash_func = {
            'MD5': hashlib.md5,
            'SHA-1': hashlib.sha1,
            'SHA-256': hashlib.sha256,
            'SHA-512': hashlib.sha512
        }.get(algorithm, hashlib.sha256)
        calculated_hash = hash_func(data).hexdigest()
        is_valid = (calculated_hash.lower() == hash_value.strip().lower())
        response = {
            'is_valid': is_valid,
            'calculated_hash': calculated_hash,
            'provided_hash': hash_value,
            'algorithm': algorithm,
            'filename': file.filename,
            'file_size': len(file_content)
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

