#include <stdio.h>
#include "mineObj.h"

int main(){
    mineObj* myMine = init(8,8);

    myMine->openXY(myMine,0,0,1);
    printf("\n open: \n");
    myMine->showOpen(myMine);
    printf("\n test: \n");
    myMine->showTest(myMine);

//    myMine->showOuter(myMine);
    printf("\n showInner \n");
    myMine->showInner(myMine);
    return 0;
}