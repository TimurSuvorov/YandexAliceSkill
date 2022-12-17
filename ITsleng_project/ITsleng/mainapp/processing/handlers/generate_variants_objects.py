import random


def generate_var_buttons(question_variants) -> list:
    buttons_list = []

    for var in question_variants:
        buttons_list.append({'title': f'⚡{var.capitalize().replace("+", "")}', 'hide': 'true'})
        random.shuffle(buttons_list)
    buttons_list.append({'title': "🤔Сдаюсь!", 'hide': 'true'})
    return buttons_list


def generate_var_string(question_variants: list) -> str:
    random.shuffle(question_variants)
    buttons_str = "•   " + "\n•   ".join(question_variants)
    return buttons_str


if __name__ == '__main__':
    f = generate_var_buttons(['окиара', 'таска', 'фича'])
    print(f)

    l = generate_var_string(['окиара', 'таска', 'фича'])
    print(l)