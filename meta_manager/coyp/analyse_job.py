#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import commands

#表名获取顺序：OUT->TABLE_NAME->file_name
def regex_head_get(input_str, info):
    """
    找出头信息内容如下
    DATE、OUT、DEV、DESC、PRODUCT_WIKI、DEV_WIKI
    :param input_str:
    :param info:
    :return:
    """
    regex=r'\s*#\s*%s\s*:\s*([\S]+)' % info
    if info=='DATE':
        regex=r'\s*#\s*%s\s*:\s*(\d{4}-\d{2}-\d{2})' % info

    search_obj=re.search(regex, input_str)
    if search_obj:
        return search_obj.group(1)
    return None

def fecth_from_line(dict, line, word, job_key):
    """
    :param dict:
    :param line:
    :param word: 获取到字典中
    :param job_key: 从job中查找
    :return:
    """
    if dict.has_key(word)==False:
        info = regex_head_get(line, job_key)
        if info!=None:
            dict[word]=info

def analyse_job(job_path):
    '''
    analysis file , get head comments
    :param job_path:
    :param list: 把结果存入这个list
    :return:
    '''
    dict={}
    dict['job_path'] = job_path
    dict['job_name'] = job_path.split('/')[-1].replace('.job', '')

    file = open(job_path)
    for line in file:
        fecth_from_line(dict, line, 'create_date', 'DATE')
        fecth_from_line(dict, line, 'author', 'DEV')
        fecth_from_line(dict, line, 'job_desc','DESC')
        fecth_from_line(dict, line, 'product_wiki','PRODUCT_WIKI')
        fecth_from_line(dict, line, 'dev_wiki','DEV_WIKI')
        fecth_from_line(dict, line, 'table_name','OUT')
        # 如果是ods,会单独处理ods信息
    print dict

##########################################################################
#              处理上传数据
##########################################################################
def process_ods_upload(file_path):
    print 'process_ods_upload'

##########################################################################
#              处理log同步
##########################################################################
def process_ods_logs(file_path):
    print 'process_ods_logs'

##########################################################################
#              处理数据库同步
##########################################################################
def get_value_of(file_path, variable):
    return commands.getstatusoutput('bash get_variable.sh {0} {1}'.format(file_path,variable))[1]

def read_ods_file(file_path):
    return commands.getstatusoutput('bash read_file.sh {}'.format(file_path))[1]

def get_from_regex(dict, input_str, key, file_path):
    if dict.has_key(key):
        return None
    regex = r'\s*\${?SQOOP}?.+--%s\s+\${?(\S+)}?' % key
    search_obj=re.search(regex, input_str)
    if search_obj:
        ods_key=search_obj.group(1)
        dict[key]=get_value_of(file_path, ods_key)
        return dict[key]
    return None

def process_ods_db(file_path):
    dict = {}
    for line in read_ods_file(file_path).split('\n'):
        get_from_regex(dict, line, 'connect', file_path)
        get_from_regex(dict, line, 'username', file_path)
        get_from_regex(dict, line, 'password', file_path)
        get_from_regex(dict, line, 'table', file_path)
    search_obj = re.search('jdbc:(\S+)://([0-9\.]+):(\d+)/(\S+)', dict['connect'])
    if search_obj:
        dict['db_type'] = search_obj.group(1)
        dict['ip'] = search_obj.group(2)
        dict['port'] = search_obj.group(3)
        dict['database'] = search_obj.group(4)
    return dict

#首先获得正确的输出
def analyse_ods(job_path, process):
    """
    如果是ods,分析ods特有的信息
    :param job_path:
    :return:
    """
    job_name = job_path.split('/')[-1].replace('.job', '')
    if job_name.startswith('ods_'):
        return process(job_path)
    return None

dict=analyse_ods('/home/nvme/code/wormpex/analysis-jobs/jobs/ods_wormpex_os_1_op_log_01/ods_wormpex_os_1_op_log_01.job', process_ods_db)
