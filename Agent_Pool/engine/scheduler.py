# -*- coding: utf-8 -*-
"""调度器"""
from log import app_logger
from engine.getproxy import Getproxies
from engine.testerproxy import Tester
from engine.webserver import app
import time
import multiprocessing
from config.settings import CYCLE_TESTER, CYCLE_GETTER, IS_WINDOWS, ENABLE_SERVER, ENABLE_TESTER, ENABLE_GETTER, \
    API_HOST, API_PORT, API_THREADED
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
# sch = BackgroundScheduler()
sch = BlockingScheduler()

if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, getter_process, server_process = None, None, None


class Scheduler(object):
    """Scheduler"""

    def run_tester(self, cycle=CYCLE_TESTER):
        """
        定时启动检测器
        :param cycle:
        :return:
        """
        if not ENABLE_TESTER:
            app_logger.info('tester not enabled, exit')
            return
        tester = Tester()
        sch.add_job(tester.run, 'interval', seconds=cycle, id='run_tester')
        sch.start()

    def run_getter(self, cycle=CYCLE_GETTER):
        """
        定时开启爬虫补充代理
        :param cycle:
        :return:
        """
        if not ENABLE_GETTER:
            app_logger.info('getter not enabled, exit')
            return
        getter = Getproxies()
        sch.add_job(getter.run, 'interval', seconds=cycle, id='run_getter')
        sch.start()

    def run_server(self):
        """web服务端开启"""
        if not ENABLE_SERVER:
            app_logger.info('server not enabled, exit')
            return
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)

    def run(self):
        """调度器启动"""
        global tester_process, getter_process, server_process
        try:
            app_logger.info('starting proxypool...')
            if ENABLE_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester)
                app_logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            if ENABLE_GETTER:
                getter_process = multiprocessing.Process(target=self.run_getter)
                # print(dir(getter_process),getter_process)
                app_logger.info(f'starting getter, pid{getter_process.pid}...')
                getter_process.start()

            if ENABLE_SERVER:
                server_process = multiprocessing.Process(target=self.run_server)
                app_logger.info(f'starting server, pid{server_process.pid}...')
                server_process.start()

            tester_process.join()
            getter_process.join()
            server_process.join()
        except KeyboardInterrupt:
            app_logger.info('received keyboard interrupt signal')
            tester_process.terminate()
            getter_process.terminate()
            server_process.terminate()
        finally:
            # must call join method before calling is_alive
            tester_process.join()
            getter_process.join()
            server_process.join()
            app_logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            app_logger.info(f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            app_logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            app_logger.info('proxy terminated')


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()