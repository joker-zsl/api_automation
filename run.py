from tools.handle_path import log_path

# 存储日志文件代码
import pytest
from loguru import logger
from tools.handle_path import log_path

logger.add(sink=log_path,
           encoding="UTF8",
           level="INFO",
           rotation="10MB",
           retention= 20)

pytest.main(["-v","--alluredir=outputs/allure_report","--clean-alluredir"])
# pytest.main(["-v","-m p1","--alluredir=outputs/allure_report", "--clean-alluredir"])


