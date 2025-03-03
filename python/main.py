import os
import logging
import pathlib
import json
from fastapi import FastAPI, Form, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel
from contextlib import asynccontextmanager
import hashlib


# Define the path to the images & sqlite3 database
images = pathlib.Path(__file__).parent.resolve() / "images"
db = pathlib.Path(__file__).parent.resolve() / "db" / "mercari.sqlite3"


def get_db():
    if not db.exists():
        yield

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
    finally:
        conn.close()


# STEP 5-1: set up the database connection
def setup_database():
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    yield


app = FastAPI(lifespan=lifespan)

logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class HelloResponse(BaseModel):
    message: str


@app.get("/", response_model=HelloResponse)
def hello():
    return HelloResponse(**{"message": "Hello, world!"})


class AddItemResponse(BaseModel):
    message: str


# add_item is a handler to add a new item for POST /items .
@app.post("/items", response_model=AddItemResponse)
def add_item(
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: sqlite3.Connection = Depends(get_db),
):
    file_data = image.file.read()
    # Calculate the SHA-256 hash of the file
    hashed_value = hashlib.sha256(file_data).hexdigest()
    
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    insert_item(Item(name=name, category=category, image=hashed_value))
    return AddItemResponse(**{"message": f"item received: {name}"})

# get_item is a handler to get all items for GET /items .
@app.get("/items")
async def get_items():
    path_to_jsonfile = 'items.json'
    try:    
        with open(path_to_jsonfile, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
        pass
    return data 

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    path_to_jsonfile = 'items.json'
    try:
        with open(path_to_jsonfile, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
        pass
    return data['items'][item_id-1]

# get_image is a handler to return an image for GET /images/{filename} .
@app.get("/image/{image_name}")
async def get_image(image_name):
    # Create image path
    image = images / image_name

    if not image_name.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)


class Item(BaseModel):
    name: str
    category: str 
    image: str  


def insert_item(item: Item):
    # STEP 4-1: add an implementation to store an item
    try:
        # 既存のJSONデータを読み込む
        path_to_jsonfile = 'items.json'
        with open(path_to_jsonfile, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {'items': []} 
        pass

    # データに新たなitemを追加
    if not any(existing_item == item.dict() for existing_item in data):
        data['items'].append(item.dict())
        print('item added')

    # データをjsonファイルに書き込む
    with open(path_to_jsonfile, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
