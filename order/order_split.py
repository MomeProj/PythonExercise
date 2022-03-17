# 平均拆單 N張 拆M次

import sys

from threading import main_thread

from black import main


def order_split(number, count, max_split):
    print(f"input: number:{number} count: {count}")
    ret = []
    # number 量
    # count 次
    # sum = 0
    sum = count / 2
    # sum = count - 1
    nn = 0
    for i in range(count):
        sum += number
        # print(f"sum1 {sum}")
        while (sum >= count):
            sum -= count
            # print(f"sum2 {sum}")
            nn += 1

        if (nn > max_split):
            return []

        ret.append(nn)
        nn = 0
    return ret


if __name__ == "__main__":
    ret = order_split(1000, 2, 499)
    sum = 0
    index = 0
    for i in ret:
        index += 1
        print(f"{index}. num: {i} sum: {sum}")
        sum += i

    print(f"sum: {sum}")
