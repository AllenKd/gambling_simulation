
def sol(m, n):
    r = m
    for i in range(m+1, n+1):
        r ^= i
    return r


if __name__ == '__main__':
    print(sol(5, 8))