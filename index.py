#!/usr/bin/env python
# coding=utf-8
import random
import sys
import re

global langth  # 多长多宽
global mine_count  # 多少雷
global good_count  # 多少空格
global now_good  # 已经打开的空格
global mine_table  # 扫雷答案表
global show_mine_table  # 扫雷已打开标记表
global result_mine_table  # 扫雷展示表

langth = 8
mine_count = 8
good_count = langth * langth - mine_count
now_good = 0
mine_table = []
show_mine_table = []
result_mine_table = []


# 扫雷表格编号 [ [0,0],[0,1],[1,0],[1,1] ]
def get_mine_number():
    global langth
    i = 0
    mine_number = []
    while (i < langth):
        j = 0
        while (j < langth):
            mine_number.append([i, j])
            j += 1
        i += 1
    return mine_number


# 指定雷区，初始化扫雷表
def get_init_mine_table(init_mine_table, has_mine_table):
    for index in range(len(has_mine_table)):
        # 获取雷区地址
        mine_i = has_mine_table[index][0]
        mine_j = has_mine_table[index][1]
        # 在扫雷初始表中设置雷区
        new_i_line = init_mine_table[mine_i].copy()
        new_i_line[mine_j] = '#'
        init_mine_table[mine_i] = new_i_line
    return init_mine_table


# 雷区数量提示
def prompt_mine(init_mine_table):
    global langth
    i = 0
    while (i < langth):
        j = 0
        while (j < langth):
            # 本格是雷区就跳过
            if init_mine_table[i][j] == '#':
                j = j + 1
                continue

            flag = 0

            # around_row_i = -1
            # 本格上一行雷区数量
            if (0 <= (i - 1) < langth):
                if (0 <= (j - 1) < langth) and (init_mine_table[i - 1][j - 1] == '#'):
                    flag = flag + 1
                if (init_mine_table[i - 1][j] == '#'):
                    flag = flag + 1
                if (0 <= (j + 1) < langth) and (init_mine_table[i - 1][j + 1] == '#'):
                    flag = flag + 1

                    # 本格本行雷区数量
            if (0 <= (j - 1) < langth) and (init_mine_table[i][j - 1] == '#'):
                flag = flag + 1
            if (0 <= (j + 1) < langth) and (init_mine_table[i][j + 1] == '#'):
                flag = flag + 1

                # 本格下一行雷区数量
            if (0 <= (i + 1) < langth):
                if (0 <= (j - 1) < langth) and (init_mine_table[i + 1][j - 1] == '#'):
                    flag = flag + 1
                if (init_mine_table[i + 1][j] == '#'):
                    flag = flag + 1
                if (0 <= (j + 1) < langth) and (init_mine_table[i + 1][j + 1] == '#'):
                    flag = flag + 1

                    # 记录本格雷区数
            new_i_line = init_mine_table[i].copy()
            new_i_line[j] = str(flag)
            init_mine_table[i] = new_i_line
            j = j + 1

        i = i + 1
    return init_mine_table


# 已经发现的标记为'd'=>'discover'
def check_input_addr(addr, show_mine_table, mine_table):
    global langth
    global now_good
    i = addr[0]
    j = addr[1]

    if (not (0 <= i < langth)) or (not (0 <= j < langth)):
        return -1

    if init_mine_table[i][j] == 'd':
        return 0

    if mine_table[i][j] == '#':
        return 2

    if mine_table[i][j] != '0':
        new_i_line = show_mine_table[i].copy()
        new_i_line[j] = 'd'
        show_mine_table[i] = new_i_line
        now_good += 1
        return 1
    else:
        new_i_line = show_mine_table[i].copy()
        new_i_line[j] = 'd'
        show_mine_table[i] = new_i_line
        now_good += 1
        check_round([i, j], show_mine_table, mine_table)
        return 1


# 检查零区周围是否也为零区
def check_round(addr, show_mine_table, mine_table):
    global langth
    global now_good
    i = addr[0]
    j = addr[1]

    if (0 <= (i - 1) < langth):
        if (0 <= (j - 1) < langth) and (show_mine_table[i - 1][j - 1] != 'd'):
            if mine_table[i - 1][j - 1] == '0':
                now_good += 1
                change_show_mine_table(i - 1, j - 1, show_mine_table)
                check_round([i - 1, j - 1], show_mine_table, mine_table)
            elif mine_table[i - 1][j - 1] != '#':
                now_good += 1
                change_show_mine_table(i - 1, j - 1, show_mine_table)

        if (show_mine_table[i - 1][j] != 'd'):
            if mine_table[i - 1][j] == '0':
                now_good += 1
                change_show_mine_table(i - 1, j, show_mine_table)
                check_round([i - 1, j], show_mine_table, mine_table)
            elif mine_table[i - 1][j] != '#':
                now_good += 1
                change_show_mine_table(i - 1, j, show_mine_table)

        if (0 <= (j + 1) < langth) and (show_mine_table[i - 1][j + 1] != 'd'):
            if mine_table[i - 1][j + 1] == '0':
                now_good += 1
                change_show_mine_table(i - 1, j + 1, show_mine_table)
                check_round([i - 1, j + 1], show_mine_table, mine_table)
            elif mine_table[i - 1][j + 1] != '#':
                now_good += 1
                change_show_mine_table(i - 1, j + 1, show_mine_table)

    if (0 <= (j - 1) < langth) and (show_mine_table[i][j - 1] != 'd'):
        if mine_table[i][j - 1] == '0':
            now_good += 1
            change_show_mine_table(i, j - 1, show_mine_table)
            check_round([i, j - 1], show_mine_table, mine_table)
        elif mine_table[i][j - 1] != '#':
            now_good += 1
            change_show_mine_table(i, j - 1, show_mine_table)

    if (0 <= (j + 1) < langth) and (show_mine_table[i][j + 1] != 'd'):
        if mine_table[i][j + 1] == '0':
            now_good += 1
            change_show_mine_table(i, j + 1, show_mine_table)
            check_round([i, j + 1], show_mine_table, mine_table)
        elif mine_table[i][j + 1] != '#':
            now_good += 1
            change_show_mine_table(i, j + 1, show_mine_table)

    if (0 <= (i + 1) < langth):
        if (0 <= (j - 1) < langth) and (show_mine_table[i + 1][j - 1] != 'd'):
            if mine_table[i + 1][j - 1] == '0':
                now_good += 1
                change_show_mine_table(i + 1, j - 1, show_mine_table)
                check_round([i + 1, j - 1], show_mine_table, mine_table)
            elif mine_table[i + 1][j - 1] != '#':
                now_good += 1
                change_show_mine_table(i + 1, j - 1, show_mine_table)

        if (show_mine_table[i + 1][j] != 'd'):
            if mine_table[i + 1][j] == '0':
                now_good += 1
                change_show_mine_table(i + 1, j, show_mine_table)
                check_round([i + 1, j], show_mine_table, mine_table)
            elif mine_table[i + 1][j] != '#':
                now_good += 1
                change_show_mine_table(i + 1, j, show_mine_table)

        if (0 <= (j + 1) < langth) and (show_mine_table[i + 1][j + 1] != 'd'):
            if mine_table[i + 1][j + 1] == '0':
                now_good += 1
                change_show_mine_table(i + 1, j + 1, show_mine_table)
                check_round([i + 1, j + 1], show_mine_table, mine_table)
            elif mine_table[i + 1][j + 1] != '#':
                now_good += 1
                change_show_mine_table(i + 1, j + 1, show_mine_table)


def change_show_mine_table(i, j, show_mine_table):
    new_i_line = show_mine_table[i].copy()
    new_i_line[j] = 'd'
    show_mine_table[i] = new_i_line


def print_show(mine_table, show_mine_table, result_mine_table):
    for index_i in range(len(show_mine_table)):
        for index_j in range(len(show_mine_table[index_i])):
            if (show_mine_table[index_i][index_j] != '*') and (result_mine_table[index_i][index_j] == '*'):
                new_i_line = result_mine_table[index_i].copy()
                new_i_line[index_j] = mine_table[index_i][index_j]
                result_mine_table[index_i] = new_i_line


def game_over_mine(mine_table, result_mine_table):
    for index_i in range(len(result_mine_table)):
        for index_j in range(len(result_mine_table[index_i])):
            if (mine_table[index_i][index_j] == '#'):
                new_i_line = result_mine_table[index_i].copy()
                new_i_line[index_j] = mine_table[index_i][index_j]
                result_mine_table[index_i] = new_i_line


init_mine_table = [['*'] * langth] * langth

# 展示用的扫雷图   已经发现的标记为'd'=>'discover'
show_mine_table = init_mine_table.copy()

mine_number = get_mine_number()
has_mine_table = random.sample(mine_number, mine_count)
init_mine_table = get_init_mine_table(init_mine_table, has_mine_table)
mine_table = prompt_mine(init_mine_table)

result_mine_table = show_mine_table.copy()
while 1:
    print_show(mine_table, show_mine_table, result_mine_table)
    print('xy--0----1----2----3----4----5----6----7--')
    show_i = 0
    for item in result_mine_table:
        print(show_i, item)
        print('------------------------------------------')
        show_i += 1
        if not (0 <= show_i < langth):
            show_i = 0

    if now_good == good_count:
        print('==============success!!!================')
        sys.exit()

    last_good = good_count - now_good
    line_input = input('还剩' + str(last_good) + '个空格\n(继续游戏输入行列:"x,y"/退出:"gg"): ')
    if line_input == 'gg':
        sys.exit()

    if not (re.match(r'^\d+,\d+', line_input)):
        print('输入格式错误，请重试')
        continue

    i, j = eval(line_input)

    result = check_input_addr([i, j], show_mine_table, mine_table)
    if result == -1:
        print('地址错误')
    elif result == 0:
        print('正在展示结果')
    elif result == 2:
        print('--------------game over-----------------')
        game_over_mine(mine_table, result_mine_table)
        for item in result_mine_table:
            print(item)
            print('----------------------------------------')
        sys.exit()
