#include <stdio.h>
#include "mineObj.h"

int main(){
    mineObj* myMine = init(4,4);

    openXY(myMine,0,0);
    printf("\n open: \n");
    myMine->showOpen(myMine);
    printf("\n test: \n");
    myMine->showTest(myMine);

//    myMine->showOuter(myMine);
//    printf("\n");
//    myMine->showInner(myMine);
    return 0;
}