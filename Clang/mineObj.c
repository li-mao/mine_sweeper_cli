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
    makeRandMine(mineMap, x*y, x, 0);

    // 申请mineObj对象
    mineObj* myMineObj = (mineObj*)malloc(sizeof(mineObj));
    myMineObj->mineMap = mineMap;
    myMineObj->x = x;
    myMineObj->y = y;
    myMineObj->showInner = showInner;
    myMineObj->showOuter = showOuter;
    myMineObj->showOpen = showOpen;
    myMineObj->showFail = showFail;
    myMineObj->showTest = showTest;
    myMineObj->openXY = openXY;
    myMineObj->getXY = getXY;

    return myMineObj;
}

 /**
  * 生成雷地址
  * @param mineMap
  * @param mapLength
  * @param mineMax
  * @param current
  */
void makeRandMine(mineCell* mineMap, int mapLength, int mineMax, int current) {
    time_t t;
    srand((unsigned) time(&t) + current);
    int r = rand() % mapLength;

    if ((mineMap+r)->inner != 'M') {
        (mineMap+r)->inner = 'M';
        current++; 
        if (current >= mineMax) {
            return;
        }
    }

    return makeRandMine(mineMap, mapLength, mineMax, current);
}

/**
 * 该地方是否有雷
 * @param self
 * @param x
 * @param y
 * @return  0 1
 */
int getXY(mineObj* self, int x, int y){
    return (self->mineMap + (self->x * x + y))->inner == 'M';
}


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
    (self->mineMap + (self->x * x + y))->outer = 'O';
}

void openRound(mineObj* self, int x, int y){

}

