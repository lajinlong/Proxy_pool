
# redis hash table key name
import platform

REDIS_KEY = 'proxies:universal'

# definition of proxy scores
PROXY_SCORE_MAX = 10
PROXY_SCORE_MIN = 0
PROXY_SCORE_INIT = 5

# definition of proxy number
PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

# definition of tester
TEST_URL = 'https://www.baidu.com'
TEST_TIMEOUT = 10
TEST_BATCH = 20
TEST_VALID_STATUS = [200, 206, 302]

# definition of api
API_HOST = '127.0.0.1'
API_PORT = 5000
API_THREADED = True

# definition of tester cycle, it will test every CYCLE_TESTER second
CYCLE_TESTER = 10
# definition of getter cycle, it will get proxy every CYCLE_GETTER second
CYCLE_GETTER = 30

# definition of flags
IS_WINDOWS = platform.system().lower() == 'windows'

# flags of enable
ENABLE_TESTER = True
ENABLE_GETTER = True
ENABLE_SERVER = True