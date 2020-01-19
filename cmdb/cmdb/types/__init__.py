# -*- coding: utf-8 -*-

import ipaddress
import importlib

classes_cache = {}
instance_cache = {}

def get_class(type:str):
    cls = classes_cache.get(type)
    if cls:
        return cls

    # m, c = type.rsplit('.', maxsplit=1)
    # # print(m, c)
    # mod = importlib.import_module(m)
    # cls = getattr(mod, c)
    #
    # if issubclass(cls, BaseType):
    #     classes_cache[type] = cls
    #     return cls
    return TypeError('Wrong Type ! {} is not sub class of BaseType'.format(cls))

def get_instance(type:str, **option):
    key = ",".join("{}={}".format(k, v) for k, v in sorted(option.items()))
    key = "{}|{}".format(type, key)

    obj = instance_cache.get(key)
    if obj:
        return obj

    obj = get_class(type)(**option)
    instance_cache[key] = obj
    return obj

class BaseType:
    def __init__(self, **option:dict):
        self.option = option

    def __getattr__(self, item):
        return self.option.get(item)

    def stringify(self, value):
        raise NotImplementedError()

    def destringify(self, value):
        raise NotImplementedError()

class Int(BaseType):
    def stringify(self, value):
        """存到数据库前要做数据类型转黄"""
        val = int(value)
        # max = self.option.get('max')
        max = self.max
        if max and val > max:
            raise ValueError("too big")

        # min = self.option.get('min')
        min = self.min
        if min and val < min:
            raise ValueError("too small")

        return str(val)

    def destringify(self, value):
        return value

class IP(BaseType):
    def stringify(self, value):
        ipaddr = str(ipaddress.ip_address(value))
        prefix = self.prefix
        if not ipaddr.startswith(prefix):
            raise ValueError('prefix not match')
        return ipaddr

    def destringify(self, value):
        return value

# 加载类到字典
def inject_class_cache():
    mod = globals().get('__package__')
    for k, v in globals().items():
        if type(v) == type and k != 'BaseType' and issubclass(v, BaseType):
            classes_cache[k] = v
            classes_cache['{}.{}'.format(mod, k)] = v

    print(classes_cache)

inject_class_cache()