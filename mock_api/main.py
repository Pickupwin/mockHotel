from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import json


class InvokeRequest(BaseModel):
    location: str


class Hotel(BaseModel):
    name: str
    price: float
    rating: float


class PlotData(BaseModel):
    x: list[float]
    y: list[float]


app = FastAPI(title="Mock Hotel API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 解析日志文件的辅助函数
def parse_plot_log(file_path: str) -> PlotData:
    # 这里使用mock数据模拟解析结果
    # 在实际应用中，可以读取文件内容并解析
    if "para" in file_path:
        # 快速启动数据 (para)
        return PlotData(
            x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 26, 35, 36, 37, 38, 44, 45, 46, 47, 49, 50, 51, 62, 66, 67, 68, 80, 81, 82, 83, 84, 85],
            y=[5, 10, 16, 20, 25, 27, 30, 34, 38, 39, 40, 45, 49, 50, 52, 54, 56, 57, 62, 66, 69, 71, 73, 74, 78, 80, 87, 90, 94, 96, 98, 100]
        )
    else:
        # 普通启动数据 (seq)
        return PlotData(
            x=[0, 12, 58, 108, 138, 164, 210, 245, 272, 307, 347, 392, 435, 454, 468, 506, 537, 565, 588, 601, 639, 661, 710, 758, 777, 798, 848, 864, 876, 921, 964, 1014, 1029, 1061, 1096, 1123, 1164, 1198, 1248, 1267, 1309, 1356, 1404, 1418, 1463, 1506, 1528, 1576, 1613, 1639, 1661, 1700, 1715, 1747, 1792, 1822, 1861, 1877, 1897, 1922, 1969, 2002, 2031, 2066, 2114, 2125, 2154, 2204, 2232, 2279, 2290, 2339, 2352, 2389, 2411, 2429, 2455, 2479, 2490, 2540, 2565, 2596, 2615, 2655, 2673, 2703, 2747, 2762, 2784, 2817, 2865, 2880, 2908, 2924, 2962, 2999, 3028, 3040, 3088, 3135],
            y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        )


@app.post("/invoke")
def invoke(req: InvokeRequest) -> list[Hotel]:
    # Static demo data regardless of location
    hotels: list[Hotel] = [
        Hotel(name="Sunrise Hotel", price=129.0, rating=4.5),
        Hotel(name="City Center Inn", price=89.0, rating=4.1),
        Hotel(name="Lakeside Resort", price=159.0, rating=4.7),
        Hotel(name="Budget Stay", price=59.0, rating=3.9),
        Hotel(name="Grand Palace", price=199.0, rating=4.8),
    ]
    return hotels


@app.get("/hotel-search/quick-start")
def get_quick_start_data() -> PlotData:
    """获取快速启动数据（对应para-251103-0942/plot.log）"""
    file_path = "/Users/bytedance/BowenSu/mockHotel/mitosis_log/para-251103-0942/plot.log"
    return parse_plot_log(file_path)


@app.get("/hotel-search/normal-start")
def get_normal_start_data() -> PlotData:
    """获取普通启动数据（对应seq-251103-0938/plot.log）"""
    file_path = "/Users/bytedance/BowenSu/mockHotel/mitosis_log/seq-251103-0938/plot.log"
    return parse_plot_log(file_path)


# To run locally:
#   uvicorn main:app --reload --host 0.0.0.0 --port 8000


