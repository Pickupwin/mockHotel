import subprocess
import time
import json
import re

def run_command(vcpu):
    """运行指定VCPU的命令并返回执行时间"""
    command = [
        "/root/faasit/demo-202405/venv/bin/python", "-m", "serverless_framework.controller", "mitosis", "restore",
        "--restore_mode", "parallel",
        "--restore_num", "100",
        "--vcpu", str(vcpu)
    ]
    
    start_time = time.time()
    result = subprocess.run(command, text=True)

    try:
        with open('/etc/mitosis/plot.log', 'r') as file:
            content = file.read()
        
        # 使用正则表达式匹配x数组
        pattern = r'x:\s*\[([^\]]+)\]'
        match = re.search(pattern, content)
        
        if match:
            x_values_str = match.group(1)
            # 将字符串转换为整数列表
            x_values = [int(x.strip()) for x in x_values_str.split(',')]
            
            if x_values:
                # 返回最后一个x值作为延迟
                latency = x_values[-1]
                return latency
            else:
                print(f"VCPU={vcpu}: 未找到有效的x值")
                return None
        else:
            print(f"VCPU={vcpu}: 未找到x数组")
            return None
            
    except FileNotFoundError:
        print(f"VCPU={vcpu}: plot.log文件未找到")
        return None
    except Exception as e:
        print(f"VCPU={vcpu}: 读取plot.log时发生错误: {e}")
        return None

def main():
    results = []
    
    for vcpu in [1, 2, 3, 4, 5]:
        print(f"正在测试 VCPU={vcpu}...")
        latency = run_command(vcpu)*0.001
        
        if latency is not None:
            cost = (vcpu * latency) / 30
            
            result = {
                "app": "hotelsearchv3",
                "config": f"1-{vcpu*1000}-0",
                "latency": latency,
                "cost": cost,
                "profile": ""
            }
            results.append(result)
            print(f"VCPU={vcpu} 测试完成, 延迟: {latency:.6f}秒")
        else:
            print(f"VCPU={vcpu} 测试失败")
        time.sleep(0.1)
    
    # 输出JSON格式结果到文件
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("结果已保存到 results.json")

if __name__ == "__main__":
    main()