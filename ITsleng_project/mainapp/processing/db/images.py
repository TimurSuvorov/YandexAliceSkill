import random
from enum import Enum


class Image(Enum):
    # Приветствие.
    HI = [
        '213044/fff44481883c826a21fa'
    ]
    # Вызов "Правила".
    RULES = [
        '965417/9699f16cb9389e6860cd',
    ]
    # Вызов "Что умеешь?".
    ABOUT = [
        '1652229/5d13ee4c8153687b2dff',
    ]
    # Выход из игры.
    BYE = [
        '1652229/b460df3074f4dcc64689',
        '1540737/b7ab90b44796985ab8a5',
    ]
    # Запрос на повторение
    REPEAT = [
        '1533899/d195db9c2c39144e4206'
    ]
    # Новый/первый вопрос.
    NEW_QUEST = [
        '1652229/a027800396eea7abecf8',
        '1540737/be328c04042e4c812064',
    ]
    # Верный ответ.
    CORRECT_ANSWER = [
        '1521359/dfc00b8abf99f1c43d74',
        '997614/b7a9cf472550d196b95d',
        '1521359/25e45a3b5cdacdf3cfae',
    ]
    # Неверный ответ. Попытка 1.
    WRONG_ANSWER_1 = [
        '937455/5d4a7fd816dab38588c5',
    ]
    # Неверный ответ. Попытка 2.
    WRONG_ANSWER_2 = [
        '1540737/83ebeaa55120527664f0',
        '1030494/da284a60f203f9773b73',
        '997614/533b7dd542123dd74ffc',
    ]
    # Сдался или пропустил.
    GAVEUP = [
        '213044/fe41341d0749761c8b8a',
        '1540737/8a6fc598972077f4917d',
    ]
    # Вызов рейтинга.
    RATING = [
        '',
    ]

    # Вне сценария.
    OFF_SCRIPT = [
        '1652229/0688870c8bbf71921c3b',
    ]
    # Нецензурная речь.
    OBSCENE = [
        '997614/2a57a38b8a44321c0a58',
        '1030494/7eb8aa6998b31a401907',
    ]

    @property
    def id(self):
        return random.choice(self.value)


if __name__ == '__main__':
    print(Image.CORRECT_ANSWER.id)
    print(Image.CORRECT_ANSWER.id)
