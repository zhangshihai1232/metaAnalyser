#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from abc import ABCMeta, abstractmethod
class Analyser(object):
    __metaclass__ = ABCMeta

    def __init__(self, jobBaseDir, bashGetVariableFile, bashReadFile):
        self.jobBaseDir=jobBaseDir
        self.bashGetVariableFile=bashGetVariableFile
        self.bashReadFile=bashReadFile
        self.jobBasePath = os.path.join(self.jobBaseDir, 'job')

    def analyse(self):
        """
        分析文件
        1. filterFile
        2. doAnalyse
        3. recordInfo
        :param filePath:
        :return:
        """

        for root, dirs, files in os.walk(jobBasePath):
            for name in files:
                if self.filterFile(name):
                    filePath = os.path.join(root, name)
                    info = self.doAnalyse(filePath)
                    self.recordInfo(info)

    @abstractmethod
    def filterFile(self, fileName):
        """
        筛选需要的文件
        :param basePath:
        :return:
        """

    @abstractmethod
    def doAnalyse(self, filePath):
        """
        解析文件，生成所需的dict
        :param basePath:
        :return:
        """

    @abstractmethod
    def recordInfo(self, dict):
        """
        记录数据
        :param basePath:
        :return:
        """