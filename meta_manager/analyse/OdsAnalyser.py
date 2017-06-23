#!/usr/bin/python
# -*- coding: utf-8 -*-
import commands

import Analyser

class OdsAnalyser(Analyser):

    def filterFile(self, fileName):
        if fileName.startswith('ods_'):
            return True
        return False

    def doAnalyse(self, filePath):
        for line in self.readFile(filePath).split('\n'):
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
    def analyse(self, filePath):


    def getVariable(self, filePath, variable):
        return commands.getstatusoutput('bash {0} {1} {2}'.format(self.bashGetStatusOutput, filePath, variable))[1]

    # def readFile(self, filePath):
    #     return commands.getstatusoutput('bash {0} {1}'.format(self.bashReadFile, filePath))[1]

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
        pass

    def get_from_regex(dict, input_str, key, file_path):
        if dict.has_key(key):
            return None
        regex = r'\s*\${?SQOOP}?.+--%s\s+\${?(\S+)}?' % key
        search_obj = re.search(regex, input_str)
        if search_obj:
            ods_key = search_obj.group(1)
            dict[key] = get_value_of(file_path, ods_key)
            return dict[key]
        return None
