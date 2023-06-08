import json
import os

cur_dir = os.path.dirname(__file__)

# with open(os.path.join(cur_dir, 'sentences_for_check.txt'), 'r', encoding='utf-8') as fp:
#     data = fp.readline()
#

sentences = []
with open(os.path.join(cur_dir, 'sentences_for_check.txt'), 'r', encoding='utf-8') as fp:
    for line in fp.readlines():
        sentences.append(line.strip())


# sentence = sentences.pop()

sentences.pop(0)

with open(os.path.join(cur_dir, 'sentences_for_check_.txt'), 'w', encoding='utf-8') as fp:
    for s in sentences:
        fp.write(f"{s}\n")