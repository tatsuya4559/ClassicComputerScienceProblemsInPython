import functools


# 再帰は性能問題があるからメモ化する
memo = {0: 0, 1: 1}


def fib2(x):
    if x not in memo:
        memo[x] = fib2(x - 1) + fib2(x - 2)
    return memo[x]


# lru_cacheでメモ化を自動で行ってくれる
@functools.lru_cache(maxsize=None)
def fib3(x):
    if x < 2:
        return x
    else:
        return fib3(x - 1) + fib3(x - 2)


# すべての再帰はループになる
# 実は一番効率がいい
def fib5(x):
    if x == 0:
        return x
    last = 0
    next = 1
    for _ in range(1, x):
        last, next = next, last + next
    return next
