# #!/usr/bin/env python3
# import json
# import re
# from collections import defaultdict
# # from itertools import
#
# file_target = 'rsrc/ingredients.json'
# file_source = 'rsrc/ingredients.txt'
# category_dico = defaultdict(list)
#
#
# def format(element):
#     print(f'Process {element.strip()}')
#     if ' ' in element:
#         element = re.sub('[0-9]*', '', element)
#         name = element.strip()
#     else:
#         name = element.strip()
#     category_list = list(category_dico.keys())
#     category_avali = '\n'.join([str(x) for x in zip(range(len(category_list)), category_list)])
#     category = input(f'Category of element {name} \n{category_avali}\n')
#     if category.isdigit():
#         category = category_list[int(category)]
#     if category == '':
#         return None, None
#     category_dico[category] = [name.strip()]
#     return (name.strip(), category)
#
# # lines = list(map(format, open(file_source)))
#
# # for name, category in lines:
# #     category_dico[category].append(name)
#
# with open(file_target, 'r') as fout:
#     data = fout.read()
# result  = json.loads(data)
# result_new = defaultdict(list)
# for category,list_el in result.items():
#     result_new[category] = list(sorted(list(set(list_el))))
#
# with open(file_target, 'w') as fout:
#     fout.write(json.dumps(result_new))
#
# print('end')
