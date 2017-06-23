#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

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

def make_table_column_regex(table_name):
    return r'\s*CREATE\s+EXTERNAL\s+TABLE\s+`?{0}`?\s*\((\s*[^\)]+)\).+LOCATION\s+\S+/{0}\S+\s*;'.format(table_name)

def make_table_comment_partition_regex(table_name):
    return r'\s*CREATE\s+EXTERNAL\s+TABLE\s+`?{0}`?\s*\(\s*[^\)]+\)\s+COMMENT\s+\'(.+)\'\s+PARTITIONED\s+BY\s+\((.+)\).+LOCATION\s+\S+/{0}\S+\s*;'.format(table_name)

def analyse_sql(file_path):
    """
    输入.sql文件，从从建表语句中解析信息
    partition、table_desc、db_type
    :param file_path:
    :return:
    """
    partition=None
    table_desc=None
    db_type=None
    dict={}

    table_name_regex='\s*CREATE\s+EXTERNAL\s+TABLE\s+`?([\w]+)`?\s*\('
    table_partition_regex='^\s+PARTITIONED\s+BY\s+\((\s*`?\w+`?\s+\w+\s*,?)+\)'
    column_list = []
    partition_list = []

    file = open(file_path)
    try:
        content = file.read()
        content = content.replace('\n',' ')
        table_name_list = re.findall(table_name_regex, content)

        for table_name in table_name_list:
            # 分区信息
            search_object = re.search(make_table_comment_partition_regex(table_name), content)
            if search_object:
                partition_content = search_object.group(2)
                for partition_line in partition_content.split(','):
                    partition_line=partition_line.replace('`','')
                    partition_split=partition_line.strip().split(' ');
                    partition_list.append((table_name,partition_split[0],partition_split[1],'分区'))

            # 列信息
            search_object = re.search(make_table_column_regex(table_name), content)
            print search_object.group(0)
            if search_object:
                column_content = re.sub(r'\s+', ' ', search_object.group(1))
                for column_line in column_content.split(','):
                    column_split=column_line.strip().split(' ');
                    column_list.append((table_name,column_split[0],column_split[1],column_split[3]))
    finally:
        file.close()

def replace_head(instr,replace_str=''):
    return instr[instr.find('_')+1:]

def replace_tail(instr,replace_str=''):
    return instr[:instr.rfind('_')]

def table_name_resolve(table_name):
    """
    layer、subject、business、update_method、version
    :param table_name:
    :return:
    """
    layer=None
    subject=None
    business=None
    version=1
    update_method='全量'

    search_object = re.search(r'^[\w]+_[vV](\d+)', table_name)
    if search_object:
        version=int(search_object.group(1))
        table_name = replace_tail(table_name)

    if table_name.startswith('app_'):
        table_name = replace_head(table_name)

    if table_name.endswith('di'):
        update_method='增量'
        table_name = replace_tail(table_name)

    search_object = re.search(r'^([\da-zA-Z]+)_([\da-zA-Z]+)_(\w+)', table_name)
    if search_object:
        layer=search_object.group(1)
        subject=search_object.group(2)
        business=search_object.group(3)
    return layer,subject,business,version,update_method

