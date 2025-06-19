# app.py (VERSI FINAL, BERSIH, DAN KONSISTEN)

from flask import Flask, render_template, request, jsonify
import hashlib
import hmac
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# =====================================================================
# == KELAS-KELAS KRIPTOGRAFI (INTI LOGIKA) ==
# PRINSIP UTAMA: Fungsi di dalam kelas ini selalu bekerja dengan `bytes`.
# =====================================================================

class MACImplementation:
    @staticmethod
    def simple_mac(message_bytes, key_bytes, hash_func):
        """Simple MAC: MAC = H(key || message)"""
        combined = key_bytes + message_bytes
        return hash_func(combined).hexdigest()
    
    @staticmethod
    def improved_mac(message_bytes, key_bytes, hash_func):
        """Improved MAC: MAC = H(key || H(message))"""
        message_hash = hash_func(message_bytes).digest()
        combined = key_bytes + message_hash
        return hash_func(combined).hexdigest()

class HMACImplementation:
    @staticmethod
    def custom_hmac(message_bytes, key_bytes, hash_func):
        """Custom HMAC implementation following RFC 2104"""
        block_size = hash_func().block_size
        
        if len(key_bytes) > block_size:
            key_bytes = hash_func(key_bytes).digest()
        if len(key_bytes) < block_size:
            key_bytes = key_bytes + b'\x00' * (block_size - len(key_bytes))
        
        ipad = bytes([0x36] * block_size)
        opad = bytes([0x5C] * block_size)
        
        inner_key = bytes([k ^ i for k, i in zip(key_bytes, ipad)])
        outer_key = bytes([k ^ o for k, o in zip(key_bytes, opad)])
        
        inner_hash = hash_func(inner_key + message_bytes).digest()
        hmac_result = hash_func(outer_key + inner_hash).hexdigest()
        
        return hmac_result

class CryptoAnalyzer:
    def __init__(self):
        self.mac_impl = MACImplementation()
        self.hmac_impl = HMACImplementation()
    
    def generate_all_macs(self, message_bytes, key):
        """Generate all MAC variants for a given message (in bytes) and key (string)"""
        results = {}
        key_bytes = key.encode()
        hash_algorithms = {
            'MD5': hashlib.md5, 'SHA-1': hashlib.sha1,
            'SHA-256': hashlib.sha256, 'SHA-512': hashlib.sha512
        }
        
        for alg_name, hash_func in hash_algorithms.items():
            results[alg_name] = {
                'simple_mac': self.mac_impl.simple_mac(message_bytes, key_bytes, hash_func),
                'improved_mac': self.mac_impl.improved_mac(message_bytes, key_bytes, hash_func),
                'custom_hmac': self.hmac_impl.custom_hmac(message_bytes, key_bytes, hash_func),
                'builtin_hmac': hmac.new(key_bytes, message_bytes, hash_func).hexdigest()
            }
        return results
    
    def verify_mac(self, message_bytes, key, mac_value, mac_type, hash_algorithm):
        """Verify a MAC for the given bytes."""
        hash_func = getattr(hashlib, hash_algorithm.lower().replace('-', ''))
        key_bytes = key.encode()
        
        calculated_mac = "" # Default value
        if mac_type == 'simple_mac':
            calculated_mac = self.mac_impl.simple_mac(message_bytes, key_bytes, hash_func)
        elif mac_type == 'improved_mac':
            calculated_mac = self.mac_impl.improved_mac(message_bytes, key_bytes, hash_func)
        elif mac_type == 'custom_hmac':
            calculated_mac = self.mac_impl.custom_hmac(message_bytes, key_bytes, hash_func)
        elif mac_type == 'builtin_hmac':
            calculated_mac = hmac.new(key_bytes, message_bytes, hash_func).hexdigest()
        else:
            return False, "Unknown MAC type"
        
        is_valid = hmac.compare_digest(calculated_mac, mac_value)
        return is_valid, calculated_mac

# Initialize analyzer
analyzer = CryptoAnalyzer()

# =====================================================================
# == ROUTE FLASK (Menangani Request & Konversi ke Bytes) ==
# =====================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_mac', methods=['POST'])
def generate_mac():
    try:
        data = request.get_json()
        message_str = data.get('message', '')
        key = data.get('key', '')
        if not message_str or not key:
            return jsonify({'error': 'Message and key are required'}), 400
        
        message_bytes = message_str.encode()
        results = analyzer.generate_all_macs(message_bytes, key)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_mac', methods=['POST'])
def verify_mac():
    try:
        data = request.get_json()
        message_str = data.get('message', '')
        key = data.get('key', '')
        mac_value = data.get('mac_value', '')
        mac_type = data.get('mac_type', '')
        hash_algorithm = data.get('hash_algorithm', '')
        if not all([message_str, key, mac_value, mac_type, hash_algorithm]):
            return jsonify({'error': 'All fields are required'}), 400
        
        message_bytes = message_str.encode()
        is_valid, calculated_mac = analyzer.verify_mac(message_bytes, key, mac_value, mac_type, hash_algorithm)
        return jsonify({
            'is_valid': is_valid, 'calculated_mac': calculated_mac, 'provided_mac': mac_value,
            'mac_type': mac_type, 'hash_algorithm': hash_algorithm
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file_integrity', methods=['POST'])
def file_integrity():
    try:
        if 'file' not in request.files: return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        key = request.form.get('key', '')
        if not key: return jsonify({'error': 'Key is required'}), 400
        
        file_content_bytes = file.read()
        results = analyzer.generate_all_macs(file_content_bytes, key)
        return jsonify({
            'filename': file.filename, 'file_size': len(file_content_bytes), 'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare_algorithms')
def compare_algorithms():
    test_message = "This is a test message for algorithm comparison"
    test_key = "secret_key_123"
    results = analyzer.generate_all_macs(test_message.encode(), key=test_key)
    algorithm_info = {
        'MD5': {'output_size': '128 bits', 'security': 'Broken', 'speed': 'Very Fast'},
        'SHA-1': {'output_size': '160 bits', 'security': 'Deprecated', 'speed': 'Fast'},
        'SHA-256': {'output_size': '256 bits', 'security': 'Secure', 'speed': 'Moderate'},
        'SHA-512': {'output_size': '512 bits', 'security': 'Very Secure', 'speed': 'Slower'}
    }
    return jsonify({
        'test_message': test_message, 'test_key': test_key,
        'results': results, 'algorithm_info': algorithm_info
    })

@app.route('/educational')
def educational():
    return render_template('educational.html')

@app.route('/file_hash_all_types', methods=['POST'])
def file_hash_all_types():
    try:
        if 'file' not in request.files: return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        key = request.form.get('key', '')
        file_content_bytes = file.read()

        data_to_hash = file_content_bytes
        if key:
            data_to_hash = key.encode() + file_content_bytes
        
        hashes = {
            'MD5': hashlib.md5(data_to_hash).hexdigest(),
            'SHA-1': hashlib.sha1(data_to_hash).hexdigest(),
            'SHA-256': hashlib.sha256(data_to_hash).hexdigest(),
            'SHA-512': hashlib.sha512(data_to_hash).hexdigest(),
        }
        return jsonify({'filename': file.filename, 'file_size': len(file_content_bytes), 'hashes': hashes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_file_hash_all_types', methods=['POST'])
def verify_file_hash_all_types():
    try:
        if 'file' not in request.files: return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        hash_value = request.form.get('hash_value', '')
        algorithm = request.form.get('algorithm', 'SHA-256')
        key = request.form.get('key', '')
        if not all([hash_value, algorithm]): return jsonify({'error': 'Hash value and algorithm are required'}), 400
        
        file_content_bytes = file.read()

        data_to_verify = file_content_bytes
        if key:
            data_to_verify = key.encode() + file_content_bytes

        hash_func = getattr(hashlib, algorithm.lower().replace('-', ''))
        calculated_hash = hash_func(data_to_verify).hexdigest()
        is_valid = hmac.compare_digest(calculated_hash.lower(), hash_value.strip().lower())
        
        return jsonify({
            'is_valid': is_valid,
            'calculated_hash': calculated_hash,
            'provided_hash': hash_value,
            'algorithm': algorithm,
            'filename': file.filename,
            'file_size': len(file_content_bytes)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)