import random
import re


def generate_var_buttons(question_variants) -> list:
    """
    Функция формирует список ответов в необходимом формате для suggest-кнопок
    """
    buttons_list = []

    for var in question_variants[:3]:
        buttons_list.append({'title': f'⚡{var.replace("+", "").capitalize()}', 'hide': 'true'})
        random.shuffle(buttons_list)
    buttons_list.append({'title': "🤔Сдаюсь!", 'hide': 'true'})
    return buttons_list


def generate_var_string(question_variants: list) -> str:
    """
    Функция форматирует список вариантов ответа, перемешивая их, для отображения в ответе
    """
    random.shuffle(question_variants)
    buttons_str: str = "•   " + "\n•   ".join(question_variants)
    return buttons_str


def tts_prompt_sound(question_body: str) -> str:
    """
    Функция заменяет пропущенное слово-загадку на звук для последующей передачи в tts ответа
    """
    if "<...>" in question_body:
        question_body = question_body.replace("<...>", "<speaker audio='alice-sounds-human-cough-1.opus'>")
    return question_body


def remove_tts_symbols(instance: str) -> str:
    """
    Функция удаляет все tts символы для последующего отображения в text ответа
    """
    if "+" in instance or " - " in instance:
        instance: str = instance.replace(" - ", "").replace("+", "")
    if "sil" in instance:
        instance: str = re.sub(r"(sil <\[\d{1,3}\]>)", "", instance)
    return instance
