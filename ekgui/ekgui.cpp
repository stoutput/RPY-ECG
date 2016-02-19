#include "ekgui.h"
#include "ui_ekgui.h"

ekgui::ekgui(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ekgui)
{
    ui->setupUi(this);
}

ekgui::~ekgui()
{
    delete ui;
}
