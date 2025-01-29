from fastapi import FastAPI
from routes import conversation_router

app = FastAPI()


app.include_router(conversation_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8008)
