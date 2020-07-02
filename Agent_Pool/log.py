import logging
import os
from logging.handlers import TimedRotatingFileHandler



# ip = util.get_host_ip()
# LOG_PATH = os.environ['HOME'] + '/logs/archer/' + ip  # 日志存放目录
LOG_PATH = os.path.dirname(__file__) + '/logs/'
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH, exist_ok=True)

LOGGING_MSG_FORMAT = '%(asctime)s.%(msecs)d %(levelname)s [%(threadName)s,,,,] %(filename)s[%(funcName)s:%(lineno)s] -> %(message)s'
#
# app日志
# app_logger = logging.getLogger('app-logger')
# app_log_file = os.path.join(LOG_PATH, 'application.log')
# app_log_handler = TimedRotatingFileHandler(app_log_file, 'midnight', 1)
# # app_log_handler.setLevel(logging.DEBUG)
# app_logging_format = logging.Formatter(LOGGING_MSG_FORMAT, datefmt='%H:%M:%S')
# ch = logging.StreamHandler()
# # ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关
# app_log_handler.setFormatter(app_logging_format)
# ch.setFormatter(app_logging_format)
# app_logger.addHandler(app_log_handler)
# app_logger.addHandler(ch)

import logging

# 第一步，创建一个logger
app_logger = logging.getLogger()
app_logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile = LOG_PATH + './proxy.log'
# fh = logging.FileHandler(logfile, mode='a')
fh = TimedRotatingFileHandler(logfile, 'midnight', 1)
fh.setLevel(logging.DEBUG)  # 用于写到file的等级开关


# 第三步，再创建一个handler,用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

# 第四步，定义handler的输出格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter(LOGGING_MSG_FORMAT, datefmt='%H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
app_logger.addHandler(fh)
app_logger.addHandler(ch)
