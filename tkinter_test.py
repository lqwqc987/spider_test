# -*- coding: utf-8 -*-
from Tkinter import *;
import tkMessageBox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets2()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()

    def createWidgets2(self):
        self.nameInput = Entry(self);
        self.nameInput.pack()
        self.alertBtn = Button(self, text='Hello', command=self.hello)
        self.alertBtn.pack()

    def hello(self):
        name = self.nameInput.get() or 'world';
        tkMessageBox.showinfo('message', 'Hello, %s' % name);
app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
app.mainloop()
