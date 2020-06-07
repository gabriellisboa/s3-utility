def bytesto(bytes, to, bsize=1024):
    scale = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    result = float(bytes)

    for i in range(scale[to]):
        result = result / bsize

    return(result)
