from PyQt5 import QtCore, QtWidgets
from datetime import datetime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow
from Clock import Ui_Clock

import sys
from saint.saint import get_Saint


class ClockScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Clock()
        self.ui.setupUi(self)
        # suppression de la barre des titres
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # effet ombrage
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(2)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 220))
        self.ui.frame.setGraphicsEffect(self.shadow)

        # QTIMER => START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.old_day = -1

        self.ui.pushButton_close.clicked.connect(self.close_window)


    def close_window(self):
        self.close()

    def update_clock(self):
        n = datetime.now()
        hour = n.strftime("%H")
        minute = n.strftime("%M")
        second = n.strftime("%S")

        style = "<span style=\" font-size:72pt;\">{hour}:{minute}:</span><span style=\" font-size:48pt;  color:#5d5d5d;\">{second}</span>"
        strTime = style.replace('{hour}', hour).replace('{minute}', minute).replace('{second}', second)
        self.ui.label_clock.setText(strTime)
        style = "<span style=\" font-size:72pt;color:#d9d9d9\">{hour}:{minute}:</span><span style=\" font-size:48pt;  color:#d9d9d9;\">{second}</span>"
        strTime = style.replace('{hour}', hour).replace('{minute}', minute).replace('{second}', second)
        self.ui.label_shadow.setText(strTime)

        jour_semaine = self.jour_semaine()
        jour = n.strftime("%d")
        month = n.strftime("%m")
        year = n.strftime("%Y")
        if jour != self.old_day:
            m = self.get_month_name(month)
            self.ui.label_date.setText(f"{jour_semaine} {jour} {m} {year}")
            self.old_day = jour

            style="<span style = \"font-style:italic; color:#5a5a5a;\" >{saint}< / span >"
            saint= get_Saint(int(month),jour)
            style=style.replace("{saint}",saint)
            self.ui.label_saint.setText(style)

    def jour_semaine(self):
        day = {0: "Lundi",
               1: "Mardi",
               2: "Mercredi",
               3: "Jeudi",
               4: "Vendredi",
               5: "Samedi",
               6: "Dimanche"
               }
        n = datetime.now().weekday()
        return day.get(n)

    def get_month_name(self, month):
        tab_month = {1: "Janvier",
                     2: "Février",
                     3: "Mars",
                     4: "Avril",
                     5: "Mai",
                     6: "Juin",
                     7: "Juillet",
                     8: "Août",
                     9: "Septembre",
                     10: "Octobre",
                     11: "Novembre",
                     12: "Décembre"
                     }
        return tab_month.get(int(month))


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ClockScreen()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
