import collections
from time import time, perf_counter

from typing import TypeVar, Deque, List, Dict

import rapidjson
import os
import random

from mainapp.processing.db.extract_json import get_db_sentences

PathLike = TypeVar("PathLike", str, os.PathLike)

cur_dir: PathLike = os.path.dirname(__file__)
SESSIONFOLDER: PathLike = os.path.join(cur_dir, 'sessionfiles')

TIME_1DAY_AGO = 1 * 24 * 60 * 60
TIME_2MIN_AGO = 2 * 60


def create_session_file(session_id: str) -> dict:
    """
    Функция запрашивает имеющийся список всех вопросов, перемешивает и
    записывает их в созданный здесь же файл для сессии в ./sessionfiles.
    Таким образом, для каждой сессии очередность вопросов будет случайной.
    """
    sentences = get_db_sentences()
    all_qa = sentences["QA"]
    random.shuffle(all_qa)
    full_file_path = os.path.join(SESSIONFOLDER, f'{session_id}.json')
    # запись данных JSON в файл
    with open(full_file_path, "w", encoding="utf-8") as new_session_fp:
        rapidjson.dump(all_qa, new_session_fp, ensure_ascii=False)
        print(f'Created new session file {session_id[-10:]}')
    return sentences


def remove_session_file(session_id: str) -> None:
    """
    Функция удаляет файл сессии по его идентификатору
    """
    full_file_path: PathLike = os.path.join(SESSIONFOLDER, f'{session_id}.json')
    os.remove(full_file_path)


def get_qa_session_sentence(session_id: str) -> dict:
    """
    Функция берет первый вопрос и ставит его в конце. Отдаёт следующий как новый вопрос.
    """
    full_file_path: PathLike = os.path.join(SESSIONFOLDER, f'{session_id}.json')
    # Читаем содержимое JSON
    with open(full_file_path, 'r', encoding="utf-8") as fp:
        qa_session_sentences: Deque = collections.deque(rapidjson.load(fp))
    # Берет первый в списке вопрос
    qa_session_sentence: Dict = qa_session_sentences.popleft()
    # Записывает его в конец
    qa_session_sentences.append(qa_session_sentence)
    # Перевод из структуры deque в list
    qa_session_sentences: List = list(qa_session_sentences)
    # Перезаписываем содержимое
    with open(full_file_path, "w", encoding="utf-8") as newfp:
        rapidjson.dump(qa_session_sentences, newfp, ensure_ascii=False)

    return qa_session_sentence


def remove_sessions_old_files(time_ago: int):
    """
    Функция удаляет файлы сессии старее, чем `time_ago`.
    """
    time_now = time()
    files: List[str] = os.listdir(SESSIONFOLDER)
    files = [os.path.join(SESSIONFOLDER, file) for file in files]
    for file in files:
        time_cr: float = os.stat(file).st_ctime
        if (time_now - time_cr) > time_ago:
            os.remove(file)


