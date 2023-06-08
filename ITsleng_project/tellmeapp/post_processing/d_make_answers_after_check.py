import collections
import json
import os.path

cur_dir = os.path.dirname(__file__)

# Формирование списка из ответов
answers = []
with open(os.path.join(cur_dir, 'a_input_answers.txt'), 'r', encoding='utf-8') as fp:
    for line in fp:
        answers.append(json.loads(line.strip()))

# Считывание результатов обучения
with open(os.path.join(cur_dir, 'db_results.json')) as fp:
    db_result = json.load(fp)

# Формирование пустого файла для заполнения
with open(os.path.join(cur_dir, 'e_answers_after_check.txt'), 'w', encoding='utf-8') as fp:
    pass

# Заполнение целевого файла на основе "a_input_answers.txt"
for ans_list in answers:
    ans_res = db_result.get(ans_list[0], None)
    if ans_res:
        ans_list.extend(ans_res)
        ans_list = list(collections.OrderedDict.fromkeys(ans_list).keys())
    with open(os.path.join(cur_dir, 'e_answers_after_check.txt'), 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(ans_list, ensure_ascii=False) + '\n')



