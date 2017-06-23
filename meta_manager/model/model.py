#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, Text, BIGINT

Base = declarative_base()
class Extend():
    @classmethod
    def insert(self, dict):
        some_engine = create_engine('postgresql://sean:sean@localhost/')
        Session = sessionmaker(bind=some_engine)
        session = Session()
        session.add(self.newInstance(dict))
        session.commit()

    @classmethod
    def newInstance(self, dict):
        return self(**dict)

class DependenceInfo(Base, Extend):
    class_name='DependenceInfo'
    __tablename__ = 'dependence_info'
    id = Column(BIGINT, primary_key=True)
    table_id = Column(BIGINT, ForeignKey('table_info.id'))
    dependence_id = Column(BIGINT)

class ColumnInfo(Base):
    __tablename__ = 'column_info'
    id = Column(BIGINT, primary_key=True)
    table_id = Column(BIGINT, ForeignKey('table_info.id'))
    column_name = Column(String(100))
    column_alias = Column(String(100))
    pos = Column(Integer)
    is_partition = Column(Integer)
    table_comment = Column(Text)

class OdsInfo(Base):
    __tablename__ = 'ods_info'
    id = Column(BIGINT, primary_key=True)
    src_ip = Column(String(200))
    src_connection = Column(String(200))
    src_username = Column(String(200))
    src_passwd = Column(String(200))
    src_db = Column(String(200))
    src_table = Column(String(200))
    table_id = Column(BIGINT, ForeignKey('table_info.id'))

class JobInfo(Base):
    __tablename__ = 'job_info'
    id = Column(BIGINT, primary_key=True)
    job_name = Column(String(255))
    job_path = Column(Text)
    create_time = Column(Time)
    update_time = Column(Time)
    author = Column(String(50))
    job_desc = Column(Text)
    product_wiki =Column(Text)
    dev_wiki =Column(Text)
    table_id =Column(BIGINT, ForeignKey('table_info.id'))

class TableInfo(Base):
    __tablename__ = 'table_info'
    id = Column(BIGINT, primary_key=True)
    table_name = Column(String(255))
    layer = Column(String(50))
    subject = Column(String(100))
    business = Column(String(200))
    partition = Column(String(100))
    create_time = Column(Time)
    update_time = Column(Time)
    update_method = Column(String(50))
    table_desc = Column(Text)
    version = Column(Integer)
    db_type =Column(String(50))
    jobs=relationship('JobInfo')
    dependencies=relationship('DependenceInfo')
    columns=relationship('ColumnInfo')
    ods=relationship('OdsInfo')

DependenceInfo.insert(dict)