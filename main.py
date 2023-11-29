#main.py

from fastapi import FastAPI
from route import router as route_router

app = FastAPI()

# Include routes from route.py
app.include_router(route_router)
