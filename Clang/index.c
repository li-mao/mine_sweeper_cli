#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void mkBottomArr(char mineTable[], int length, int width, char defaultMark);

void mkRandArr(int arr[], int total, int length, int current);

int cmpFn (const void * a, const void * b);

int main() {
    int const length = 10;
    char bottomArr[length * length];
    mkBottomArr(bottomArr, length, length, '-');
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < length; j++) {
            printf(" %c  ", bottomArr[i * length + j]);
        }
        printf("\n");
    }

    return 0;
}

/**
 * 雷区底本图
 * @param mineTable 雷区数组
 * @param length 长
 * @param width 宽
 * @param c 显示符号（非雷）
 */
void mkBottomArr(char mineTable[], int length, int width, char defaultMark) {
    int const mineNum = length*3;
    int randArr[mineNum];
    mkRandArr(randArr, mineNum, length * width, 0);
    qsort(randArr, mineNum, sizeof(int), cmpFn);
    for (int i = 0; i < mineNum; i++) {
        printf("%d  ", randArr[i]);
        if (((i + 1) % length)) {
        } else {
            printf("\n");
        }
    }
    printf("\n");

    int nowRandPtr = 0;
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < width; j++) {
            if((i *length +j) == randArr[nowRandPtr]){
                mineTable[i * length + j] = 'X';
                nowRandPtr ++;
            }else{
                mineTable[i * length + j] = defaultMark;
            }
        }
    }
}

/**
 * 随机雷区
 * @param arr  全部雷的地址（数组）
 * @param total 总雷数
 * @param length 二维图长度
 * @param current 当前生成的第n个雷
 */
void mkRandArr(int arr[], int total, int length, int current) {
    time_t t;
    srand((unsigned) time(&t) + current);
    int r = rand() % length;
    int flagExist = 0;
    for (int i = 0; i < current; i++) {
        if (arr[i] == r) {
            flagExist = 1;
            break;
        }
    }

    if (current >= total) {
        return;
    } else {
        int newCurrent = current;
        if (!flagExist) {
            arr[current] = r;
            newCurrent = newCurrent + 1;
        }
        return mkRandArr(arr, total, length, newCurrent);
    }
}

/**
 * 排序函数，从小到大
 * @param a
 * @param b
 * @return
 */
int cmpFn (const void * a, const void * b){
    const int *aa = a;
    const int *bb = b;
    return (*aa > *bb) - (*aa < *bb);
}

char countMineWithHere(int *arr, int side, int index) {
    int count = 0;
    int x = index % side;
    int y = index / side;
    if (arr[index] == 'X') {
        return 'X';
    } else {
        int index_11 = (x - 1) + (y - 1) * side;
        if ((index_11 >= 0) && (arr[index_11] == 'X')) {
            count++;
        }
        int index_12 = (x - 1) + y * side;
        if ((index_12 >= 0) && (arr[index_12] == 'X')) {
            count++;
        }
        int index_13 = (x - 1) + (y + 1) * side;
        if ((index_13 >= 0) && (arr[index_13] == 'X')) {
            count++;
        }
        int index_21 = x + (y - 1) * side;
        if ((index_21 >= 0) && (arr[index_21] == 'X')) {
            count++;
        }
        int index_23 = x + (y + 1) * side;
        if ((index_23 >= 0) && (arr[index_23] == 'X')) {
            count++;
        }
        int index_31 = (x + 1) + (y - 1) * side;
        if ((index_31 >= 0) && (arr[index_31] == 'X')) {
            count++;
        }
        int index_32 = (x + 1) + y * side;
        if ((index_32 >= 0) && (arr[index_32] == 'X')) {
            count++;
        }
        int index_33 = (x + 1) + (y + 1) * side;
        if ((index_33 >= 0) && (arr[index_33] == 'X')) {
            count++;
        }
        return (char) count;
    }
}