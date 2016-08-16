#ifndef UIDEV_H
#define UIDEV_H

#include <QMainWindow>

namespace Ui {
class uidev;
}

class uidev : public QMainWindow
{
    Q_OBJECT

public:
    explicit uidev(QWidget *parent = 0);
    ~uidev();

private:
    Ui::uidev *ui;
};

#endif // UIDEV_H
