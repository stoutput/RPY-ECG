#include "uidev.h"
#include "ui_uidev.h"

uidev::uidev(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::uidev)
{
    ui->setupUi(this);
}

uidev::~uidev()
{
    delete ui;
}
