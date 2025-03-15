import os
from datetime import datetime

from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.permission import SUPERUSER
from nonebot import on_command
from nonebot import logger

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="server_status",
    description="Get server status then return them to admin's qq account.",
    usage="/status",
    config=Config,
)

config = get_plugin_config(Config)

server_status = on_command("status", aliases={"ss"}, permission=SUPERUSER, priority=10)

@server_status.handle()
async def ask_status():
    TEMP_NORMAL = 55   
    TEMP_WARNING = 65  
    TEMP_CRITICAL = 75 
    uptime = get_uptime().replace('up ', '').strip()  # 清理uptime输出
    cpu_tem = get_server_temperature()
    mem = get_server_memory()
    temp_status = "⚠️" if cpu_tem > 55 else "✅"
    status_msg = f"""
    🖥️ Server Status 🔧
    ━━━━━━━━━━━━━━━━━━━━━━
    🕒 持续运行: {uptime.capitalize()}
    {
        "🔥 热炸了！" if cpu_tem >= TEMP_CRITICAL else 
        "⚠️ " if cpu_tem >= TEMP_WARNING else 
        "✅ "
    } CPU温度: {cpu_tem if cpu_tem != -1 else 'N/A'}℃
    💾 内存占用: {mem['used']} / {mem['total']} 
    ├─ 可用: {mem['available']} 
    └─ 缓存: {mem.get('buff/cache', 'N/A')}

    🔄  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ━━━━━━━━━━━━━━━━━━━━━━
    """.strip()
    await server_status.finish(status_msg)
    
def get_uptime():
    return os.popen("uptime -p").read()

def get_server_temperature():
    # /sys/class/thermal/thermal_zone0/temp
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temperature = float(file.read().strip()) / 1000
            return round(temperature, 2)
    except Exception as e:
        logger.opt(exception=True).error("Exception Error")
        return -1
    
def get_server_memory():
    # free -h
    #                    total        used        free      shared  buff/cache   available
    # Mem:           981Mi       335Mi        86Mi        33Mi       559Mi       538Mi
    # Swap:          490Mi          0B       490Mi

    raw_info = os.popen("free -h").read()
    list_info = raw_info.strip().split('\n')
    mem_info = next(parm for parm in list_info if 'Mem:' in parm).split()
    total_mem = mem_info[1]
    used_mem = mem_info[2]
    avail_mem = mem_info[6]
    buff_mem = mem_info[5]
    return {"total": total_mem, "used": used_mem, "available": avail_mem, "buff/cache": buff_mem}