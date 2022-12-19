import json
from timeit import timeit

import rapidjson
import os
import random
from pprint import pprint

from mainapp.processing.extract_json import get_db_sentences

SESSIONFOLDER = 'sessionfiles'

def create_session_file(session_id):
    all_qa = get_db_sentences()["QA"]
    random.shuffle(all_qa)
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, SESSIONFOLDER, f'{session_id}.json')
    # запись данных JSON в файл
    with open(full_file_path, "w", encoding="utf-8") as new_session:
        new_session.write(str(all_qa).replace("'", '"'))
        print(f'Created new session file {session_id[-10:]}')
    return full_file_path


def remove_session_file(session_id):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, SESSIONFOLDER, f'{session_id}.json')
    os.remove(full_file_path)


def get_qa_session_sentence(session_id) -> dict:
    '''
    Функция берет первый вопрос и ставит его в конце
    '''
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, SESSIONFOLDER, f'{session_id}.json')
    # Читаем содержимое JSON
    with open(full_file_path, 'r', encoding="utf-8") as fp:
        qa_session_sentences: list = rapidjson.load(fp)

    # Берет первый в списке вопрос
    qa_session_sentence = qa_session_sentences.pop(0)
    # Записывает его в конец
    qa_session_sentences.append(qa_session_sentence)

    # Перезаписываем содержимое
    with open(full_file_path, "w+", encoding="utf-8") as newfp:
        newfp.write(str(qa_session_sentences).replace("'", '"'))

    return qa_session_sentence




if __name__ == '__main__':
    session_id = "5ce4727d-47d2-453b-8383-1db65f25bd30"
    # r1 = create_session_file(session_id)
    # r2 = get_qa_session_sentence(session_id)