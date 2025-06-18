#!/usr/bin/env python3
"""
Test script untuk MAC dan HMAC implementations
Menguji berbagai skenario dan edge cases
"""

import hashlib
import hmac
import secrets
import time
from app import MACImplementation, HMACImplementation, CryptoAnalyzer

def test_mac_implementations():
    """Test semua implementasi MAC"""
    print("=" * 60)
    print("TESTING MAC & HMAC IMPLEMENTATIONS")
    print("=" * 60)
    
    # Test data
    test_cases = [
        {
            "message": "Hello, World!",
            "key": "secret_key_123",
            "description": "Basic test case"
        },
        {
            "message": "",
            "key": "empty_message_key",
            "description": "Empty message test"
        },
        {
            "message": "A" * 1000,
            "key": "long_message_key",
            "description": "Long message test"
        },
        {
            "message": "Unicode test: 你好世界 🌍",
            "key": "unicode_key_测试",
            "description": "Unicode test"
        }
    ]
    
    mac_impl = MACImplementation()
    hmac_impl = HMACImplementation()
    analyzer = CryptoAnalyzer()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print("-" * 40)
        print(f"Message: {test_case['message'][:50]}{'...' if len(test_case['message']) > 50 else ''}")
        print(f"Key: {test_case['key']}")
        
        # Test dengan SHA-256
        hash_func = hashlib.sha256
        
        # Simple MAC
        simple_mac = mac_impl.simple_mac(test_case['message'], test_case['key'], hash_func)
        print(f"Simple MAC (SHA-256): {simple_mac}")
        
        # Improved MAC
        improved_mac = mac_impl.improved_mac(test_case['message'], test_case['key'], hash_func)
        print(f"Improved MAC (SHA-256): {improved_mac}")
        
        # Custom HMAC
        custom_hmac = hmac_impl.custom_hmac(test_case['message'], test_case['key'], hash_func)
        print(f"Custom HMAC (SHA-256): {custom_hmac}")
        
        # Built-in HMAC
        builtin_hmac = hmac.new(
            test_case['key'].encode(), 
            test_case['message'].encode(), 
            hash_func
        ).hexdigest()
        print(f"Built-in HMAC (SHA-256): {builtin_hmac}")
        
        # Verify custom HMAC matches built-in
        hmac_match = custom_hmac == builtin_hmac
        print(f"HMAC Implementation Match: {'✓ PASS' if hmac_match else '✗ FAIL'}")

def test_verification():
    """Test verifikasi MAC"""
    print("\n" + "=" * 60)
    print("TESTING MAC VERIFICATION")
    print("=" * 60)
    
    analyzer = CryptoAnalyzer()
    
    # Test case untuk verifikasi
    message = "Test message for verification"
    key = "verification_key"
    
    # Generate MAC
    results = analyzer.generate_all_macs(message, key)
    sha256_hmac = results['SHA-256']['builtin_hmac']
    
    print(f"Original Message: {message}")
    print(f"Key: {key}")
    print(f"Generated HMAC: {sha256_hmac}")
    
    # Test valid verification
    is_valid, calculated = analyzer.verify_mac(
        message, key, sha256_hmac, 'builtin_hmac', 'SHA-256'
    )
    print(f"\nValid Verification: {'✓ PASS' if is_valid else '✗ FAIL'}")
    
    # Test invalid verification (wrong message)
    is_valid, calculated = analyzer.verify_mac(
        "Wrong message", key, sha256_hmac, 'builtin_hmac', 'SHA-256'
    )
    print(f"Invalid Message Test: {'✓ PASS' if not is_valid else '✗ FAIL'}")
    
    # Test invalid verification (wrong key)
    is_valid, calculated = analyzer.verify_mac(
        message, "wrong_key", sha256_hmac, 'builtin_hmac', 'SHA-256'
    )
    print(f"Invalid Key Test: {'✓ PASS' if not is_valid else '✗ FAIL'}")
    
    # Test invalid verification (wrong MAC)
    wrong_mac = "0" * 64  # Wrong MAC value
    is_valid, calculated = analyzer.verify_mac(
        message, key, wrong_mac, 'builtin_hmac', 'SHA-256'
    )
    print(f"Invalid MAC Test: {'✓ PASS' if not is_valid else '✗ FAIL'}")

def test_performance():
    """Test performa berbagai algoritma"""
    print("\n" + "=" * 60)
    print("PERFORMANCE TESTING")
    print("=" * 60)
    
    # Test data
    message = "Performance test message " * 100  # ~2.7KB message
    key = "performance_test_key"
    iterations = 1000
    
    algorithms = {
        'MD5': hashlib.md5,
        'SHA-1': hashlib.sha1,
        'SHA-256': hashlib.sha256,
        'SHA-512': hashlib.sha512
    }
    
    print(f"Message size: {len(message)} bytes")
    print(f"Iterations: {iterations}")
    print(f"Key: {key}")
    print()
    
    for alg_name, hash_func in algorithms.items():
        # Test built-in HMAC performance
        start_time = time.time()
        for _ in range(iterations):
            hmac.new(key.encode(), message.encode(), hash_func).hexdigest()
        end_time = time.time()
        
        duration = end_time - start_time
        ops_per_sec = iterations / duration
        
        print(f"{alg_name:>8}: {duration:.4f}s ({ops_per_sec:.0f} ops/sec)")

def test_security_scenarios():
    """Test skenario keamanan"""
    print("\n" + "=" * 60)
    print("SECURITY SCENARIO TESTING")
    print("=" * 60)
    
    analyzer = CryptoAnalyzer()
    
    # Test 1: Key sensitivity
    print("Test 1: Key Sensitivity")
    message = "Sensitive message"
    key1 = "key123"
    key2 = "key124"  # Slightly different key
    
    mac1 = analyzer.generate_all_macs(message, key1)['SHA-256']['builtin_hmac']
    mac2 = analyzer.generate_all_macs(message, key2)['SHA-256']['builtin_hmac']
    
    print(f"Key 1: {key1} -> MAC: {mac1[:16]}...")
    print(f"Key 2: {key2} -> MAC: {mac2[:16]}...")
    print(f"MACs are different: {'✓ PASS' if mac1 != mac2 else '✗ FAIL'}")
    
    # Test 2: Message sensitivity
    print("\nTest 2: Message Sensitivity")
    key = "test_key"
    msg1 = "Hello World"
    msg2 = "Hello World!"  # Added exclamation
    
    mac1 = analyzer.generate_all_macs(msg1, key)['SHA-256']['builtin_hmac']
    mac2 = analyzer.generate_all_macs(msg2, key)['SHA-256']['builtin_hmac']
    
    print(f"Message 1: '{msg1}' -> MAC: {mac1[:16]}...")
    print(f"Message 2: '{msg2}' -> MAC: {mac2[:16]}...")
    print(f"MACs are different: {'✓ PASS' if mac1 != mac2 else '✗ FAIL'}")
    
    # Test 3: Avalanche effect
    print("\nTest 3: Avalanche Effect (bit difference count)")
    mac1_bin = bin(int(mac1, 16))[2:].zfill(256)
    mac2_bin = bin(int(mac2, 16))[2:].zfill(256)
    
    bit_differences = sum(b1 != b2 for b1, b2 in zip(mac1_bin, mac2_bin))
    avalanche_percentage = (bit_differences / 256) * 100
    
    print(f"Bit differences: {bit_differences}/256 ({avalanche_percentage:.1f}%)")
    print(f"Good avalanche effect: {'✓ PASS' if avalanche_percentage > 40 else '✗ FAIL'}")

def main():
    """Main test function"""
    print("MAC & HMAC Implementation Test Suite")
    print("Final Project - Kriptografi")
    print("Testing all implementations and security properties")
    
    try:
        test_mac_implementations()
        test_verification()
        test_performance()
        test_security_scenarios()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
