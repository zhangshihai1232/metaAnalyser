#!/usr/bin/python
# -*- coding: utf-8 -*-
import commands
import re

def get_value_of(file_path, variable):
    search_obj = re.search('\$?{?(\w+)}?', variable)
    if search_obj:
        variable=search_obj.group(1)
        return commands.getstatusoutput('bash get_variable.sh {0} {1}'.format(file_path,variable))[1]
    return None

def make_dependence_list(content):
    dependence_regex='\s+(from|join|with)\s+([\$\w]+)'
    dependence_list=re.findall(dependence_regex, content, re.I)
    return dependence_list

def analyse_dependence(file_path):
    file = open(file_path)
    content_list=[]
    try:
        content = file.read()
        content=re.sub('\s*#.*\n', '', content)
        content=re.sub('--.*\n', '\n', content)
        content=content.replace('\n','')
        contents=make_dependence_list(content)
        #替换变量
        for elem in contents:
            if elem[1].startswith('$'):
                print elem[1]
                content_list.append(get_value_of(file_path,elem[1]))
            else:
                content_list.append(elem[1])
        print content_list
    finally:
        file.close()

file_path='/home/nvme/code/wormpex/analysis-jobs/jobs/meta_manager/template.job'
analyse_dependence(file_path)
