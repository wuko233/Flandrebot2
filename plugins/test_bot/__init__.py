from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.rule import to_me


from .config import Config

__plugin_meta__ = PluginMetadata(
    name="test_bot",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

is_bot = on_command("机器人", rule=to_me(), aliases={"bot", "r0bot"}, priority=10, block=True)

@is_bot.handle()
async def handle_function():
    print("你才是机器人！！！")
    await is_bot.finish("你才是机器人！！！你全家机器人！！！")