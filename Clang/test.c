#include <stdio.h>
#include "mineObj.h"

int main(){
    mineObj* myMine = init(4,4);
    myMine->showTest(myMine);

//    myMine->showOuter(myMine);
//    printf("\n");
//    myMine->showInner(myMine);
    return 0;
}