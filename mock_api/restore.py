import subprocess
import requests
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import aiohttp

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hotel Reserve Service")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FtInvokeRequest(BaseModel):
    app_id: int
    path: str
    name: str
    mode: str = None
    provider: str = None

class FtInvokeResponse(BaseModel):
    success: bool
    data: dict = None
    error: str = None
    restore_log: str = None

def run_restore_command():
    """执行恢复命令"""
    try:
        logger.info("开始执行恢复命令...")
        
        # 构造完整的命令
        commands = [
            "cd ~/faststart/mitosis_app",
            "source ../venv/bin/activate",
            "python ./client.py restore --restore_mode parallel --restore_num 100"
        ]
        
        full_command = " && ".join(commands)
        
        # 使用shell执行命令
        result = subprocess.run(
            full_command,
            shell=True,
            executable="/bin/bash",
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode == 0:
            logger.info("恢复命令执行成功")
            return True, result.stdout
        else:
            logger.error(f"恢复命令执行失败: {result.stderr}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        error_msg = "恢复命令执行超时"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"执行恢复命令时发生异常: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

async def call_ft_invoke(request_data: dict) -> dict:
    """调用原始的ft/invoke接口"""
    try:
        # 原始后端地址
        target_url = "http://8.130.87.93:8328/ft/invoke"
        
        timeout = aiohttp.ClientTimeout(total=60)  # 60秒超时
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                target_url,
                json=request_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
                    
    except Exception as e:
        logger.error(f"调用ft/invoke接口失败: {str(e)}")
        raise

@app.post("/restore", response_model=FtInvokeResponse)
async def hotel_reserve_endpoint(request: FtInvokeRequest):
    """酒店预订端点 - 先执行恢复命令，再调用原始接口"""
    try:
        # 第一步：执行恢复命令
        logger.info(f"开始处理酒店预订请求: {request.dict()}")
        
        restore_success, restore_log = run_restore_command()
        
        if not restore_success:
            return FtInvokeResponse(
                success=False,
                error=f"恢复过程失败: {restore_log}",
                restore_log=restore_log
            )
        
        # 第二步：调用原始ft/invoke接口
        try:
            ft_response = await call_ft_invoke(request.dict())
            
            return FtInvokeResponse(
                success=True,
                data=ft_response,
                restore_log=restore_log
            )
            
        except Exception as ft_error:
            return FtInvokeResponse(
                success=False,
                error=f"调用后端服务失败: {str(ft_error)}",
                restore_log=restore_log
            )
            
    except Exception as e:
        logger.error(f"处理请求时发生未知错误: {str(e)}")
        return FtInvokeResponse(
            success=False,
            error=f"服务器内部错误: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "hotel-reserve-service"}

@app.post("/test-restore")
async def test_restore_command():
    """测试恢复命令的独立端点"""
    success, log = run_restore_command()
    return {
        "success": success,
        "log": log
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=5897,
        log_level="info"
    )