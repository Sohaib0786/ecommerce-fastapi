from fastapi import APIRouter, Query
from typing import Optional
from bson import ObjectId
from database import db
from models.product_model import ProductCreate

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: ProductCreate):
    result = await db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@router.get("/products")
async def list_products(name: Optional[str] = None,
                        size: Optional[str] = None,
                        limit: int = 10,
                        offset: int = 0):

    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size

    cursor = db.products.find(query, {"sizes": 0}).skip(offset).limit(limit)
    products = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        products.append(doc)

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": len(products),
            "previous": max(0, offset - limit)
        }
    }
