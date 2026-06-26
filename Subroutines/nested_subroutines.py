def First(p1, p2, p3):
    v1 = p2 + p3
    print(Second(v1, p1))

def Second(p1, p2):
    v1 = p1 + p2
    if v1 > 12:
        v1 = v1 + Third(p1)
    return v1

def Third(p1):
    if p1 > 3:
        return 2
    else:
        return 0

print(First(3,4,8))
