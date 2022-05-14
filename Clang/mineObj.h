typedef struct tagMineShow {
    char outer;
    char inner;
}mineShow;

typedef struct tagMineObj {
    mineShow* mine;
    int x;
    int y;
    // void (* set)(mineObj self, int x, int y, char sign);
    void (* showInner)(struct tagMineObj* self);
    void (* showOuter)(struct tagMineObj* self);
    void (* showOpen)(struct tagMineObj* self);
    void (* showFail)(struct tagMineObj* self);
    void (* showTest)(struct tagMineObj* self);
}mineObj;

void mkRandArr(mineShow* mineMap, int mapLength, int mineMax, int current);
void showInner(mineObj* self);
void showOuter(mineObj* self);
void showOpen(mineObj* self);
void showFail(mineObj* self);
void showTest(mineObj* self);

extern mineObj* init(int x, int y);