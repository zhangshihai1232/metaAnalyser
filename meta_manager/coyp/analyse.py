#!/usr/bin/python
# -*- coding: utf-8 -*-
from analyse_py import *
from analyse_sql import *

from jobs.meta_manager.coyp.analyse_job import *


def analyse(file):
    """
    根据不同后缀解析
    :param file:
    :return:
    """
    suffix=file.split('.')[-1]
    func = {
        "sql": analyse_sql,
        "job": analyse_job,
        "py": analyse_py,
    }
    if func.has_key(suffix):
        func[suffix](file)



# analyse('aaa.sql')