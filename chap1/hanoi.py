from collections import deque


def hanoi(begin, end, tmp, n):
    if n == 1:
        end.append(begin.pop())
    else:
        hanoi(begin, tmp, end, n - 1)
        hanoi(begin, end, tmp, 1)
        hanoi(tmp, end, begin, n - 1)


def main():
    num_discs = 10
    tower_a = deque()
    tower_b = deque()
    tower_c = deque()

    for i in range(1, num_discs + 1):
        tower_a.append(i)

    print(tower_a, tower_b, tower_c)
    hanoi(tower_a, tower_c, tower_b, num_discs)
    print(tower_a, tower_b, tower_c)


if __name__ == '__main__':
    main()
