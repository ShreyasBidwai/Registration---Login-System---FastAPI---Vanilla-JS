# 📝 Student Registration & Login System – FastAPI + Vanilla JS

**Boring work for the developer is validations** — especially after you’ve finished the core functionality.  
Whether backend or frontend, you still have to make sure users don’t send junk data.  
This project is a perfect mix of **core features** + **extensive client-side validations** so the backend isn’t left cleaning up a mess.

---

## 📌 Overview

This is a **student registration and login system** built with:

- **FastAPI** for backend
- **MySQL** database via SQLAlchemy ORM
- **HTML** with **inline CSS and JavaScript** for frontend
- **AJAX (fetch API)** for communicating with the backend without page reload
- **Form validations** both on the frontend (JavaScript) and backend (FastAPI/Pydantic)
- **File uploads** with server-side file type checks

The project covers:
- **Registration** (with country → state → city dynamic loading)
- **Login**
- **File uploads** (JPG, PNG, JPEG, PDF)
- **Validation** for all inputs
- **Session-less redirect flow** after login

---


---

## ⚙️ Backend (FastAPI)

### Features
- `/` → Serves the registration form
- `/submit` → Saves a new user to the database
- `/loginform` → Serves the login page
- `/login` → Validates user credentials
- `/loginSuccess` → Displays welcome page with user details
- `/upload` → Handles file uploads with type restrictions
- `/countries`, `/states/{country_id}`, `/cities/{state_id}` → Dynamic location fetching for dropdowns
- `/seedata` → Lists all registered users (JSON)

### Tech
- **FastAPI** for HTTP handling
- **Pydantic** for request body validation
- **SQLAlchemy ORM** for database operations
- **MySQL** database (configured in `database.py`)
- **Static file handling** for uploads

---

## 🎨 Frontend

### Key Points
- All **CSS is inline** in `<style>` tags within HTML files
- All **JavaScript is inline** in `<script>` tags within HTML files
- No external libraries (pure DOM + Fetch API)

### Registration Page (`index.html`)
- **Validations:**
  - Required fields
  - Email format
  - Mobile number format (starts with 6–9, 10 digits)
  - Password strength (uppercase, lowercase, number, special char, min length 8)
  - Date of birth check (must be year 2007 or earlier)
  - At least one department checkbox selected
  - Gender selection required
  - Dropdowns for course, country, state, city
- **Dynamic location population**:
  - Fetches countries, then states, then cities from backend
- **File upload**:
  - AJAX upload before form submission
  - Server validates file type

### Login Page (`login.html`)
- **Validations**:
  - Email format
  - Password required
- **Login flow**:
  - On success → redirect to `/loginSuccess?rollNum=...&fullname=...`
  - On failure → error message without page reload

### Login Success Page (`loginSuccess.html`)
- Displays:
  - Roll number
  - Full name
- Links:
  - Back to home
  - Logout

---


## 🗄 Database Schema

The database consists of **four main tables**:

1. **countries**
2. **states**
3. **cities**
4. **userData**

The first three are for location hierarchy, while `userData` stores student registration details.

---

### Table Details

#### `countries`
| Column | Type        | Constraints |
|--------|-------------|-------------|
| id     | Integer     | Primary Key |
| name   | String(100) | Not Null    |

#### `states`
| Column     | Type        | Constraints                    |
|------------|-------------|--------------------------------|
| id         | Integer     | Primary Key                    |
| name       | String(100) | Not Null                        |
| country_id | Integer     | Foreign Key → `countries.id`   |

#### `cities`
| Column    | Type        | Constraints                  |
|-----------|-------------|------------------------------|
| id        | Integer     | Primary Key                  |
| name      | String(100) | Not Null                      |
| state_id  | Integer     | Foreign Key → `states.id`    |

#### `userData`
| Column     | Type         | Constraints                         |
|------------|--------------|-------------------------------------|
| rollNum    | Integer      | Primary Key                         |
| fullname   | String(50)   |                                     |
| fatherName | String(50)   |                                     |
| dob        | Date         |                                     |
| mobNum     | String(10)   | Unique                              |
| emailID    | String(50)   | Unique                              |
| password   | String(18)   |                                     |
| gender     | String(10)   |                                     |
| dept       | String(100)  | Stored as comma-separated values    |
| course     | String(50)   |                                     |
| content    | String(255)  | File path                           |
| country    | Integer      | Foreign Key → `countries.id`        |
| state      | Integer      | Foreign Key → `states.id`           |
| city       | Integer      | Foreign Key → `cities.id`           |
| address    | String(500)  |                                     |

---

## 📂 `sql/` Folder

To make setup easier, a **`sql/`** directory is included in the project.  
It contains SQL dump files for **countries**, **states**, and **cities** so you can quickly populate location data:


**Usage** (MySQL example):
```bash
mysql -u your_user -p your_database < sql/countries.sql
mysql -u your_user -p your_database < sql/states.sql
mysql -u your_user -p your_database < sql/cities.sql


## 🛠 Installation & Running

### 1. Clone the repo
```bash
git clone https://github.com/your-username/student-reg-login.git
cd student-reg-login

### 2. Setup virtual env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

4. Configure database
Update your MySQL credentials in database.py:
URL_DATABASE = "mysql+mysqlconnector://fastapi_user:supersecret@localhost/regis_db?charset=utf8mb4"
Create the database:
CREATE DATABASE regis_db;


5. Run server
uvicorn main:app --reload
Open http://127.0.0.1:8000


| Method | Endpoint               | Description                          |
| ------ | ---------------------- | ------------------------------------ |
| GET    | `/`                    | Registration page                    |
| POST   | `/submit`              | Save new user                        |
| GET    | `/loginform`           | Login page                           |
| POST   | `/login`               | User login validation                |
| GET    | `/loginSuccess`        | Post-login welcome page              |
| POST   | `/upload`              | File upload (JPG, PNG, JPEG, PDF)    |
| GET    | `/countries`           | Get list of countries                |
| GET    | `/states/{country_id}` | Get list of states for given country |
| GET    | `/cities/{state_id}`   | Get list of cities for given state   |
| GET    | `/seedata`             | List all registered users (JSON)     |



💡 Pro tip: Next time you think “I’ll skip the validations for now,”
remember that garbage in = garbage out.
Do yourself a favor and catch the garbage early — your backend will thank you.