def handler(event, context=None):
    """
    event = {"hotel_name": "Hilton Hotel #12"}
    """
    hotel_name = event.get("hotel_name")
    if not hotel_name:
        return {"status": "error", "message": "hotel_name missing"}
    
    # 模拟成功预定
    print(f"✅ Booking confirmed for {hotel_name}")
    return {
        "status": "success",
        "hotel_name": hotel_name,
        "confirmation_id": f"CONF-{hash(hotel_name) % 1000000}"
    }

# 测试用
if __name__ == "__main__":
    print(handler({"hotel_name": "Hilton Hotel #12"}))
