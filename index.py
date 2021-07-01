#!/usr/bin/env python
# coding=utf-8
import random
import sys
import re
import copy


class MineTable:
    tableLength = 8  # 多长多宽
    mineCount = 8  # 多少雷
    cover = '*'  # 未打开
    mine = '#'  # 雷
    allGoodCount = 0  # 多少空格
    openGoodCount = 0  # 已经打开的空格
    answerTable = []  # 扫雷答案表
    flagTable = []  # 扫雷已打开标记表
    resultTable = []  # 上两张表的合成结果表

    def __init__(self):
        # 多少空格
        self.allGoodCount = self.tableLength * self.tableLength - self.mineCount
        # 初始扫雷表
        initTable = [[self.cover for _ in range(self.tableLength)] for _ in range(self.tableLength)]
        # 答案表
        self.answerTable = copy.deepcopy(initTable)
        # 记录打开标记的扫雷图   已经发现的标记为'd'=>'discover
        self.flagTable = copy.deepcopy(initTable)
        # 结果表，这是用来合成结果后展示的
        self.resultTable = copy.deepcopy(initTable)
        # 设置雷区标记,雷区标记为 "#"
        self.getAnswerTable()
        # 雷区答案表,安全区周围雷区数
        self.promptMine()

    # 扫雷表格编号 [ [0,0],[0,1],[1,0],[1,1] ]
    def getTableAddress(self):
        tableAddress = []
        for i in range(self.tableLength):
            for j in range(self.tableLength):
                tableAddress.append([i, j])
        return tableAddress

    # 设置雷区标记,雷区标记为 "#"
    def getAnswerTable(self):
        mines = random.sample(self.getTableAddress(), self.mineCount)
        for address in mines:
            i = address[0]
            j = address[1]
            # 在扫雷初始表中设置雷区
            self.answerTable[i][j] = self.mine

    # 扫雷表各安全区周围雷区数量提示
    def promptMine(self):
        for table_i in range(self.tableLength):
            for table_j in range(self.tableLength):
                # 本格是雷区就跳过
                if self.answerTable[table_i][table_j] == self.mine:
                    continue

                flag = 0
                for around_i in range(-1, 2):
                    for around_j in range(-1, 2):
                        if (around_i == 0) and (around_j == 0):
                            continue
                        find_i = table_i + around_i
                        find_j = table_j + around_j
                        if 0 <= find_i < self.tableLength:
                            if 0 <= find_j < self.tableLength:
                                if self.answerTable[find_i][find_j] == self.mine:
                                    flag = flag + 1
                # 记录本格雷区数
                self.answerTable[table_i][table_j] = str(flag)

    # 展示扫雷表 (用答案表和打开标记表，合成结果表)
    def getNowData(self):
        for i in range(self.tableLength):
            for j in range(self.tableLength):
                # 将已打开的
                if self.flagTable[i][j] == 'd':
                    self.resultTable[i][j] = self.answerTable[i][j]

    def printShow(self):
        self.getNowData()
        print('xy--0----1----2----3----4----5----6----7--')
        for i in range(self.tableLength):
            print(i, self.resultTable[i])
            print('------------------------------------------')
        # 如果全部安全区都打开，就结束
        if self.openGoodCount == self.allGoodCount:
            print('==============success!!!================')
            return 1
        else:
            return 0

    # 已经发现的标记为'd'=>'discover'
    def checkInputAddress(self, i, j):
        # 地址是否合法
        if (not (0 <= i < self.tableLength)) or (not (0 <= j < self.tableLength)):
            return -1
        # 已打开
        if self.flagTable[i][j] == 'd':
            return 0
        # 当前位置有雷
        if self.answerTable[i][j] == self.mine:
            return 2
        # 当前附近有雷
        if self.answerTable[i][j] != '0':
            self.flagTable[i][j] = 'd'
            self.openGoodCount += 1
            return 1
        else:
            # 当前附近无雷
            self.flagTable[i][j] = 'd'
            self.openGoodCount += 1
            self.checkRound(i, j)
            return 1

    # 检查零区周围是否也为零区
    def checkRound(self, table_i, table_j):
        # 检查周围8个格
        for round_i in range(-1, 2):
            for round_j in range(-1, 2):
                # 不用检查自己
                if (round_i == 0) and (round_j == 0):
                    continue
                # 如果要检查的格从没打开
                i = table_i + round_i
                j = table_j + round_j
                if 0 <= i < self.tableLength:
                    if 0 <= j < self.tableLength:
                        if self.flagTable[i][j] != 'd':
                            # 要检查在格也是零区就递归
                            if self.answerTable[i][j] == '0':
                                self.openGoodCount += 1
                                # 先标记它已经被打开
                                self.flagTable[i][j] = 'd'
                                # 递归
                                self.checkRound(i, j)
                            # 要检查的格周围有雷，就仅标记被打开
                            elif self.answerTable[i][j] != self.mine:
                                self.openGoodCount += 1
                                self.flagTable[i][j] = 'd'

    def getLastGood(self):
        return self.allGoodCount - self.openGoodCount

    # 触雷时展示扫雷表，与上面函数不同,它多打开了全部的雷区
    def gameOverMine(self):
        for i in range(self.tableLength):
            for j in range(self.tableLength):
                if self.answerTable[i][j] == self.mine:
                    self.resultTable[i][j] = self.answerTable[i][j]


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
        line, field = eval(line_input)

        # 打开用户指定的表格位置
        result = mt.checkInputAddress(line, field)
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
