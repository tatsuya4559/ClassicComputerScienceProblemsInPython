from collections import namedtuple
from pprint import pprint

Item = namedtuple("Item", "name weight value")


def knapsack(items, max_capacity):
    table = [[0.0 for _ in range(max_capacity + 1)] for _ in range(len(items) + 1)]

    for i, item in enumerate(items):
        for capacity in range(1, max_capacity + 1):
            previous_items_value = table[i][capacity]
            if capacity >= item.weight:
                value_freeing_weight_for_item = table[i][capacity - item.weight]
                table[i + 1][capacity] = max(
                    value_freeing_weight_for_item + item.value, previous_items_value
                )
            else:
                table[i + 1][capacity] = previous_items_value
    solution = []
    capacity = max_capacity
    for i in range(len(items), 0, -1):
        if table[i - 1][capacity] != table[i][capacity]:
            solution.append(items[i - 1])
            capacity -= items[i - 1].weight
    return solution


if __name__ == "__main__":
    items = [
        Item("TV", 50, 500),
        Item("燭台", 2, 300),
        Item("ステレオ", 35, 400),
        Item("PC", 3, 1000),
        Item("食料", 15, 50),
        Item("服", 20, 800),
        Item("宝石", 1, 4000),
        Item("本", 100, 300),
        Item("プリンタ", 18, 30),
        Item("冷蔵庫", 200, 700),
        Item("絵画", 10, 1000),
    ]
    print(f'value: {sum(item.value for item in items)}')
    print(f'weight: {sum(item.weight for item in items)}')
    solution = knapsack(items, 75)
    pprint(solution)
    print(f'value: {sum(item.value for item in solution)}')
    print(f'weight: {sum(item.weight for item in solution)}')
