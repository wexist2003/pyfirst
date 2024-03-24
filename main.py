import time
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from requests import Session
from sqlalchemy import text


from src.database.db import get_db
from src.routes import owners

app = FastAPI()

# один перед всіма
@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['performace'] = str(during)
    return response


templates = Jinja2Templates(directory = 'templates')
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')


@app.get("/", response_class = HTMLResponse, description='Main Page')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Contacts App"})


app.include_router(owners.router, prefix = '/api')

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

