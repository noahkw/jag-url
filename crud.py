from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import models
from models import schemas
from util import generate_string


def get_url(db: Session, short_url: str):
    return db.query(models.Url).filter(models.Url.short_url == short_url).first()


def create_url(db: Session, url: schemas.Url):
    if not url.short_url:
        url.short_url = generate_string()

    db_url = get_url(db, url.short_url)
    if db_url:
        raise HTTPException(status_code=400, detail='This short url already exists')

    db_url = models.Url(short_url=url.short_url, long_url=url.long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
