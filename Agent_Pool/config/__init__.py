import os
from configparser import ConfigParser

# # 获取系统变量区分环境
mode = os.environ.get('SPRING_ENV')
if not mode or mode == '':
    mode = "dev"

cgf = ConfigParser()
cgf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config-{env}.ini'.format(env=mode))
cgf.read(cgf_file_path)
