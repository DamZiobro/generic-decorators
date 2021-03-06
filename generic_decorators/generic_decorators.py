#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 damian <damian@damian-desktop>
#
# Distributed under terms of the MIT license.

import concurrent.futures
import os
from functools import wraps
from time import time

from joblib import Parallel, delayed
import multiprocessing

"""
This fila contains generic useful decorators
"""

def timing(func):
    """
        Decorator which counts and print time which function take
    """
    @wraps(func)
    def wrap(*args, **kw):
        start_time = time()
        result = func(*args, **kw)
        elapsed = time() - start_time
        print('func:%r args:[%r, %r] took: %2.4f sec' % (func.__name__, args, kw, elapsed))
        return result
    return wrap


def make_parallel(func):
    """
        Decorator used to decorate any function which needs to be parallized.
        After the input of the function should be a list in which each element
        is a instance of input fot the normal function.
        You can also pass in keyword arguements seperatley.
        :param func: function
            The instance of the function that needs to be parallelized.
        :return: function
    """

    @wraps(func)
    def wrapper(lst):
        """

        :param lst:
            The inputs of the function in a list.
        :return:
        """
        # the number of threads that can be max-spawned.
        # If the number of threads are too high, then the overhead of creating the threads will be significant.
        # Here we are choosing the number of CPUs available in the system and then multiplying it with a constant.
        # In my system, i have a total of 8 CPUs so i will be generating a maximum of 16 threads in my system.
        number_of_threads_multiple = 2 # You can change this multiple according to you requirement
        number_of_workers = int(os.cpu_count() * number_of_threads_multiple)
        if len(lst) < number_of_workers:
            # If the length of the list is low, we would only require those many number of threads.
            # Here we are avoiding creating unnecessary threads
            number_of_workers = len(lst)

        if number_of_workers:
            if number_of_workers == 1:
                # If the length of the list that needs to be parallelized is 1, there is no point in
                # parallelizing the function.
                # So we run it serially.
                result = [func(lst[0])]
            else:
                # Core Code, where we are creating max number of threads and running the decorated function in parallel.
                result = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executer:
                    bag = {executer.submit(func, i): i for i in lst}
                    for future in concurrent.futures.as_completed(bag):
                        result.append(future.result())
        else:
            result = []
        return result
    return wrapper


def make_parallel_processes(func):
    """
    Similar like make_parallel, but uses multiprocessing (trigger new processes for each function)
    instead of threads.
    """

    @wraps(func)
    def wrapper(lst):
        """

        :param lst:
            The inputs of the function in a list.
        :return:
        """
        # the number of processes that can be max-spawned.
        number_of_workers = int(multiprocessing.cpu_count())
        if len(lst) < number_of_workers:
            # If the length of the list is low, we would only require those many number of processes
            # Here we are avoiding creating unnecessary processes
            number_of_workers = len(lst)

        if number_of_workers:
            if number_of_workers == 1:
                # If the length of the list that needs to be parallelized is 1, there is no point in
                # parallelizing the function.
                # So we run it serially.
                result = [func(lst[0])]
            else:
                # Core Code, where we are creating max number of processes and
                # running the decorated function in parallel.
                result = Parallel(n_jobs=number_of_workers)(delayed(func)(i) for i in lst)
        else:
            result = []
        return result
    return wrapper


def singleton(class_):
    """
    Class decorator which helps to create Singleton classes.
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            print(f"singleton(): creating class {class_.__name__}")
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance
