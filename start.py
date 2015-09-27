import __init__
from Tkinter import *

class SampleApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.create_widgets()
        self.entries = [self.e1,self.e2,self.e3,self.e4,self.e5,self.e6,self.e7]
        self.data_from_config()

    def data_from_config(self):

        self.file = open("config.py")
        data = self.file.read().split("\n")
        for i in range(0,(len(self.entries))):
            self.entries[i].insert(0, data[i].split("=")[1][1:-1])
        self.file.close()


    def create_widgets(self):

        self.l1 = Label(self,text="             Consumer Key")
        self.l2 = Label(self,text="             Consumer Secret")
        self.l3 = Label(self,text="             Access Token")
        self.l4 = Label(self,text="             Access Token Secret")
        self.l9 = Label(self,text="             Printer's Twitter Handle")
        self.l14 = Label(self,text="            Your Twitter Handle")
        self.l10 = Label(self,text="            Printer Name")
        self.l5 = Label(self)
        self.l6 = Label(self, text="Welcome To")
        self.l7 = Label(self, text="#Print")
        self.l8 = Label(self)
        self.l11= Label(self)
        self.l12 = Label(self)
        self.l13 = Label(self)
        self.e1 = Entry(self)
        self.e2 = Entry(self)
        self.e3 = Entry(self)
        self.e4 = Entry(self)
        self.e5 = Entry(self)
        self.e6 = Entry(self)
        self.e7 = Entry(self)
        self.b1 = Button(self,text="QUIT", command=self.quit)
        self.b2 = Button(self, text="Configure and Run", command=self.on_config_and_run)

        self.l6.config(font=('times',20,'italic'))
        self.l7.config(font=('times',38,'bold'))

        self.e1.grid(column=1,row=4)
        self.e2.grid(column=1,row=5)
        self.e3.grid(column=1,row=6)
        self.e4.grid(column=1,row=7)
        self.e5.grid(column=1,row=8)
        self.e6.grid(column=1,row=9)
        self.e7.grid(column=1,row=10)
        self.l1.grid(column=0,row=4,sticky="E")
        self.l2.grid(column=0,row=5,sticky="E")
        self.l3.grid(column=0,row=6,sticky="E")
        self.l4.grid(column=0,row=7,sticky="E")
        self.l9.grid(column=0,row=8,sticky="E")
        self.l14.grid(column=0,row=9, sticky="E")
        self.l10.grid(column=0,row=10,sticky="E")
        self.l5.grid(columnspan=2,row=0)
        self.l6.grid(columnspan=2,row=1)
        self.l7.grid(columnspan=2,row=2)
        self.l8.grid(columnspan=2,row=3)
        self.b1.grid(column=0,row=12,sticky="E")
        self.b2.grid(column=1,row=12,sticky="W")
        # self.e1.insert(0,"Default")

    # def on_button(self):
    #     print(self.e2.get())


    def on_config_and_run(self):
        self.file_config_run = open("config.py")
        data_config_run = self.file_config_run.read().split("\n")
        self.url = data_config_run[7].split("=")[1][1:-1]
        # print self.url
        self.file_config_run.close()
        self.write_in_config()
        __init__.main()

    def write_in_config(self):
        with open("config.py",'wb+') as config_run:
            # v = self.entries[0].get()
            # print v
            config_run.write("consumer_key='{0}'\n".format(self.entries[0].get()))
            config_run.write("consumer_secret='{0}'\n".format(self.entries[1].get()))
            config_run.write("access_token='{0}'\n".format(self.entries[2].get()))
            config_run.write("access_token_secret='{0}'\n".format(self.entries[3].get()))
            config_run.write("printer_handle='{0}'\n".format(self.entries[4].get()))
            config_run.write("super_sender='{0}'\n".format(self.entries[5].get()))
            config_run.write("printer_name='{0}'\n".format(self.entries[6].get()))
            config_run.write("url='{0}'\n".format(self.url))





app = SampleApp()
app.grid()
app.geometry("350x350")
app.title("#Print")
app.mainloop()