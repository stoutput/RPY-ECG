#include "ekgui.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ekgui w;
    w.show();

    return a.exec();
}
