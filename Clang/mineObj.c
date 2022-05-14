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
    mineShow* minePoint = (mineShow*)malloc(sizeof(mineShow)*x*y);
    for(int i=0; i<x*y; i++){
        (minePoint+i)->outer = '*';
        (minePoint+i)->inner = ' ';
    }
    mkRandArr(minePoint, x*y, x, 0);

    // 申请mineObj对象
    mineObj* myMine = (mineObj*)malloc(sizeof(mineObj));
    myMine->mine = minePoint;
    myMine->x = x;
    myMine->y = y;
    // myMine->set = set;
    myMine->showInner = showInner;
    myMine->showOuter = showOuter;
    myMine->showOpen = showOpen;
    myMine->showFail = showFail;
    myMine->showTest = showTest;

    return myMine;
}

/**
 * @brief 随机雷区
 * 
 * @param mineMap 
 * @param mapLength 
 * @param mineMax 
 * @param current 
 */
void mkRandArr(mineShow* mineMap, int mapLength, int mineMax, int current) {
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

    return mkRandArr(mineMap, mapLength, mineMax, current);
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
        printf(" %c", (self->mine + i)->inner);
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
        printf(" %c", (self->mine + i)->outer);
    }
}

void showOpen(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mine + i)->outer == '*' ? (self->mine + i)->outer: (self->mine + i)->inner);
    }
}

void showFail(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mine + i)->inner == 'M'
                        ? 'm'
                        : (self->mine + i)->outer == '*'
                            ? (self->mine + i)->outer
                            : (self->mine + i)->inner );
    }
}

void showTest(mineObj* self){
    for(int i=0; i< self->x * self->y; i++){
        if(!(i % self->x )){
            printf("\n");
        }
        printf(" %c", (self->mine + i)->inner == 'M' ? (self->mine + i)->inner: (self->mine + i)->outer);
    }
}