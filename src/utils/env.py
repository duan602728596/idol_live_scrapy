""" 获取当前环境变量 """

from os import getenv
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent
# 加载环境变量
load_dotenv(Path.joinpath(ROOT_DIR, '.env'))
# 数据库配置
postgres_url: str = getenv('DATABASE_URL')
# 是否是测试环境
in_test_env: bool = getenv('TEST') is not None
