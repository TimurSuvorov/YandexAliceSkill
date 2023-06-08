import collections
import json
import os.path

cur_dir = os.path.dirname(__file__)

# Формирование списка из вариантов
variants = []
with open(os.path.join(cur_dir, 'a_input_variants.txt'), 'r', encoding='utf-8') as fp:
    for line in fp:
        variants.append(json.loads(line.strip()))

# Считывание результатов обучения
with open(os.path.join(cur_dir, 'db_results.json')) as fp:
    db_result = json.load(fp)

# Формирование пустого файла для заполнения
with open(os.path.join(cur_dir, 'e_variants_after_check.txt'), 'w', encoding='utf-8') as fp:
    pass

# Заполнение целевого файла на основе "a_input_variants.txt"
for var_list in variants:
    check_res_all = []
    [var_list.extend(db_result.get(var_list[var_id])) for var_id in range(0, 3)
     if db_result.get(var_list[var_id], None)]

    var_list = list(collections.OrderedDict.fromkeys(var_list).keys())
    with open(os.path.join(cur_dir, 'e_variants_after_check.txt'), 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(var_list, ensure_ascii=False) + '\n')



