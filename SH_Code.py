from cmath import e
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel,
    QPushButton, QTextEdit, QSpinBox,
    QComboBox, QDoubleSpinBox, QCheckBox,
    QListView, QStatusBar, QListWidget,
    QLineEdit, QMessageBox, QAction,
    QFileDialog, QMenu)
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
import pyautogui
import sqlite3


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load UI File
        uic.loadUi("SH_Layout.ui", self)

        # Define Widgets
        self.statusBar = self.findChild(QStatusBar, "statusbar")

        self.XSpin = self.findChild(QSpinBox, "X_Spin")
        self.YSpin = self.findChild(QSpinBox, "Y_Spin")
        self.MouseEvents = self.findChild(QComboBox, "MouseEvents")
        self.ClickSpin = self.findChild(QSpinBox, "ClickSpin")
        self.MouseButton = self.findChild(QComboBox, "MouseButton")
        self.IntervalSpin = self.findChild(QDoubleSpinBox, "IntervalSpin")
        self.SubmitMouse = self.findChild(QPushButton, "SubmitButton_Mouse")
        self.ScrollSpin = self.findChild(QSpinBox, "ScrollSpin")

        self.EnteredText = self.findChild(QLineEdit, "EnteredText")
        self.TextIntervalSpin = self.findChild(
            QDoubleSpinBox, "TextIntervalSpin")
        self.SubmitText = self.findChild(QPushButton, "SubmitButton_Text")

        self.KeyPressed = self.findChild(QComboBox, "KeyPressed")
        self.KeyState = self.findChild(QComboBox, "KeyState")
        self.SubmitKey = self.findChild(QPushButton, "SubmitButton_Key")

        self.RunAll = self.findChild(QPushButton, "RunAll")
        self.RunSeleted = self.findChild(QPushButton, "RunSelected")
        self.Loop = self.findChild(QSpinBox, "InterationSpin")
        self.DeleteEvent = self.findChild(QPushButton, "DeleteEvent")
        self.DeleteAll = self.findChild(QPushButton, "DeleteAll")
        self.EventList = self.findChild(QListWidget, "EventList")
        self.TaskName = self.findChild(QLineEdit, "TaskName")
        self.EditButton = self.findChild(QPushButton, "EditButton")

        self.FileMenu = self.findChild(QMenu, "menuFile")
        self.NewProject = self.findChild(QAction, "actionNew")
        self.Save = self.findChild(QAction, "actionSave")
        self.Open = self.findChild(QAction, "actionOpen")
        self.CloseIt = self.findChild(QAction, "actionClose")
        self.Quit = self.findChild(QAction, "actionQuit")

        self.EditButton.clicked.connect(self.CopyOver)
        self.NewProject.triggered.connect(self.NewFile)
        self.Quit.triggered.connect(self.quitAll)
        self.CloseIt.triggered.connect(self.closeAll)
        self.Save.triggered.connect(self.saveAll)
        self.Open.triggered.connect(self.openAll)
        self.SubmitMouse.clicked.connect(self.SubmitMouseBTN)
        self.SubmitText.clicked.connect(self.SubmitTextBTN)
        self.SubmitKey.clicked.connect(self.SubmitKeyBTN)
        self.RunAll.clicked.connect(self.RunAllBTN)
        self.RunSeleted.clicked.connect(self.RunSelectedBTN)
        self.DeleteAll.clicked.connect(self.DeleteAllBTN)
        self.DeleteEvent.clicked.connect(self.DeleteEventBTN)

        # Show App
        self.show()
        self.setMouseTracking(True)

    def SubmitKeyBTN(self):
        item = f'{self.KeyPressed.currentText()}*{self.KeyState.currentIndex()}*2'
        self.EventList.addItem(item)

    def SubmitTextBTN(self):
        item = f'{self.EnteredText.text()}*{self.TextIntervalSpin.value()}*1'
        self.EventList.addItem(item)

    def SubmitMouseBTN(self):
        item = f'{self.MouseEvents.currentIndex()}{self.MouseButton.currentIndex()}{self.ClickSpin.value()}*{self.IntervalSpin.value()}*{self.XSpin.value()}*{self.YSpin.value()}*{self.ScrollSpin.value()}*0'
        self.EventList.addItem(item)

    def RunAllBTN(self):
        loopCount = int(self.Loop.value())
        while loopCount > 0:
            loopCount -= 1
            items = []
            for events in range(self.EventList.count()):
                items.append(self.EventList.item(events))

            if items == []:
                return

            for item in items:
                process = item.text().split("*")
                if process[-1] == "2":
                    if process[1] == "0":
                        pyautogui.keyDown(process[0])
                    if process[1] == "1":
                        pyautogui.keyUp(process[0])
                    if process[1] == "2":
                        pyautogui.press(process[0])
                if process[-1] == "1":
                    pyautogui.typewrite(process[0], interval=float(process[1]))
                if process[-1] == "0":
                    if process[0][0] == "0":
                        pyautogui.moveTo(x=int(process[2]), y=int(
                            process[3]), duration=float(process[1]))

                    elif process[0][0] == "1":
                        if process[0][1] == "0":
                            pyautogui.click(button='left', clicks=int(process[0][2:]), interval=float(
                                process[1]), x=int(process[2]), y=int(process[3]))
                        if process[0][1] == "1":
                            pyautogui.click(button='right', clicks=int(process[0][2:]), interval=float(
                                process[1]), x=int(process[2]), y=int(process[3]))
                        if process[0][1] == "2":
                            pyautogui.click(button='middle', clicks=int(process[0][2:]), interval=float(
                                process[1]), x=int(process[2]), y=int(process[3]))

                    if process[0][0] == "2":
                        pyautogui.scroll(x=int(process[2]), y=int(
                            process[3]), clicks=int(process[4]))

                    if process[0][0] == "3":
                        if process[0][1] == "0":
                            pyautogui.dragTo(x=int(process[2]), y=int(
                                process[3]), button='left', duration=float(
                                process[1]))
                        if process[0][1] == "1":
                            pyautogui.dragTo(x=int(process[2]), y=int(
                                process[3]), button='right', duration=float(
                                process[1]))
                        if process[0][1] == "2":
                            pyautogui.dragTo(x=int(process[2]), y=int(
                                process[3]), button='middle', duration=float(
                                process[1]))

    def RunSelectedBTN(self):
        loopCount = int(self.Loop.value())
        while loopCount > 0:
            loopCount -= 1
            if self.EventList.count() == 0:
                return

            task = self.EventList.item(self.EventList.currentRow())
            if task == None:
                return

            process = task.text().split("*")

            if process[-1] == "2":
                if process[1] == "0":
                    pyautogui.keyDown(process[0])
                if process[1] == "1":
                    pyautogui.keyUp(process[0])
                if process[1] == "2":
                    pyautogui.press(process[0])
            if process[-1] == "1":
                pyautogui.typewrite(process[0], interval=float(process[1]))
            if process[-1] == "0":
                if process[0][0] == "0":
                    pyautogui.moveTo(x=int(process[2]), y=int(
                        process[3]), duration=float(process[1]))

                elif process[0][0] == "1":
                    if process[0][1] == "0":
                        pyautogui.click(button='left', clicks=int(process[0][2:]), interval=float(
                            process[1]), x=int(process[2]), y=int(process[3]))
                    if process[0][1] == "1":
                        pyautogui.click(button='right', clicks=int(process[0][2:]), interval=float(
                            process[1]), x=int(process[2]), y=int(process[3]))
                    if process[0][1] == "2":
                        pyautogui.click(button='middle', clicks=int(process[0][2:]), interval=float(
                            process[1]), x=int(process[2]), y=int(process[3]))

                if process[0][0] == "2":
                    pyautogui.scroll(x=int(process[2]), y=int(
                        process[3]), clicks=int(process[4]))

                if process[0][0] == "3":
                    if process[0][1] == "0":
                        pyautogui.dragTo(x=int(process[2]), y=int(
                            process[3]), button='left', duration=float(
                            process[1]))
                    if process[0][1] == "1":
                        pyautogui.dragTo(x=int(process[2]), y=int(
                            process[3]), button='right', duration=float(
                            process[1]))
                    if process[0][1] == "2":
                        pyautogui.dragTo(x=int(process[2]), y=int(
                            process[3]), button='middle', duration=float(
                            process[1]))

    def DeleteAllBTN(self):
        self.EventList.clear()

    def DeleteEventBTN(self):
        selectEvent = self.EventList.currentRow()
        self.EventList.takeItem(selectEvent)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        text = f'x: {x},  y: {y}'
        # print(text)
        self.statusBar.showMessage(f'{pyautogui.position()}')

    def saveAll(self):
        if self.TaskName.text() != "":
            conn = sqlite3.connect(f'{self.TaskName.text()}.db')
        else:
            conn = sqlite3.connect(f'untitled.db')

        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists todo_list(
            list_item text)
            """)

        # Dlete Everything in Database
        c.execute('DELETE FROM todo_list;',)

        items = []
        for index in range(self.EventList.count()):
            items.append(self.EventList.item(index))

        for item in items:
            c.execute("INSERT INTO todo_list VALUES (:item)",
                      {
                          'item': item.text(),
                      }
                      )

        conn.commit()
        conn.close()

        # Popup Box
        msg = QMessageBox()
        msg.setWindowTitle("Saved To Database!")
        msg.setText("Your Todo List has been Saved!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def openAll(self):
        fname = QFileDialog.getOpenFileName(
            self, "Open File", "", "Database FIles (*db)")
        if fname:
            splitName = fname[0].split("/")
            conn = sqlite3.connect(f'{splitName[-1]}')
            c = conn.cursor()
            c.execute("SELECT * FROM todo_list")
            records = c.fetchall()
            conn.commit()
            conn.close()

            self.TaskName.setText(f'{splitName[-1][:-3]}')

            for record in records:
                self.EventList.addItem(str(record[0]))
            self.Loop.setValue(1)

    def quitAll(self):
        self.close()

    def closeAll(self):
        self.FileMenu.hideTearOffMenu()

    def NewFile(self):
        self.TaskName.setText("")
        self.EventList.clear()
        self.Loop.setValue(1)

    def CopyOver(self):
        if self.EventList.count() == 0:
            return

        task = self.EventList.item(self.EventList.currentRow())
        if task == None:
            return

        process = task.text().split("*")

        if process[-1] == "2":
            if process[1] == "0":
                # pyautogui.keyDown(process[0])
                self.KeyPressed.setCurrentText(process[0])
                self.KeyState.setCurrentIndex(0)
            if process[1] == "1":
                self.KeyPressed.setCurrentText(process[0])
                self.KeyState.setCurrentIndex(1)
            if process[1] == "2":
                self.KeyPressed.setCurrentText(process[0])
                self.KeyState.setCurrentIndex(2)
        if process[-1] == "1":
            # pyautogui.typewrite(process[0], interval=process[1])
            self.EnteredText.setText(process[0])
            self.TextIntervalSpin.setValue(float(process[1]))
        if process[-1] == "0":
            if process[0][0] == "0":
                # pyautogui.moveTo(x=int(process[2]), y=int(
                #     process[3]), duration=float(process[1]))
                self.XSpin.setValue(int(process[2]))
                self.YSpin.setValue(int(process[3]))
                self.IntervalSpin.setValue(float(process[1]))
                self.MouseEvents.setCurrentIndex(0)

            elif process[0][0] == "1":
                if process[0][1] == "0":
                    # pyautogui.click(button='left', clicks=int(process[0][2:]), interval=float(
                    #     process[1]), x=int(process[2]), y=int(process[3]))

                    self.XSpin.setValue(int(process[2]))
                    self.YSpin.setValue(int(process[3]))
                    self.IntervalSpin.setValue(float(process[1]))
                    self.MouseEvents.setCurrentIndex(1)
                    self.MouseButton.setCurrentIndex(0)
                    self.ClickSpin.setValue(int(process[0][2:]))
                if process[0][1] == "1":
                    self.XSpin.setValue(int(process[2]))
                    self.YSpin.setValue(int(process[3]))
                    self.IntervalSpin.setValue(float(process[1]))
                    self.MouseEvents.setCurrentIndex(1)
                    self.MouseButton.setCurrentIndex(1)
                    self.ClickSpin.setValue(int(process[0][2:]))
                if process[0][1] == "2":
                    self.XSpin.setValue(int(process[2]))
                    self.YSpin.setValue(int(process[3]))
                    self.IntervalSpin.setValue(float(process[1]))
                    self.MouseEvents.setCurrentIndex(1)
                    self.MouseButton.setCurrentIndex(2)
                    self.ClickSpin.setValue(int(process[0][2:]))

            if process[0][0] == "2":
                # pyautogui.scroll(x=int(process[2]), y=int(
                #     process[3]), clicks=int(process[4]))
                self.XSpin.setValue(int(process[2]))
                self.YSpin.setValue(int(process[3]))
                self.MouseEvents.setCurrentIndex(2)
                self.ScrollSpin.setValue(int(process[4]))

            if process[0][0] == "3":
                if process[0][1] == "0":
                    # pyautogui.dragTo(x=int(process[2]), y=int(
                    #     process[3]), button='left', duration=float(
                    #     process[1]))
                    self.XSpin.setValue(int(process[2]))
                    self.YSpin.setValue(int(process[3]))
                    self.IntervalSpin.setValue(float(process[1]))
                    self.MouseEvents.setCurrentIndex(3)
                    self.MouseButton.setCurrentIndex(0)
                if process[0][1] == "1":
                    self.XSpin.setValue(int(process[2]))
                    self.YSpin.setValue(int(process[3]))
                    self.IntervalSpin.setValue(float(process[1]))
                    self.MouseEvents.setCurrentIndex(3)
                    self.MouseButton.setCurrentIndex(1)
                if process[0][1] == "2":
                    self.XSpin.setValue(int(process[2]))
                    self.YSpin.setValue(int(process[3]))
                    self.IntervalSpin.setValue(float(process[1]))
                    self.MouseEvents.setCurrentIndex(3)
                    self.MouseButton.setCurrentIndex(2)


# Initialize App
# if __name__ == "__Main__":
# app = QApplication(sys.argv)
# UIWindow = UI()
# app.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    UIWindow.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window...")
    # app.exec_()
