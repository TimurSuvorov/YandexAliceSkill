import random
from enum import Enum


class Image(Enum):
    # Приветствие.
    HI = [
        '213044/fff44481883c826a21fa'
    ]
    # Вызов "Правила".
    RULES = [
        '1030494/965748bbb13fd2c06af9',
    ]
    # Вызов "Что умеешь?".
    ABOUT = [
        '213044/a700f6301a1cb2ac307c',
    ]
    # Выход из игры.
    BYE = [
        '1533899/407c99f61e52e219dc88',
        '965417/8a29fba9419ef5325a5c',
    ]
    # Запрос на повторение
    REPEAT = [
        '937455/d7516071f6240f61230c'
    ]
    # Новый/первый вопрос.
    NEW_QUEST = [
        '1030494/83ea6af57c677159b31b',
        '1030494/66d774c8a767f8472c75',
    ]
    # Верный ответ.
    CORRECT_ANSWER = [
        '1030494/2becceeb83472f656b86',
        '1652229/70132eb12c40eb63ac98',
        '1652229/fe345b0f3cf6632cde04',
    ]
    # Неверный ответ. Попытка 1.
    WRONG_ANSWER_1 = [
        '965417/d19d0cf213a535d8faee',
        '1533899/0b69063950976f611181',
    ]
    # Неверный ответ. Попытка 2.
    WRONG_ANSWER_2 = [
        '1030494/e9fbd70389dffb2f7937',
        '997614/d9a88a5a8453b3d747de',
        '1652229/3c735868ff71d22dccd6',
    ]
    # Сдался или пропустил.
    GAVEUP = [
        '213044/5d811387ed334bc05815',
        '1030494/456b380eaa2f9aa24f9d',
    ]
    # Вызов рейтинга.
    RATING = [
        '1030494/0fe6f908f175e997963e',
    ]

    # Вне сценария.
    OFF_SCRIPT = [
        '997614/931c89708835804490e7',
        '965417/065851d63e72c2fc52c9',
    ]
    # Нецензурная речь.
    OBSCENE = [
        '997614/84b8fe2802d48eaa6fb2',
        '997614/ab1c98dc43b89673a4ab',
    ]

    @property
    def id(self):
        return random.choice(self.value)


if __name__ == '__main__':
    print(Image.CORRECT_ANSWER.id)
    print(Image.CORRECT_ANSWER.id)
