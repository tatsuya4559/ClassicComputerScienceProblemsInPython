from collections import namedtuple

Item = namedtuple("Item", "name weight")


def subsetsum(items, total):
    table = [[False for _ in range(total + 1)] for _ in range(len(items) + 1)]
    table[0][0] = True

    for i in range(1, len(items)):
        item = items[i - 1]
        for t in range(total + 1):
            table[i][t] = table[i - 1][t] or table[i - 1][t - item.weight]

    return {
        cost: any(table[i][cost] for i in range(len(items) + 1))
        for cost in range(total + 1)
    }


if __name__ == "__main__":
    items = [
        Item("飴玉", 2),
        Item("するめいか", 3),
        Item("おせんべい", 3),
        Item("クッキー", 7),
        Item("チョコレート", 11),
        Item("ポテチ", 13),
    ]
    from pprint import pprint

    pprint(subsetsum(items, 30))
