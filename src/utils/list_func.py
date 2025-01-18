""" 对list的一些操作 """

from typing import Callable


def _list_core(array: list, callback: Callable, init_value: bool, judge_value: bool) -> bool:
    """ 判断数组的核心函数 """
    result: bool = init_value
    for item in array:
        if callback(item) is judge_value:
            result = judge_value
            break
    return result


def list_every(array: list, callback: Callable) -> bool:
    """ 满足数组所有条件 """
    return _list_core(array, callback, True, False)


def list_some(array: list, callback: Callable) -> bool:
    """ 满足内有一个满足条件 """
    return _list_core(array, callback, False, True)
