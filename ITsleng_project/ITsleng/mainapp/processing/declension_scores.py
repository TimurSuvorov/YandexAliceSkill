def decl_scores(score):
    d = score%10
    h = score%100
    if d == 1 and h != 11:
        s = ""
    elif 1 < d < 5 and not 11 < h < 15:
        s = "а"
    else:
        s = "ов"
    return f'{score} балл{s}'


if __name__  ==  '__main__':
    for i in range(0, 100):
        r = decl_scores(i)
        print(r)
