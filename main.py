from fastapi import FastAPI
import uvicorn

from routes import router


app = FastAPI(title='STREAMING SERVICES API', version='1.0',
              description='Queries for movies and series across multiple streaming services')

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
