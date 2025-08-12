from fastapi import Body
from fastapi import FastAPI, Depends, Request, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
from datetime import date
from app import models
from app.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from .models import User
from fastapi.encoders import jsonable_encoder
from .models import Country, State, City
from typing import List
import os
from fastapi.responses import JSONResponse
from fastapi import Body
from fastapi.responses import RedirectResponse



app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../static/uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)



@app.post("/upload")
async def upload_content(content: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if content.content_type not in allowed_types:
        return JSONResponse(status_code=400, content={"detail": "Invalid file type."})
    file_ext = os.path.splitext(content.filename)[1]
    save_path = os.path.join(UPLOAD_DIR, content.filename)
    base, ext = os.path.splitext(content.filename)
    i = 1
    while os.path.exists(save_path):
        save_path = os.path.join(UPLOAD_DIR, f"{base}_{i}{ext}")
        i += 1
    with open(save_path, "wb") as f:
        f.write(await content.read())
    rel_path = os.path.relpath(save_path, os.path.dirname(__file__))
    return {"path": rel_path}

class UserBase(BaseModel):
    rollNum: int
    fullname: str
    fatherName: str
    dob: date
    mobNum: str
    emailID: str
    password: str
    gender: str
    dept: List[str]
    course: str
    country: int
    state: int
    city: int
    address: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/seedata")
def show_data(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return jsonable_encoder(all_users)

@app.get("/loginform", response_class=HTMLResponse)
def login_form(request: Request):
    print("Rendering login.html")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(payload: dict = Body(...), db: Session = Depends(get_db)):
    emailID = payload.get("emailID")
    password = payload.get("password")
    user = db.query(User).filter(User.emailID == emailID).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"success": True, "rollNum": user.rollNum, "fullname": user.fullname}

@app.get("/logout")
def logout(request: Request):
    return RedirectResponse(url="/loginform")
    
@app.get("/loginSuccess", response_class=HTMLResponse)
def login_success(request: Request, rollNum: int, fullname: str):
    return templates.TemplateResponse("loginSuccess.html", {"request": request, "rollNum": rollNum, "fullname": fullname})

@app.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    return [{"id": c.id, "name": c.name} for c in countries]

@app.get("/states/{country_id}")
def get_states(country_id: int, db: Session = Depends(get_db)):
    states = db.query(State).filter(State.country_id == country_id).all()
    return [{"id": s.id, "name": s.name} for s in states]

@app.get("/cities/{state_id}")
def get_cities(state_id: int, db: Session = Depends(get_db)):
    cities = db.query(City).filter(City.state_id == state_id).all()
    return [{"id": c.id, "name": c.name} for c in cities]

@app.post("/submit")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    try:
        user_data = user.model_dump()
        if isinstance(user_data["dept"], list):
            user_data["dept"] = ",".join(user_data["dept"])
        print("User data being saved:", user_data)
        new_user = models.User(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": "User successfully created",
            "rollNum": new_user.rollNum
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")
