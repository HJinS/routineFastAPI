from fastapi import FastAPI
from user.routes import user_app


app = FastAPI()

app.mount('/users/v1', user_app)
