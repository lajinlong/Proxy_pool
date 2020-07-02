# -*- coding: utf-8 -*-
"""自定义异常类"""


class PoolEmptyException(Exception):
    def __str__(self):
        """
        proxypool is used out
        :return:
        """
        return repr('no proxy in proxypool')
