#!/usr/bin/python
# -*- coding: utf-8 -*-
class Mapper:
    __mapper_relation = {}

    @staticmethod
    def register(cls, value):
        Mapper.__mapper_relation[cls] = value

    @staticmethod
    def exist(cls):  ###判断是否在里面
        if cls in Mapper.__mapper_relation:
            return True
        return False

    @staticmethod
    def value(cls):
        return Mapper.__mapper_relation[cls]


class MyType(type):
    def __call__(cls, *args, **kwargs):  ##执行Type的__call__方法，这里的cls就是<__main__.Foo object at 0x001B59F0> Foo类
        obj = cls.__new__(cls, *args, **kwargs)  ##Foo的__new__方法
        arg_list = list(args)
        if Mapper.exist(cls):
            value = Mapper.value(cls)
            arg_list.append(value)
        obj.__init__(*arg_list, **kwargs)  ##在执行Foo的__init__的之前做什么操作
        return obj