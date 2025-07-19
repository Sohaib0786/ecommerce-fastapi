from fastapi import FastAPI
from routes import product_routes, order_routes

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI E-Commerce Backend is running 🎉"}

app.include_router(product_routes.router)
app.include_router(order_routes.router)
