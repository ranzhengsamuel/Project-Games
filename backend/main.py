from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
import redis
import json

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# 连接 Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# endpoint 1: 获取所有笔记（加了缓存）
@app.get("/notes", response_model=list[schemas.NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    # 先查 Redis
    cached = r.get('all_notes')
    if cached:
        return json.loads(cached)  # cache hit ✅

    # Redis 没有，查数据库
    notes = db.query(models.Note).all()
    notes_data = [{"id": n.id, "title": n.title, "content": n.content} for n in notes]

    # 存入 Redis，60秒后过期
    r.setex('all_notes', 60, json.dumps(notes_data))

    return notes_data  # cache miss，但现在已缓存

# endpoint 2: 创建笔记（清除缓存）
@app.post("/notes", response_model=schemas.NoteResponse, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    r.delete('all_notes')  # 数据变了，清除旧缓存
    return db_note

# endpoint 3: 删除笔记（清除缓存）
@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    r.delete('all_notes')  # 数据变了，清除旧缓存