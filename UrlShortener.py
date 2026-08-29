import string
import random
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker,Session

DATABASE_URL = "sqlite:///.urls.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class URLItem(Base):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)



Base.metadata.create_all(bind=engine)



class URLCreate(BaseModel):
    url: HttpUrl



class URLInfo(BaseModel):
    short_code: str
    original_url: str
    clicks: int



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


app = FastAPI(title="URL Shortener API")



@app.post("/shorten", response_model=URLInfo, status_code=status.HTTP_201_CREATED)
def create_short_url(item: URLCreate, db: Session = Depends(get_db)):

    for _ in range(10):
        code = generate_short_code()
        if not db.query(URLItem).filter(URLItem.short_code == code).first():
            break
    else:
        raise HTTPException(status_code=500, detail="Не удалось сгенерировать уникальный код")


    db_item = URLItem(short_code=code, original_url=str(item.url), clicks=0)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_item = db.query(URLItem).filter(URLItem.short_code == short_code).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    db_item.clicks += 1
    db.commit()

    return RedirectResponse(url=db_item.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)