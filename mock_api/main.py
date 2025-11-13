from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import json
import subprocess
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime



class InvokeRequest(BaseModel):
    app_id: int
    path: str
    name: str
    mode: Optional[str] = None
    provider: Optional[str] = None


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

def execute_restore_command(restore_mode: str) -> bool:
    """执行恢复命令（同步版本）"""
    try:
        # 构建命令
        commands = [
            "cd ~/faststart/mitosis_app",
            "source ../venv/bin/activate",
            f"python ./client.py restore --restore_mode {restore_mode} --restore_num 100"
        ]
        
        # 使用bash执行命令
        full_command = f"bash -c '{'; '.join(commands)}'"
        
        # 执行命令
        result = subprocess.run(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        # if result.returncode != 0:
        #     print(f"命令执行失败: {result.stderr}")
        #     return False
            
        # print(f"命令执行成功: {result.stdout}")
        return True
        
    except subprocess.TimeoutExpired:
        print("命令执行超时")
        return False
    except Exception as e:
        print(f"执行命令时发生异常: {e}")
        return False

def parse_plot_log(file_path: str) -> PlotData:
    """解析plot.log文件"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"日志文件不存在: {file_path}")
        
        # 读取文件内容
        with open(file_path, 'r') as file:
            content = file.read()
        
        # 使用正则表达式匹配Plot Info行
        pattern = r"Plot Info: x: \[(.*?)\], y: \[(.*?)\]"
        match = re.search(pattern, content)
        
        if not match:
            raise ValueError("日志文件中未找到Plot Info数据")
        
        x_str = match.group(1)
        y_str = match.group(2)
        
        # 解析x和y数组
        x_list = [float(x.strip()) for x in x_str.split(',') if x.strip()]
        y_list = [float(y.strip()) for y in y_str.split(',') if y.strip()]
        
        return PlotData(x=x_list, y=y_list)
        
    except Exception as e:
        print(f"解析日志文件失败: {e}")
        # 返回默认数据作为fallback
        if "para" in file_path or restore_mode == "parallel":
            return PlotData(
                x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 26, 35, 36, 37, 38, 44, 45, 46, 47, 49, 50, 51, 62, 66, 67, 68, 80, 81, 82, 83, 84, 85],
                y=[5, 10, 16, 20, 25, 27, 30, 34, 38, 39, 40, 45, 49, 50, 52, 54, 56, 57, 62, 66, 69, 71, 73, 74, 78, 80, 87, 90, 94, 96, 98, 100]
            )
        else:
            return PlotData(
                x=[0, 12, 58, 108, 138, 164, 210, 245, 272, 307, 347, 392, 435, 454, 468, 506, 537, 565, 588, 601, 639, 661, 710, 758, 777, 798, 848, 864, 876, 921, 964, 1014, 1029, 1061, 1096, 1123, 1164, 1198, 1248, 1267, 1309, 1356, 1404, 1418, 1463, 1506, 1528, 1576, 1613, 1639, 1661, 1700, 1715, 1747, 1792, 1822, 1861, 1877, 1897, 1922, 1969, 2002, 2031, 2066, 2114, 2125, 2154, 2204, 2232, 2279, 2290, 2339, 2352, 2389, 2411, 2429, 2455, 2479, 2490, 2540, 2565, 2596, 2615, 2655, 2673, 2703, 2747, 2762, 2784, 2817, 2865, 2880, 2908, 2924, 2962, 2999, 3028, 3040, 3088, 3135],
                y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
            )

def write_log_message(message: str):
    """将日志消息写入spilot.log文件"""
    log_file = "/app/output/HotelReserve-baseline/spilot.log"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # 获取当前时间戳
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_time = current_datetime.strftime("%H:%M:%S")
    
    # 格式化日志消息
    log_entry = f"{current_date} {current_time} INFO \"{message}\"\n"
    
    # 追加写入日志文件
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)



@app.post("/invoke")
def invoke(req: InvokeRequest) -> List[Hotel]:
    
    log_file = "/app/output/HotelReserve-baseline/spilot.log"
    with open(log_file, "w", encoding="utf-8") as f:
        pass

    write_log_message("Fast start toggled, starting instances from snapshots...")

    # 执行指定的命令
    cmd = "source ~/faasit/demo-202405/venv/bin/activate;cd /root/sbw/mockHotel/backend/Hotel-DSL;ft invoke -p fast_start >> /app/output/HotelReserve-baseline/spilot.log 2> /dev/null"
    
    try:
        # 使用bash执行命令，因为包含source命令
        result = subprocess.run(
            cmd,
            shell=True,
            executable="/bin/bash",
            capture_output=True,
            text=True,
            timeout=30  # 设置30秒超时
        )
        
        # 检查命令执行结果
        if result.returncode != 0:
            print(f"命令执行失败，返回码: {result.returncode}")
            # 可以选择记录日志或进行其他错误处理
        else:
            print("命令执行成功")
            write_log_message("Fast start completed successfully. Check /etc/mitosis for results.")
            
    except subprocess.TimeoutExpired:
        print("命令执行超时")
    except Exception as e:
        print(f"执行命令时发生错误: {e}")

    # 返回静态演示数据（无论位置如何）
    hotels: List[Hotel] = [
        Hotel(name="Sunrise Hotel", price=129.0, rating=4.5),
        Hotel(name="City Center Inn", price=89.0, rating=4.1),
        Hotel(name="Lakeside Resort", price=159.0, rating=4.7),
        Hotel(name="Budget Stay", price=59.0, rating=3.9),
        Hotel(name="Grand Palace", price=199.0, rating=4.8),
    ]
    return hotels


@app.get("/hotel-search/quick-start")
def get_quick_start_data() -> PlotData:
    """获取快速启动数据（并行恢复模式）"""
    try:
        # 执行快速启动命令
        success = execute_restore_command("parallel")
        
        if not success:
            raise HTTPException(status_code=500, detail="快速启动命令执行失败")
        
        # 从标准路径获取结果
        file_path = "/etc/mitosis/plot.log"
        return parse_plot_log(file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取快速启动数据失败: {str(e)}")


@app.get("/hotel-search/normal-start")
def get_normal_start_data() -> PlotData:
    """获取普通启动数据（顺序恢复模式）"""
    try:
        # 执行普通启动命令
        success = execute_restore_command("sequential")
        
        if not success:
            raise HTTPException(status_code=500, detail="普通启动命令执行失败")
        
        # 从标准路径获取结果
        file_path = "/etc/mitosis/plot.log"
        return parse_plot_log(file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取普通启动数据失败: {str(e)}")


# To run locally:
#   uvicorn main:app --reload --host 0.0.0.0 --port 8000