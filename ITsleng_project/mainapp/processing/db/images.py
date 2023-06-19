import random
from enum import Enum


class Image(Enum):
    # Приветствие.
    HI = [
        '213044/fff44481883c826a21fa'
    ]
    # Вызов "Правила".
    RULES = [
        '1540737/2b8ec31e4b8f202fb100',
    ]
    # Вызов "Что умеешь?".
    ABOUT = [
        '1030494/c07043a8a3d8be4ad1a0',
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
        '213044/41a35abdf0734a8ca717',
        '1540737/43c2686d6d6c6b88b46b',
    ]
    # Вызов рейтинга.
    RATING = [
        '1030494/0fe6f908f175e997963e',
    ]

    # Вне сценария.
    OFF_SCRIPT = [
        '1030494/671b06307e6ddeeb6d68',
        '213044/36ef29ba4c91fb135182',
    ]
    # Нецензурная речь.
    OBSCENE = [
        '965417/923020dc485a94343b9b',
        '1652229/d3e21339a40877fdb79f',
    ]

    @property
    def id(self):
        return random.choice(self.value)


if __name__ == '__main__':
    print(Image.CORRECT_ANSWER.id)
    print(Image.CORRECT_ANSWER.id)
