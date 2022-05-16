#include <stdio.h>
#include "mineObj.h"

int main(){
    mineObj* myMine = init(16,16);

    int x = 0, y = 0, result = 1;
    while(1){
        printf("plase entry x y:\n");
        scanf("%d %d", &x, &y);
        result = myMine->openXY(myMine,x,y,1);
        if(result){
            myMine->showOpen(myMine);
            printf("\n");
        }else{
            myMine->showFail(myMine);
            printf("\ngame over!!!");
            break;
        }
    }
    return 0;
}