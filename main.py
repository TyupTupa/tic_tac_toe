import tkinter as tk
from tkinter import *
import time
from tkinter.messagebox import showinfo


class myButton(tk.Button):
    def __init__(self, master, x, y, *args, **kvargs):
        super(myButton, self).__init__(master, *args, **kvargs)
        self.x = x
        self.y = y
        self.whichCoise = 0

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.whichCoise}'

    def makeChoise(self, player):
        self.whichCoise = player
        # print(self.whichCoise)


class Game:
    window = tk.Tk()
    n = 3
    turn = 1
    winSize = 3
    IS_GAME_OVER = False

    def __init__(self):
        self.buttons = []
        count = 1
        self.strTurn = StringVar()
        self.strTurn.set(str(Game.turn))
        self.strWinSize = StringVar()
        self.strWinSize.set(str(Game.winSize))
        for i in range(Game.n):
            temp = []
            for j in range(Game.n):
                btn = myButton(Game.window, x=i, y=j, width=2, height=2, font="Calibri 15 bold")
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
                count += 1
            self.buttons.append(temp)
        self.enteredData = [0] * Game.n
        for i in range(Game.n):
            self.enteredData[i] = [0] * Game.n

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        Game.IS_GAME_OVER = False
        Game.turn = 1
        self.__init__()
        self.createWidgets()

    def createWidgets(self):
        menubar = tk.Menu(Game.window)
        self.window.config(menu=menubar)
        settingsMenu = tk.Menu(menubar, tearoff=0)
        settingsMenu.add_command(label="Перезапуск", command=self.reload)
        settingsMenu.add_command(label="Настройки", command=self.createSettingsWin)
        settingsMenu.add_command(label="Выход", command=self.window.destroy)
        menubar.add_cascade(label="Файл", menu=settingsMenu)
        for i in range(Game.n):
            for j in range(Game.n):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)
        self.label1Text = tk.Label(Game.window, text="Очередь игрока", font="Colibri 15 bold")
        self.label1Text.grid(row=0, column=Game.n + 1)
        self.strTurn.set(str(Game.turn))
        self.labelTurn = tk.Label(Game.window, textvariable=self.strTurn, font="Colibri 15 bold")
        self.labelTurn.grid(row=1, column=Game.n + 1)
        self.label3Text = tk.Label(Game.window, text="Выигрыш (в ряд) -", font="Colibri 10 bold")
        self.label3Text.grid(row=2, column=Game.n + 1)
        self.labelTurn = tk.Label(Game.window, textvariable=self.strWinSize, font="Colibri 15 bold")
        self.labelTurn.grid(row=3, column=Game.n + 1)
        self.label2Text = tk.Label(Game.window, text="Клинова Мария ИДБ-21-12", font="Colibri 10 bold")
        self.label2Text.grid(row=4, column=Game.n + 1)

    def changeTurn(self):
        if Game.turn == 1:
            Game.turn = 2
        else:
            Game.turn = 1
        self.strTurn.set(str(Game.turn))

    def start(self):
        Game.window.title("Крестики/нолики")
        self.createWidgets()
        # self.printButtons()
        Game.window.mainloop()

    def click(self, clickedButton: myButton):
        if Game.IS_GAME_OVER == True:
            return None
        clickedButton.makeChoise(Game.turn)
        if clickedButton.whichCoise == 1:
            clickedButton.config(text="X", disabledforeground="#B71C1C", )
        else:
            clickedButton.config(text="O", disabledforeground="#0000ff")
        clickedButton.config(state="disabled")
        x = clickedButton.x
        y = clickedButton.y
        self.enteredData[x][y] = Game.turn

        if (self.checGlobalWin()):
            Game.IS_GAME_OVER = True
            if Game.turn == 1:
                showinfo('Game over', 'Won 1st player')
            else:
                showinfo('Game over', 'Won 2d player')
        elif (self.checkDraw()):
            showinfo('Game over', 'Draw')
        # print(clickedButton)
        # print(self.enteredData)
        self.changeTurn()

    def checkDraw(self):
        temp = []
        for i in range(Game.n):
            for j in range(Game.n):
                temp.append(self.enteredData[i][j])
        # print(temp)
        if 0 in temp:
            return False
        else:
            return True

    def checGlobalWin(self):
        for i in range(Game.n - Game.winSize + 1):
            for j in range(Game.n - Game.winSize + 1):
                if (self.checkWin3(i, j, Game.winSize)):
                    return True
        return False

    def checkWin3(self, x, y, winSize):
        win = False

        # print(self.enteredData)

        for i in range(winSize):
            temp = []
            for j in range(winSize):
                temp.append(self.enteredData[x + i][y + j])
            counter = 1
            for i in range(len(temp) - 1):
                if temp[i] == temp[i + 1] and (temp[i + 1] != 0 or temp[i] != 0):
                    counter += 1
                    # print("Count "+ str(counter))
                else:
                    counter = 1
                if counter == winSize: win = True

        for i in range(winSize):
            temp = []
            for j in range(winSize):
                temp.append(self.enteredData[x + j][y + i])
            counter = 1
            for i in range(len(temp) - 1):
                if temp[i] == temp[i + 1] and (temp[i + 1] != 0 or temp[i] != 0):
                    counter += 1
                    # print("Count "+ str(counter))
                else:
                    counter = 1
                if counter == winSize: win = True

        temp1 = []
        for i in range(winSize):
            temp1.append(self.enteredData[x + i][y + i])
        counter = 1
        for i in range(len(temp1) - 1):
            if temp1[i] == temp1[i + 1] and (temp1[i + 1] != 0 or temp1[i] != 0):
                counter += 1
                # print("Count "+ str(counter))
            else:
                counter = 1
            if counter == winSize: win = True

        temp2 = []
        for i in range(winSize):
            temp2.append(self.enteredData[x + winSize - 1 - i][y + i])
        counter = 1
        for i in range(len(temp2) - 1):
            if temp2[i] == temp2[i + 1] and (temp2[i + 1] != 0 or temp2[i] != 0):
                counter += 1
                # print("Count "+ str(counter))
            else:
                counter = 1
            if counter == winSize: win = True

        return win

    def settingsClick(self, clickedButton, size):
        Game.n = size
        if size == 3:
            Game.winSize = 3
        else:
            Game.winSize = 4
        clickedButton.config(state="disabled")
        time.sleep(1)
        self.winSettings.destroy()
        self.reload()

    def createSettingsWin(self):

        self.winSettings = tk.Toplevel(self.window)
        self.winSettings.title("Настройки")
        label = tk.Label(self.winSettings, text="Размер поля", font="Colibri 15 bold")
        label.grid(row=0, column=1)
        choise1 = tk.Button(self.winSettings, text='3', font="Colibri 15 bold", width=5, height=1)
        choise2 = tk.Button(self.winSettings, text='4', font="Colibri 15 bold", width=5, height=1)
        choise3 = tk.Button(self.winSettings, text='6', font="Colibri 15 bold", width=5, height=1)
        choise1.config(command=lambda button=choise1: self.settingsClick(button, 3))
        choise2.config(command=lambda button=choise2: self.settingsClick(button, 4))
        choise3.config(command=lambda button=choise3: self.settingsClick(button, 6))
        choise1.grid(row=1, column=1)
        choise2.grid(row=2, column=1)
        choise3.grid(row=3, column=1)

    def printButtons(self):
        for i in self.buttons:
            print(i)


gm1 = Game()
gm1.start()







