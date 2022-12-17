import random
from pprint import pprint

from mainapp.processing.extract_json import get_db_sentences


def generate_question() -> dict:
    sentences = get_db_sentences()
    question_dict = random.choice(sentences["QA"])
    #!!! Сразу генерировать с attemp = 1
    return question_dict


def tts_prompt_sound(question_body):
    if "<...>" in question_body:
        question_body = question_body.replace("<...>", "<speaker audio='alice-sounds-human-cough-1.opus'>")
    return question_body


def remove_tts_symbols(instance: str):
    if "+" in instance or " - " in instance:
        instance = instance.replace(" - ", "").replace("+", "")
    return instance


if __name__ == '__main__':
    s = " - +Оффер – это значит предложить. С предложениями надо быть аккуратнее."
    r = remove_tts_symbols(s)
    print(r)





if __name__ == '__main__':
    f = generate_question()
    pprint(f, sort_dicts=False)

    s = r"Вставь слово в предложение: Пока еще рано <...>, надо вначале баги пофиксить"
    r = tts_prompt_sound(s)
    print(r)