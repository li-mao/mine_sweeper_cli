typedef struct tagMineCell {
    char outer;
    char inner;
}mineCell;

typedef struct tagMineObj {
    mineCell* mineMap;
    int x;
    int y;
    // void (* set)(mineObj self, int x, int y, char sign);
    void (* showInner)(struct tagMineObj* self);
    void (* showOuter)(struct tagMineObj* self);
    void (* showOpen)(struct tagMineObj* self);
    void (* showFail)(struct tagMineObj* self);
    void (* showTest)(struct tagMineObj* self);
    void (* openXY)(struct tagMineObj* self, int x, int y);
    int (* getXY)(struct tagMineObj* self, int x, int y);
}mineObj;

void makeRandMine(mineCell* mineMap, int mapLength, int mineMax, int current);
void showInner(mineObj* self);
void showOuter(mineObj* self);
void showOpen(mineObj* self);
void showFail(mineObj* self);
void showTest(mineObj* self);
void openXY(mineObj* self, int x, int y);
int getXY(mineObj* self, int x, int y);

extern mineObj* init(int x, int y);