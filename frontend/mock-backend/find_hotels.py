import math
import hashlib

def hash_to_coords(location: str):
    """将地名哈希为二维坐标"""
    h = hashlib.md5(location.encode()).hexdigest()
    x = int(h[:8], 16) % 100
    y = int(h[8:16], 16) % 100
    return x, y

def read_hotels(filename="hotels.txt"):
    hotels = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            brand, name, x, y, price, rating = line.strip().split(",")
            hotels.append({
                "brand": brand,
                "name": name,
                "x": float(x),
                "y": float(y),
                "price": int(price),
                "rating": float(rating)
            })
    return hotels

def handler(event, context=None):
    """
    Serverless 入口函数
    event = {"location": "Shanghai"}
    """
    location = event.get("location", "Beijing")
    x, y = hash_to_coords(location)
    
    hotels = read_hotels()  # 读文件
    for h in hotels:
        h["distance"] = math.sqrt((h["x"] - x)**2 + (h["y"] - y)**2)
    
    top10 = sorted(hotels, key=lambda h: h["distance"])[:10]
    return {"query_location": location, "coords": (x, y), "results": top10}

# 测试用
if __name__ == "__main__":
    print(handler({"location": "Shanghai"}))
