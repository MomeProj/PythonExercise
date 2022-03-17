# 平均拆單 N張 拆M次

import sys


def order_split(number, count, max_split):
    """
        input: number 量
        input: count 次
        output: array
    """
    print(f"input: number:{number} count: {count}")
    ret = []

    # sum = 0          # 前序
    sum = count / 2    # 中序
    # sum = count - 1  # 後序
    nn = 0
    for i in range(count):
        sum += number
        # print(f"sum1 {sum}")
        while (sum >= count):
            sum -= count
            # print(f"sum2 {sum}")
            nn += 1

        if (nn > max_split):
            # 超過最大分拆值
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
    sys.exit(0)
