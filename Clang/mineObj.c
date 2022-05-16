#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "mineObj.h"

/**
 * @brief 初始化 mineObj
 * 
 * @param x 
 * @param y 
 * @return mineObj* 
 */
mineObj* init(int x, int y){
    // 申请mine数组
    mineCell* mineMap = (mineCell*)malloc(sizeof(mineCell)*x*y);
    for(int i=0; i<x*y; i++){
        (mineMap+i)->outer = '*'; // *: 未打开， O: 已打开
        (mineMap+i)->inner = ' '; // ' ': 周围无雷， 1-5: 周围雷数， M: 雷
    }
    // 申请mineObj对象
    mineObj* myMineObj = (mineObj*)malloc(sizeof(mineObj));
    myMineObj->mineMap = mineMap;
    myMineObj->x = x;
    myMineObj->y = y;
    myMineObj->makeRandMine = makeRandMine;
    myMineObj->showInner = showInner;
    myMineObj->showOuter = showOuter;
    myMineObj->showOpen = showOpen;
    myMineObj->showFail = showFail;
    myMineObj->showTest = showTest;
    myMineObj->openXY = openXY;
    myMineObj->getXY = getXY;
    myMineObj->cellCountRound = cellCountRound;
    myMineObj->cellHint = cellHint;

    myMineObj->makeRandMine(myMineObj, x*y, x, 0);
    myMineObj->cellHint(myMineObj);

    return myMineObj;
}

 /**
  * 生成雷地址
  * @param mineMap
  * @param mapLength
  * @param mineMax
  * @param current
  */
void makeRandMine(mineObj* self, int mapLength, int mineMax, int current) {
    time_t t;
    srand((unsigned) time(&t) + current);
    int r = rand() % mapLength;

    if ((self->mineMap+r)->inner != 'M') {
        (self->mineMap+r)->inner = 'M';
        current++; 
        if (current >= mineMax) {
            return;
        }
    }

    return makeRandMine(self, mapLength, mineMax, current);
}

/**
 * 该地方是否有雷
 * @param self
 * @param x
 * @param y
 * @return  0 1
 */
int getXY(mineObj* self, int x, int y){
    if( x < 0 || x > self->x){
        return 0;
    }
    if( y < 0 || y > self->y){
        return 0;
    }
    return (self->mineMap + (self->y * x + y))->inner == 'M';
}

char cellCountRound(mineObj* self, int x, int y){
    int count = 0;
    char countChar[2];

    if(x-1 >= 0){
        count += y-1 >=0 ?       (self->mineMap + self->y * (x-1) + y-1)->inner == 'M' : 0;
        count +=                 (self->mineMap + self->y * (x-1) + y)->inner == 'M';
        count += y+1 < self->y ? (self->mineMap + self->y * (x-1) + y+1)->inner == 'M' : 0;
    }

    count += y-1 >= 0 ?      (self->mineMap + self->y * (x) + y-1)->inner == 'M' : 0;
    count += y+1 < self->y ? (self->mineMap + self->y * (x) + y+1)->inner == 'M' : 0;

    if(x+1 < self->x){
        count += y-1 >= 0 ?      (self->mineMap + self->y * (x+1) + y-1)->inner == 'M' : 0;
        count +=                 (self->mineMap + self->y * (x+1) + y)->inner == 'M';
        count += y+1 < self->y ? (self->mineMap + self->y * (x+1) + y+1)->inner == 'M': 0;

    }

    sprintf(countChar, "%d" , count);
    return countChar[0];
}

void cellHint(mineObj* self){
    for(int x= 0; x < self->x; x++){
        for(int y=0; y < self->y; y++){
            if((self->mineMap + (self->y * x + y))->inner != 'M'){
                char result =  self->cellCountRound(self, x, y);
                (self->mineMap + (self->y * x + y))-> inner = result;
            }
        }
    }
}

//void openRound(mineObj* self, int x, int y){
//
//}



/**
 * @brief 展示底层地图
 * 
 * @param self 
 */
void showInner(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mineMap + i)->inner);
    }
}

/**
 * @brief 展示外部地图
 * 
 * @param self 
 */
void showOuter(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mineMap + i)->outer);
    }
}

void showOpen(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mineMap + i)->outer == '*' ? (self->mineMap + i)->outer: (self->mineMap + i)->inner);
    }
}

void showFail(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mineMap + i)->inner == 'M'
                        ? 'm'
                        : (self->mineMap + i)->outer == '*'
                            ? (self->mineMap + i)->outer
                            : (self->mineMap + i)->inner );
    }
}

void showTest(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mineMap + i)->inner == 'M' ? (self->mineMap + i)->inner: (self->mineMap + i)->outer);
    }
}

void openXY(mineObj* self, int x, int y){
    (self->mineMap + (self->y * x + y))->outer = 'O';
}


