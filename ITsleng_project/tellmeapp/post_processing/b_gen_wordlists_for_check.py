import json
import os.path

cur_dir = os.path.dirname(__file__)

# Формирование списка из ответов
answers = []
with open(os.path.join(cur_dir, 'a_input_answers.txt'), 'r', encoding='utf-8') as fp:
    for line in fp:
        answers.append(json.loads(line.strip()))

ans_list = []
for w in answers:
    ans_list.append(w[0])

with open(os.path.join(cur_dir, 'bb__answers_for_check.txt'), 'w', encoding='utf-8') as fp:
    fp.write(str(f'answers_for_check = {ans_list}'))

# Формирование списка из вариантов
variants = []
with open(os.path.join(cur_dir, 'a_input_variants.txt'), 'r', encoding='utf-8') as fp:
    for line in fp:
        variants.append(json.loads(line.strip()))

var_list = []
for w in variants:
    var_list.extend(w[0:3])
with open(os.path.join(cur_dir, 'bb__variants_for_check.txt'), 'w', encoding='utf-8') as fp:
    fp.write(str(f'variants_for_check = {var_list}'))
