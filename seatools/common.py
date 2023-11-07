# Public method
import logging


def judgment_login(func):
    """
    判断用户是否登录
    """
    def inner(*args, **kwargs):
        self = args[0]
        if self.token is None:
            raise Exception("Please login first")
        return func(*args)
    return inner


def iter_func(func):
    """
    测试打印 list
    """
    def inner(*args, **kwargs):
        res = func(*args)
        if not isinstance(res, list):
            raise Exception("此函数返回值不是 list")
        for index in res:
            print(index, end='\n')
    return inner


def logger():
    """
    日志打印配置
    """
    log = logging.getLogger("logger")
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    formats = logging.Formatter(fmt="%(asctime)s %(filename)s %(levelname)s %(message)s",
                                datefmt="%Y/%m/%d %X")

    sh.setFormatter(formats)
    log.addHandler(sh)

    return log
