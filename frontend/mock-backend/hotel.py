from fastapi import FastAPI, Query
from pydantic import BaseModel
from find_hotels import handler as find_handler
from book_hotel import handler as book_handler

app = FastAPI()


# ---- 请求体模型 ----
class ReserveRequest(BaseModel):
    hotel_id: int


# ---- 酒店搜索接口 ----
@app.get("/hotel-search")
def search(location: str = Query(..., description="输入地名，例如 Shanghai")):
    """
    调用 find_hotels.handler 返回最近的10家酒店
    """
    result = find_handler({"location": location})
    # 转成简化输出（前端用）
    hotels = []
    for i, h in enumerate(result["results"], start=1):
        hotels.append({
            "id": i,  # 本demo使用顺序ID
            "name": h["name"],
            "brand": h["brand"],
            "price": h["price"],
            "rating": h["rating"],
            "distance": round(h["distance"], 2),
        })
    return hotels


# ---- 酒店预订接口 ----
@app.post("/hotel-reserve")
def reserve(req: ReserveRequest):
    """
    调用 book_hotel.handler 完成预订（总是成功）
    """
    # demo逻辑：偶数ID -> 模拟失败，奇数ID -> 成功
    # if req.hotel_id % 2 == 0:
        # return {"success": False, "message": "预订失败（模拟）"}
    
    # 找到对应酒店（可选）
    hotel_name = f"Hotel #{req.hotel_id}"
    result = book_handler({"hotel_name": hotel_name})
    return {"success": True, "confirmation": result["confirmation_id"]}


# ---- 根路径 ----
@app.get("/")
def root():
    return {"message": "Serverless Hotel Booking Demo Running"}
