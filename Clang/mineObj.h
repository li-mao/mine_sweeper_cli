typedef struct tagMineCell {
    char outer;
    char inner;
}mineCell;

typedef struct tagMineObj {
    mineCell* mineMap;
    int x;  // 多少行
    int y;  // 每行多少个
    void (* makeRandMine)(struct tagMineObj* self, int mapLength, int mineMax, int current);
    void (* showInner)(struct tagMineObj* self);
    void (* showOuter)(struct tagMineObj* self);
    void (* showOpen)(struct tagMineObj* self);
    void (* showFail)(struct tagMineObj* self);
    void (* showTest)(struct tagMineObj* self);
    int (* openXY)(struct tagMineObj* self, int x, int y, int manual);
    int (* getXY)(struct tagMineObj* self, int x, int y);
    char (* cellCountRound)(struct tagMineObj* self, int x, int y);
    void (* cellHint)(struct tagMineObj* self);
}mineObj;

void makeRandMine(mineObj* self, int mapLength, int mineMax, int current);
void showInner(mineObj* self);
void showOuter(mineObj* self);
void showOpen(mineObj* self);
void showFail(mineObj* self);
void showTest(mineObj* self);
int openXY(mineObj* self, int x, int y, int manual);
int getXY(mineObj* self, int x, int y);
char cellCountRound(mineObj* self, int x, int y);
void cellHint(mineObj* self);

extern mineObj* init(int x, int y);