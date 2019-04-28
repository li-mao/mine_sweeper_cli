#!/usr/bin/env python
# coding=utf-8
import random
import sys
import re

global table_langth  # 多长多宽
global mine_count  # 多少雷
global good_count  # 多少空格
global now_good  # 已经打开的空格
global answer_table  # 扫雷答案表
global flag_table  # 扫雷已打开标记表
global result_table  # 上两张表的合成结果表

table_langth = 8
mine_count = 8
good_count = table_langth * table_langth - mine_count
now_good = 0
answer_table = []
flag_table = []
result_table = []

# 扫雷表格编号 [ [0,0],[0,1],[1,0],[1,1] ]
def get_mine_number( ):
    global table_langth
    i = 0
    mine_number = []
    while (i < table_langth):
        j = 0
        while (j < table_langth):
            mine_number.append([i, j])
            j += 1
        i += 1
    return mine_number

# 指定雷区所在位置，初始化扫雷表
def get_init_mine_table( init_table, has_mine_table ):
    for index in range(len(has_mine_table)):
        # 获取雷区地址
        mine_i = has_mine_table[index][0]
        mine_j = has_mine_table[index][1]
        # 在扫雷初始表中设置雷区
        new_i_line = init_table[mine_i].copy()
        new_i_line[mine_j] = '#'
        init_table[mine_i] = new_i_line
    return init_table

# 扫雷表各安全区周围雷区数量提示
def prompt_mine(init_table):
    global table_langth
    table_i = 0
    while (table_i < table_langth):
        table_j = 0
        while (table_j < table_langth):
            # 本格是雷区就跳过
            if init_table[table_i][table_j] == '#':
                table_j = table_j + 1
                continue

            flag = 0
            around_i = -1
            while(around_i <= 1):
                around_j = -1
                while(around_j <= 1):
                    if (around_i == 0) and (around_j == 0):
                        around_j = around_j + 1
                        continue
                    find_i = table_i + around_i
                    find_j = table_j + around_j
                    if (0 <= (find_i) < table_langth) and (0 <= (find_j) < table_langth) and (init_table[find_i][find_j] == '#'):
                        flag = flag + 1
                    around_j = around_j + 1
                around_i = around_i + 1

            # 记录本格雷区数
            new_i_line = init_table[table_i].copy()
            new_i_line[table_j] = str(flag)
            init_table[table_i] = new_i_line
            table_j = table_j + 1

        table_i = table_i + 1
    return init_table

# 已经发现的标记为'd'=>'discover'
def check_input_addr(addr, flag_table, answer_table):
    global table_langth
    global now_good
    i = addr[0]
    j = addr[1]

    if (not (0 <= i < table_langth)) or (not (0 <= j < table_langth)):
        return -1
    if init_table[i][j] == 'd':
        return 0
    if answer_table[i][j] == '#':
        return 2

    if answer_table[i][j] != '0':
        new_i_line = flag_table[i].copy()
        new_i_line[j] = 'd'
        flag_table[i] = new_i_line
        now_good += 1
        return 1
    else:
        new_i_line = flag_table[i].copy()
        new_i_line[j] = 'd'
        flag_table[i] = new_i_line
        now_good += 1
        check_round([i, j], flag_table, answer_table)
        return 1

# 检查零区周围是否也为零区
def check_round(addr, flag_table, answer_table):
    global table_langth
    global now_good
    table_i = addr[0]
    table_j = addr[1]
    #检查周围8个格
    around_i = -1
    while (around_i <= 1):
        around_j = -1
        while (around_j <= 1):
            #不用检查自己
            if (around_i == 0) and (around_j == 0):
                around_j = around_j + 1
                continue
            #如果要检查的格从没打开
            find_i = table_i + around_i
            find_j = table_j + around_j
            if (0 <= (find_i) < table_langth) and (0 <= (find_j) < table_langth) and (flag_table[find_i][find_j] != 'd'):
                #要检查在格也是零区就递归
                if answer_table[find_i][find_j] == '0':
                    now_good += 1
                    #先标记它已经被打开
                    change_show_mine_table(find_i, find_j, flag_table)
                    #递归
                    check_round([find_i, find_j], flag_table, answer_table)
                #要检查的格周围有雷，就仅标记被打开
                elif answer_table[find_i][find_j] != '#':
                    now_good += 1
                    change_show_mine_table(find_i, find_j, flag_table)

            around_j = around_j + 1
        around_i = around_i + 1

# 标记该格已被打开
def change_show_mine_table(i, j, flag_table):
    new_i_line = flag_table[i].copy()
    new_i_line[j] = 'd'
    flag_table[i] = new_i_line

# 展示扫雷表 (用答案表和打开标记表，合成结果表)
def print_show(answer_table, flag_table, result_table):
    for index_i in range(len(flag_table)):
        for index_j in range(len(flag_table[index_i])):
            if (flag_table[index_i][index_j] != '*') and (result_table[index_i][index_j] == '*'):
                new_i_line = result_table[index_i].copy()
                new_i_line[index_j] = answer_table[index_i][index_j]
                result_table[index_i] = new_i_line

# 触雷时展示扫雷表，与上面函数不同,它多打开了全部的雷区
def game_over_mine(answer_table, result_table):
    for index_i in range(len(result_table)):
        for index_j in range(len(result_table[index_i])):
            if (answer_table[index_i][index_j] == '#'):
                new_i_line = result_table[index_i].copy()
                new_i_line[index_j] = answer_table[index_i][index_j]
                result_table[index_i] = new_i_line


# 初始扫雷表
init_table = [['*'] * table_langth] * table_langth
# 记录打开标记的扫雷图   已经发现的标记为'd'=>'discover'
flag_table = init_table.copy()
# 结果表，这是用来合成结果后展示的
result_table = init_table.copy()
# 生成雷区位置
mine_number = get_mine_number()
has_mine_table = random.sample(mine_number, mine_count)
# 设置雷区标记,雷区标记为 "#"
init_table = get_init_mine_table(init_table, has_mine_table)
# 雷区答案表,安全区周围雷区数
answer_table = prompt_mine(init_table)

# 游戏开始
while 1:
    # 屏幕上展示扫雷结果图
    print_show(answer_table, flag_table, result_table)
    print('xy--0----1----2----3----4----5----6----7--')
    show_i = 0
    for item in result_table:
        print(show_i, item)
        print('------------------------------------------')
        show_i += 1
        if not (0 <= show_i < table_langth):
            show_i = 0

    # 如果全部安全区都打开，就结束
    if now_good == good_count:
        print('==============success!!!================')
        sys.exit()

    # 提示扫雷信息，并接收用户输入
    last_good = good_count - now_good
    line_input = input('雷区总数：' + str(mine_count) + ' ; 剩余安全区总数: ' + str(last_good) + ' \n(继续游戏输入行列:"x,y"/退出:"gg"): ')
    # 用户要求结束
    if line_input == 'gg':
        sys.exit()
    # 用户继续输入, 先判断输入格式
    if not (re.match(r'^\d+,\d+', line_input)):
        print('输入格式错误，请重试')
        continue
    i, j = eval(line_input)

    # 打开用户指定的表格位置
    result = check_input_addr([i, j], flag_table, answer_table)
    if result == -1:
        print('地址错误')
    elif result == 0:
        print('正在展示结果')
    elif result == 2:
        print('--------------game over-----------------')
        game_over_mine(answer_table, result_table)
        for item in result_table:
            print(item)
            print('----------------------------------------')
        sys.exit()
