from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import crud
from database import SessionLocal, engine
from models import schemas, models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root(user_agent: str = Header(None)):
    return {'User-Agent': user_agent}


@app.get('/{short_url}')
async def get_url(short_url: str, no_redirect: bool = False, db: Session = Depends(get_db)):
    db_url = crud.get_url(db, short_url)
    if not db_url:
        raise HTTPException(status_code=404, detail='This short url does not exist')
    return db_url if no_redirect else RedirectResponse(db_url.long_url)


@app.post('/shorten', response_model=schemas.Url)
async def create_url(url: schemas.Url, db: Session = Depends(get_db)):
    return crud.create_url(db, url)
