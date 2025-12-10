# PPD Backend API

Backend API untuk Penambangan Data menggunakan FastAPI dengan fitur autentikasi dan machine learning.

## 🚀 Instalasi

```bash
# Clone repository
git clone https://github.com/WahyuAgg/ppd_be.git
cd ppd_be

# Install dependencies
pip install -r app/requirements.txt

# Jalankan server
python -m uvicorn app.main:app --reload
```

Server akan berjalan di `http://127.0.0.1:8000`

## 📚 API Documentation

Buka `http://127.0.0.1:8000/docs` untuk Swagger UI interaktif.

## 🔐 Authentication Endpoints

### Register
```
POST /auth/register
Content-Type: application/json

{
    "username": "namauser",
    "password": "passwordmu"
}
```

### Login (JSON)
```
POST /auth/login-json
Content-Type: application/json

{
    "username": "namauser",
    "password": "passwordmu"
}
```

### Login (Form)
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=namauser&password=passwordmu
```

## 👥 User Endpoints

### Get All Users
```
GET /users/
```

### Get User Count
```
GET /users/count
```

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib

## 📁 Project Structure

```
ppd_be/
├── app/
│   ├── core/           # Config, JWT, Security
│   ├── crud/           # Database operations
│   ├── database/       # Database connection
│   ├── deps/           # Dependencies
│   ├── ml/             # Machine Learning models
│   ├── models/         # SQLAlchemy models
│   ├── routers/        # API routes
│   ├── schemas/        # Pydantic schemas
│   ├── main.py         # Application entry
│   └── requirements.txt
├── model/              # ML model files (.pkl)
└── README.md
```

## 📝 License

MIT License
