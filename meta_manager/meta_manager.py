#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from jobs.meta_manager.analyse.analyse import analyse

job_dir_prefixs=['ods','pdw','mid','dw','mdw','app','rpt','druid','mail','dim']
job_suffixs=['job']
base_dir=os.path.join('../')

def check_job_dir(dir_name, prefix_list):
    """
    判断dir_name是否以job_prefix列表的内容开头
    :param dir_name:
    :param job_prefix:
    :return:
    """
    for prefix in prefix_list:
        if dir_name.startswith(prefix):
            return True
    return False

def check_job(job_name, suffix_list):
    """
    通过后缀检查是否是job
    :param job_name:
    :param suffix_list:
    :return:
    """
    for suffix in suffix_list:
        if job_name.endswith(suffix):
            return True
    return False

def job_root_walk(base_dir, check_job_dir, check_job, job_dir_prefixs, job_suffixs):
    """
    处理所有目录和目录下文件
    :param base_dir: 分析的根目录
    :param suffix: 后缀
    :param func: 处理函数
    :return:
    """
    for root, dirs, files in os.walk(base_dir):
        pure_dir_name=root.replace(base_dir,'')
        if check_job_dir(pure_dir_name, job_dir_prefixs):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                analyse(file_path)

job_root_walk(base_dir, check_job_dir, check_job, job_dir_prefixs, job_suffixs)



