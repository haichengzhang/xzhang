# -*- coding: utf-8 -*-
# import json
# import importlib
# from cmdb.types import get_instance
#
# # 模拟字段保存的json
# jsonstr = """
# {
#     "type":"cmdb.types.IP",
#     "value":"192.168.1.10",
#     "option":{
#         "prefix":"192"
#     }
# }
# """
#
# obj = json.loads(jsonstr)
# # print(obj, type(obj))
#
# # 结果为 {'type': 'cmdb.types.Int', 'value': 300}
#
# print(get_instance(obj['type'], **obj.get('option', {})).stringify(obj['value']))















