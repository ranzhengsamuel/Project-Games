"# Week 4 - FastAPI backend goes here" 
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str
    published: bool = False

notes = []

@app.get("/notes")
def get_notes():
    return notes

@app.post("/notes", status_code=201)
def create_note(note: Note):
    notes.append(note)
    return note