#ifndef EKGUI_H
#define EKGUI_H

#include <QMainWindow>

namespace Ui {
class ekgui;
}

class ekgui : public QMainWindow
{
    Q_OBJECT

public:
    explicit ekgui(QWidget *parent = 0);
    ~ekgui();

private:
    Ui::ekgui *ui;
};

#endif // EKGUI_H
