def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    return newfunc


def multiply(x, y):
    print(x * y)


multiply_by_two = partial(multiply, 2)
multiply_by_two(6)