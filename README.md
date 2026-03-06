# Checkout API dengan Django & Midtrans Sandbox

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Django](https://img.shields.io/badge/django-4.2+-green)
![DRF](https://img.shields.io/badge/djangorestframework-latest-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 1️⃣ Deskripsi
Sistem checkout sederhana dengan fitur:  

- Produk bisa dibeli (multi-item)  
- Order memvalidasi stok & menghitung total harga  
- Integrasi **Midtrans Sandbox** untuk pembayaran  
- Status order update otomatis via **webhook Midtrans**  
- Duplicate webhook dicegah, aman dengan **signature validation**  

---

## 2️⃣ Requirement

- Python 3.10+
- Django 4+
- Django REST Framework
- PostgreSQL (boleh SQLite lokal)
- Midtrans Sandbox Account
- Ngrok (untuk testing webhook di localhost)

---

## 3️⃣ Setup Project

### 3.1 Clone repository
```bash
git clone <YOUR_REPO_URL>
cd checkout-api
```

### 3.2 Buat Virtual Environment
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux / macOS
```

### 3.3 Install Dependencies

Setelah virtual environment aktif, install semua dependency project:

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Setup Database

### 4.1 PostgreSQL
1. Buat database, misal `checkout_db`.

2. Update file `.env` dengan credential:

### 4.2 Migrate Database & Seed Produk

Setelah konfigurasi database di `.env`, jalankan migrate untuk membuat tabel di database:

```bash
python manage.py migrate
```

Kemudian seed produk awal ke database:
```bash
python manage.py seed_products
```

---

## 5️⃣ Jalankan Server
```bash
python manage.py runserver 8000
```

Endpoint lokal: http://127.0.0.1:8000
Endpoint publik untuk webhook via ngrok:
```bash
ngrok http 8000
```

Copy URL ngrok → daftarkan di Midtrans Sandbox Webhook URL.

---

## 6️⃣ Endpoints

| Endpoint                         | Method | Keterangan                       |
|---------------------------------|--------|----------------------------------|
| `/api/products/`                 | GET    | List semua produk                |
| `/api/products/<id>/`            | GET    | Detail produk                    |
| `/api/orders/`                   | POST   | Buat order, multi-item           |
| `/api/orders/midtrans-webhook/` | POST   | Terima webhook Midtrans          |

---

## 7️⃣ Contoh Request

Collection sudah dipublish di **Postman**.

Gunakan environment variable `base_url` sesuai server (lokal/ngrok):

```json
{
  "base_url": "http://127.0.0.1:8000"
}
```
Jika menggunakan ngrok, ganti base_url menjadi URL publik ngrok.

---

## 8️⃣ Test
```bash
python manage.py test
```