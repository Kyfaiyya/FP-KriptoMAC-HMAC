# MAC & HMAC Cryptography Tool

Final Project untuk mata kuliah **Kriptografi** dengan tema **Message Authentication Code (MAC)** dan **Hash-based Message Authentication Code (HMAC)**.

## 📋 Daftar Anggota Kelompok

| Nama                 | NRP        |
| -------------------- | ---------- |
| Daffa Rajendra P     | 5027231009 |
| Muhamad Arrayyan     | 5027231014 |
| Athalla Barka Fadhil | 5027231018 |
| Naufal Syafi Hakim   | 5027231022 |
| RM. Novian Malcolm B | 5027231035 |
| Muhammad Dzaky Ahnaf | 5027231039 |
| Dzaky Faiq Fayyadhi  | 5027231047 |

## 📋 Deskripsi Project

Aplikasi web interaktif yang mengimplementasikan dan mendemonstrasikan konsep MAC dan HMAC dalam kriptografi. Aplikasi ini menyediakan berbagai fitur untuk memahami, menggunakan, dan membandingkan berbagai implementasi MAC dan HMAC.

## 🎯 Tujuan Pembelajaran

1. **Memahami konsep MAC dan HMAC** dalam konteks keamanan informasi
2. **Mengimplementasikan algoritma** MAC dan HMAC dari scratch
3. **Membandingkan berbagai algoritma hash** (MD5, SHA-1, SHA-256, SHA-512)
4. **Menerapkan praktik keamanan** dalam implementasi kriptografi
5. **Mengembangkan aplikasi web** dengan antarmuka yang user-friendly

## 🚀 Fitur Utama

### 1. Generate MAC

- Implementasi Simple MAC: `MAC = H(key || message)`
- Implementasi Improved MAC: `MAC = H(key || H(message))`
- Implementasi Custom HMAC sesuai RFC 2104
- Built-in HMAC menggunakan library Python
- Support multiple hash algorithms (MD5, SHA-1, SHA-256, SHA-512)

### 2. Verify MAC

- Verifikasi autentisitas pesan menggunakan MAC
- Deteksi perubahan pesan atau key
- Comparison antara calculated MAC vs provided MAC
- Support semua jenis MAC yang diimplementasikan

### 3. File Integrity Checking

- Upload file dan generate MAC untuk file integrity
- Deteksi perubahan pada file
- Support berbagai format file (.txt, .md, .json, .csv)

### 4. Algorithm Comparison

- Perbandingan output dari berbagai algoritma hash
- Informasi keamanan dan performa setiap algoritma
- Visualisasi perbedaan output MAC

### 5. Educational Content

- Penjelasan teori MAC dan HMAC
- Formula dan cara kerja HMAC
- Security considerations dan best practices
- Use cases dalam dunia nyata

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Cryptography**: hashlib, hmac (built-in Python libraries)
- **UI Framework**: Bootstrap 5, Font Awesome icons
- **Testing**: Custom test suite

## 📦 Struktur Project

```
mac-hmac-crypto-tool/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── test_mac_hmac.py      # Test suite
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Main application interface
│   └── educational.html  # Educational content
└── README.md             # Project documentation
```

## 🔧 Instalasi dan Setup

### Prerequisites

- Python 3.8 atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau download project**

   ```bash
   # Jika menggunakan git
   git clone https://github.com/Kyfaiyya/FP-KriptoMAC-HMAC
   cd FP-KriptoMAC-HMAC
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi**

   ```bash
   python app.py
   ```

4. **Akses aplikasi**
   - Buka browser dan kunjungi: `http://localhost:5000`
   - Aplikasi akan berjalan di port 5000

### Menjalankan Test Suite

```bash
python test_mac_hmac.py
```

Test suite akan menjalankan berbagai pengujian:

- Test implementasi MAC dan HMAC
- Test verifikasi MAC
- Performance testing
- Security scenario testing

## 📚 Cara Penggunaan

### 1. Generate MAC

1. Pilih tab "Generate MAC"
2. Masukkan pesan yang ingin di-authenticate
3. Masukkan secret key
4. Klik "Generate MAC"
5. Lihat hasil MAC untuk berbagai algoritma dan metode

### 2. Verify MAC

1. Pilih tab "Verify MAC"
2. Masukkan pesan asli, secret key, dan MAC value
3. Pilih jenis MAC dan algoritma hash
4. Klik "Verify MAC"
5. Lihat hasil verifikasi (VALID/INVALID)

### 3. File Integrity

1. Pilih tab "File Integrity"
2. Upload file yang ingin dicek integritasnya
3. Masukkan secret key
4. Klik "Generate File MAC"
5. Simpan MAC values untuk verifikasi di kemudian hari

### 4. Compare Algorithms

1. Pilih tab "Compare Algorithms"
2. Klik "Load Algorithm Comparison"
3. Lihat perbandingan output dan karakteristik setiap algoritma

## 🔐 Implementasi Kriptografi

### Simple MAC

```python
def simple_mac(message, key, hash_func=hashlib.sha256):
    combined = key.encode() + message.encode()
    return hash_func(combined).hexdigest()
```

### Improved MAC

```python
def improved_mac(message, key, hash_func=hashlib.sha256):
    message_hash = hash_func(message.encode()).digest()
    combined = key.encode() + message_hash
    return hash_func(combined).hexdigest()
```

### Custom HMAC (RFC 2104)

```python
def custom_hmac(message, key, hash_func=hashlib.sha256):
    block_size = 64  # SHA-256 block size

    # Key processing
    if len(key) > block_size:
        key = hash_func(key.encode()).digest()
    else:
        key = key.encode()

    # Padding
    if len(key) < block_size:
        key = key + b'\\x00' * (block_size - len(key))

    # Create paddings
    ipad = bytes([0x36] * block_size)
    opad = bytes([0x5C] * block_size)

    # XOR operations
    inner_key = bytes([k ^ i for k, i in zip(key, ipad)])
    outer_key = bytes([k ^ o for k, o in zip(key, opad)])

    # HMAC calculation
    inner_hash = hash_func(inner_key + message.encode()).digest()
    hmac_result = hash_func(outer_key + inner_hash).hexdigest()

    return hmac_result
```

## 🔍 Aspek Keamanan

### Key Management

- Gunakan key yang cukup panjang (minimal 128 bit)
- Key harus random dan unpredictable
- Jangan hardcode key dalam source code
- Implementasi key rotation

### Algorithm Selection

- **Recommended**: SHA-256, SHA-512
- **Deprecated**: SHA-1 (masih didukung untuk pembelajaran)
- **Broken**: MD5 (hanya untuk demonstrasi)

### Security Properties

- **Authentication**: Verifikasi pengirim pesan
- **Integrity**: Deteksi perubahan pesan
- **Non-repudiation**: Pengirim tidak dapat menyangkal

## 🧪 Testing dan Validasi

Project ini dilengkapi dengan comprehensive test suite yang menguji:

1. **Functional Testing**

   - Semua implementasi MAC dan HMAC
   - Verifikasi dengan berbagai test cases
   - Edge cases (empty message, long message, unicode)

2. **Security Testing**

   - Key sensitivity testing
   - Message sensitivity testing
   - Avalanche effect analysis

3. **Performance Testing**

   - Benchmark berbagai algoritma hash
   - Throughput measurement

4. **Compatibility Testing**
   - Verifikasi custom implementation vs built-in library
   - Cross-algorithm compatibility

## 📊 Hasil Testing

Berdasarkan test suite yang dijalankan:

- ✅ Custom HMAC implementation matches built-in library
- ✅ All MAC variants produce different outputs for different inputs
- ✅ Good avalanche effect (>40% bit difference for small input changes)
- ✅ Performance benchmarks show expected relative speeds
- ✅ Security properties maintained across all implementations

## 🚀 Cara Menjalankan Program

### 1. **Persiapan Environment**

```bash
# Pastikan Python 3.8+ terinstall
python --version

# Install Flask
pip install Flask==2.3.3 Werkzeug==2.3.7
```

## 📸 Dokumentasi Hasil Program
