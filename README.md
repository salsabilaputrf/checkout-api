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

## 2️⃣ Struktur Folder
checkout-api/
│
├─ checkout_api/ # Django project settings
│ ├─ settings.py
│ ├─ urls.py
│ └─ wsgi.py
│
├─ products/ # App untuk produk
│ ├─ models.py
│ ├─ views.py
│ ├─ serializers.py
│ ├─ tests.py
│ └─ management/ # Seeder
│ └─ commands/
│ └─ seed_products.py
│
├─ orders/ # App untuk order & Midtrans
│ ├─ models.py
│ ├─ views.py
│ ├─ serializers.py
│ └─ tests.py
│
├─ payments/ # App untuk webhook & integrasi Midtrans
│ ├─ views.py
│
├─ requirements.txt
├─ manage.py
└─ .env # environment variables

---

## 3️⃣ Requirement

- Python 3.10+
- Django 4+
- Django REST Framework
- PostgreSQL (boleh SQLite lokal)
- Midtrans Sandbox Account
- Ngrok (untuk testing webhook di localhost)

---

## 4️⃣ Setup Project

### 4.1 Clone repository
```bash
git clone <YOUR_REPO_URL>
cd checkout-api

### 4.2 Buat Virtual Environment
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux / macOS

### 4.3 Install Dependencies

Setelah virtual environment aktif, install semua dependency project:

```bash
pip install -r requirements.txt

## 5️⃣ Setup Database

### 5.1 PostgreSQL
1. Buat database, misal `checkout_db`.

2. Update file `.env` dengan credential:

### 5.2 Migrate Database & Seed Produk

Setelah konfigurasi database di `.env`, jalankan migrate untuk membuat tabel di database:

```bash
python manage.py migrate

Kemudian seed produk awal ke database:
```bash
python manage.py seed_products

## 6️⃣ Jalankan Server
```bash
python manage.py runserver 8000

Endpoint lokal: http://127.0.0.1:8000
Endpoint publik untuk webhook via ngrok:
```bash
ngrok http 8000

Copy URL ngrok → daftarkan di Midtrans Sandbox Webhook URL.

## 7️⃣ Endpoints

| Endpoint                         | Method | Keterangan                       |
|---------------------------------|--------|----------------------------------|
| `/api/products/`                 | GET    | List semua produk                |
| `/api/products/<id>/`            | GET    | Detail produk                    |
| `/api/orders/`                   | POST   | Buat order, multi-item           |
| `/api/orders/midtrans-webhook/` | POST   | Terima webhook Midtrans          |

---

## 8️⃣ Contoh Request

Collection sudah dipublish di **Postman**.

Gunakan environment variable `base_url` sesuai server (lokal/ngrok):

```json
{
  "base_url": "http://127.0.0.1:8000"
}

Jika menggunakan ngrok, ganti base_url menjadi URL publik ngrok.

---

## 9️⃣ Test
```bash
python manage.py test