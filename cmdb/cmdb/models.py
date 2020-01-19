# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, create_engine, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from string import ascii_lowercase, digits
from .types import get_instance
import random
import json

alphanum = ascii_lowercase + digits
def randstr(count:int=48):
    return ''.join([alphanum[random.randint(0, 35)] for _ in range(count)])

class Reference:
    def __init__(self, ref:dict):
        self.schema = ref.get('schema') # 引用的schema
        self.field = ref.get('field') # 引用的field
        self.on_delete = ref.get('on_delete', 'disable') # cascade, set_null, disable
        self.on_update = ref.get('on_update', 'disable') # cascade, disable

class FieldMeta:
    def __init__(self, metastr:str):
        meta = json.loads(metastr)
        tp = meta.get('type')

        if isinstance(tp, str): # 简写形式的type，没有option选项
            self.instance = get_instance(meta)
        elif isinstance(tp, dict):
            option = tp.get('option')
            if option:
                self.instance = get_instance(tp.get('name'), **option)
            else:
                self.instance = get_instance(tp.get('name'))

        self.unique = meta.get('unique', False)
        self.nullable = meta.get('nullable', True)
        self.default = meta.get('default')
        self.multi = meta.get('multi', False)

        ref = meta.get('reference')
        if ref:
            self.reference = Reference(ref)
        else:
            self.reference = None

# 基类
Base = declarative_base()

# 逻辑表
class Schema(Base):
    __tablename__ = 'schema'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False, unique=True)
    desc = Column(String(128), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)

    field = relationship('Field') # 指定的是类名


class Field(Base):
    __tablename__ = 'field'
    __table_args__ = (UniqueConstraint('schema_id', 'name'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    schema_id = Column(Integer, ForeignKey('schema.id'), nullable=False)
    meta = Column(Text, nullable=False)
    ref_id = Column(Integer, ForeignKey('field.id'), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)

    schema = relationship('Schema')
    ref = relationship('Field', uselist=False) # TODO; 1对1， 被引用的id

    @property
    def meta_data(self): # 增加一个属性将meta解析成对象，注意不要使用metadata这个名字
        return FieldMeta(self.meta)

# 逻辑表的记录
class Entity(Base):
    __tablename__ = 'entity'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String(48), nullable=False, unique=True) # TODO; 数据库序设置唯一
    schema_id = Column(Integer, ForeignKey('schema.id'), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    schema = relationship('Schema')

class Value(Base):
    __tablename__ = 'value'
    __table_args__ = (UniqueConstraint('entity_id', 'field_id', name='uq_entity_field'),)

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(Text, nullable=False)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    entity_id = Column(BigInteger, ForeignKey('entity.id'), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    entity = relationship('Entity')
    field = relationship('Field')

# mysql+pymysql://<username>:<password>@<host>:port/<dbname>[?<options>]
constructor = "{}://{}:{}@{}:{}/{}".format(
    'mysql+pymysql', 'root', 'xiangx', '192.168.1.20', 3306, 'cmdb2'
)

# 创建连接
engine = create_engine(constructor, echo=True)

# 创建session
Session = sessionmaker(bind=engine)
session = Session()

# 创建表
def create_all():
    Base.metadata.create_all(engine)

# 删除表
def delete_all():
    Base.metadata.drop_all(engine)

# create_all()