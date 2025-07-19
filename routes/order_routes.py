from fastapi import APIRouter
from models.order_model import OrderCreate
from bson import ObjectId
from database import db

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    result = await db.orders.insert_one(order.dict())
    return {"id": str(result.inserted_id)}

@router.get("/orders/{user_id}")
async def list_orders(user_id: str, limit: int = 10, offset: int = 0):
    orders_cursor = db.orders.find({"userId": user_id}).skip(offset).limit(limit)
    results = []
    async for order in orders_cursor:
        items = []
        total = 0
        for item in order["items"]:
            product = await db.products.find_one({"_id": ObjectId(item["productId"])})
            if not product:
                continue
            price = product["price"]
            total += price * item["qty"]
            items.append({
                "productDetails": {
                    "id": str(product["_id"]),
                    "name": product["name"]
                },
                "qty": item["qty"]
            })

        results.append({
            "id": str(order["_id"]),
            "items": items,
            "total": total
        })

    return {
        "data": results,
        "page": {
            "next": offset + limit,
            "limit": len(results),
            "previous": max(0, offset - limit)
        }
    }
