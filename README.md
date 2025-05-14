# 📚 Library Management System (Django + JWT + AI)

This is a full-featured **Library Management System** built with **Django**, using **JWT Authentication**, **role-based access control**, **PostgreSQL**, and an integrated **AI-based book recommendation system** powered by **Groq (LLaMA 3)**.

---

## 🚀 Features

* 🔐 JWT-based user authentication (email login)
* 🛡️ Role-based permissions (librarian vs user)
* 📚 Book, Author, Genre management
* 📖 Borrow and return books
* ❌ Prevent borrowing same book twice before returning
* 🧠 AI-generated book recommendations using Groq
* 🔍 Filter available/unavailable book recommendations
* ✅ PostgreSQL database integration

---

## 📂 Project Structure

```
library-management/
├── accounts/           # Custom user model & authentication
├── library/            # Book, Author, Genre, Borrow models & views
├── .env                # Environment variables (GROQ key, DB creds)
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Vansh160205/library-management.git
cd library-management
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file:

```ini
GROQ_API_KEY=your_groq_api_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

---

## 🧪 API Testing with Postman

* Login with JWT: `POST /api/token/`
* Borrow Book: `POST /borrow/` with book ID
* Return Book: `POST /return/<borrow_id>/`
* View AI Recommendations: `GET /recommend/ai/`

Use the JWT access token in headers:

```
Authorization: Bearer <your_token>
```

---

## 🤖 AI Book Recommendations

AI recommendations are generated using **Groq's LLaMA 3** model based on user borrowing history. The system:

1. Sends previously borrowed titles to Groq.
2. Parses the 5 recommended books from the response.
3. Filters available books in the library.
4. Suggests alternatives from the same genre if needed.

---

## 📦 Tech Stack

* **Backend**: Django + Django REST Framework
* **Database**: PostgreSQL
* **Authentication**: JWT (SimpleJWT)
* **AI**: Groq (LLaMA 3 API)

---

## ✨ Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.
