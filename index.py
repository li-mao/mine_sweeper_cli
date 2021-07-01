#!/usr/bin/env python
# coding=utf-8
import random
import sys
import re


class MineTable:
    tableLength = 8  # 多长多宽
    mineCount = 8  # 多少雷
    mineNumber = []  # 扫雷表格编号
    noOpen = '*'
    sign = '#'
    initTable = []  # 初始扫雷表
    goodCount = 0  # 多少空格
    nowGood = 0  # 已经打开的空格
    flagTable = []  # 扫雷已打开标记表
    resultTable = []  # 上两张表的合成结果表
    answerTable = []  # 扫雷答案表

    def __init__(self):
        # 初始扫雷表
        self.initTable = [[self.noOpen] * self.tableLength] * self.tableLength
        # 多少空格
        self.goodCount = self.tableLength * self.tableLength - self.mineCount
        # 记录打开标记的扫雷图   已经发现的标记为'd'=>'discover
        self.flagTable = self.initTable.copy()
        # 结果表，这是用来合成结果后展示的
        self.resultTable = self.initTable.copy()
        # 生成雷区位置
        self.getMineNumber()
        # 设置雷区标记,雷区标记为 "#"
        self.getInitMineTable()
        # 雷区答案表,安全区周围雷区数
        self.promptMine()

    # 扫雷表格编号 [ [0,0],[0,1],[1,0],[1,1] ]
    def getMineNumber(self):
        for _i in range(self.tableLength - 1):
            for _j in range(self.tableLength - 1):
                self.mineNumber.append([_i, _j])

    def getInitMineTable(self):
        _has_mine_table = random.sample(self.mineNumber, self.mineCount)
        for _i in range(len(_has_mine_table)):
            # 获取雷区地址
            mine_i = _has_mine_table[_i][0]
            mine_j = _has_mine_table[_i][1]
            # 在扫雷初始表中设置雷区
            new_i_line = self.initTable[mine_i].copy()
            new_i_line[mine_j] = self.sign
            self.initTable[mine_i] = new_i_line

    # 扫雷表各安全区周围雷区数量提示
    def promptMine(self):
        self.answerTable = self.initTable.copy()
        for table_i in range(self.tableLength - 1):
            for table_j in range(self.tableLength - 1):
                # 本格是雷区就跳过
                if self.answerTable[table_i][table_j] == self.sign:
                    continue

                flag = 0
                for around_i in range(-1, 1):
                    for around_j in range(-1, 1):
                        if (around_i == 0) and (around_j == 0):
                            continue
                        find_i = table_i + around_i
                        find_j = table_j + around_j
                        if (0 <= find_i < self.tableLength) and (0 <= find_j < self.tableLength) and (
                                self.answerTable[find_i][find_j] == self.sign):
                            flag = flag + 1
                # 记录本格雷区数
                new_i_line = self.answerTable[table_i].copy()
                new_i_line[table_j] = str(flag)
                self.answerTable[table_i] = new_i_line

    # 展示扫雷表 (用答案表和打开标记表，合成结果表)
    def getNowData(self):
        for _i in range(len(self.flagTable)):
            for _j in range(len(self.flagTable[_i])):
                if (self.flagTable[_i][_j] != self.noOpen) and (self.resultTable[_i][_j] == self.noOpen):
                    new_i_line = self.resultTable[_i].copy()
                    new_i_line[_j] = self.answerTable[_i][_j]
                    self.resultTable[_i] = new_i_line

    def printShow(self):
        self.getNowData()
        print('xy--0----1----2----3----4----5----6----7--')
        show_i = 0
        for _i in self.resultTable:
            print(show_i, _i)
            print('------------------------------------------')
            show_i += 1
            if not (0 <= show_i < self.tableLength):
                show_i = 0

        # 如果全部安全区都打开，就结束
        if self.nowGood == self.goodCount:
            print('==============success!!!================')
            return 1
        else:
            return 0

    # 触雷时展示扫雷表，与上面函数不同,它多打开了全部的雷区
    def gameOverMine(self):
        for _i in range(len(self.resultTable)):
            for _j in range(len(self.resultTable[_i])):
                if self.answerTable[_i][_j] == self.sign:
                    new_i_line = self.resultTable[_i].copy()
                    new_i_line[_j] = self.answerTable[_i][_j]
                    self.resultTable[_i] = new_i_line

    # 已经发现的标记为'd'=>'discover'
    def checkInputAddress(self, address):
        _i = address[0]
        _j = address[1]

        if (not (0 <= _i < self.tableLength)) or (not (0 <= _j < self.tableLength)):
            return -1
        if self.initTable[_i][_j] == 'd':
            return 0
        if self.answerTable[_i][_j] == self.sign:
            return 2

        if self.answerTable[_i][_j] != '0':
            new_i_line = self.flagTable[_i].copy()
            new_i_line[_j] = 'd'
            self.flagTable[_i] = new_i_line
            self.nowGood += 1
            return 1
        else:
            new_i_line = self.flagTable[_i].copy()
            new_i_line[_j] = 'd'
            self.flagTable[_i] = new_i_line
            self.nowGood += 1
            self.checkRound([_i, _j])
            return 1

    # 检查零区周围是否也为零区
    def checkRound(self, address):
        table_i = address[0]
        table_j = address[1]
        # 检查周围8个格
        for _i in range(-1, 1):
            for _j in range(-1, 1):
                # 不用检查自己
                if (_i == 0) and (_j == 0):
                    continue
                # 如果要检查的格从没打开
                find_i = table_i + _i
                find_j = table_j + _j
                if (0 <= find_i < self.tableLength) and (0 <= find_j < self.tableLength) and (
                        self.flagTable[find_i][find_j] != 'd'):
                    # 要检查在格也是零区就递归
                    if self.answerTable[find_i][find_j] == '0':
                        self.nowGood += 1
                        # 先标记它已经被打开
                        self.changeShowMineTable([find_i, find_j])
                        # 递归
                        self.checkRound([find_i, find_j])
                    # 要检查的格周围有雷，就仅标记被打开
                    elif self.answerTable[find_i][find_j] != self.sign:
                        self.nowGood += 1
                        self.changeShowMineTable([find_i, find_j])

    # 标记该格已被打开
    def changeShowMineTable(self, address):
        _i = address[0]
        _j = address[1]
        new_i_line = self.flagTable[_i].copy()
        new_i_line[_j] = 'd'
        self.flagTable[i] = new_i_line

    def getLastGood(self):
        return self.goodCount - self.nowGood


if __name__ == "__main__":
    mt = MineTable()

    # 游戏开始
    while 1:
        # 屏幕上展示扫雷结果图
        if mt.printShow():
            sys.exit()

        # 提示扫雷信息，并接收用户输入
        line_input = input(
            '雷区总数：' + str(mt.mineCount) + ' ; 剩余安全区总数: ' + str(mt.getLastGood()) + ' \n(继续游戏输入行列:"x,y"/退出:"gg"): ')
        # 用户要求结束
        if line_input == 'gg':
            sys.exit()

        # 用户继续输入, 先判断输入格式
        if not (re.match(r'^\d+,\d+', line_input)):
            print('输入格式错误，请重试')
            continue
        i, j = eval(line_input)

        # 打开用户指定的表格位置
        result = mt.checkInputAddress([i, j])
        if result == -1:
            print('地址错误')
        elif result == 0:
            print('正在展示结果')
        elif result == 2:
            print('--------------game over-----------------')
            mt.gameOverMine()
            for item in mt.resultTable:
                print(item)
                print('----------------------------------------')
            sys.exit()
