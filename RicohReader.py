import tkinter as tk
from tkinter import ttk
import os
import datetime
import webbrowser
import time
from puresnmp import walk, get

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for
            PyInstaller. Found on stackoverflow """
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath('.')
            return os.path.join(base_path, relative_path)
        
        self.printers=[
                  {'IP':'172.18.181.227','Name':'CI-121'},
                  {'IP':'172.18.166.19','Name':'CI-202L'},
                  {'IP':'172.18.166.92','Name':'CI-202R'},
                  {'IP':'172.18.181.232','Name':'CI-214'},
                  {'IP':'172.18.181.244','Name':'CI-301'},
                  {'IP':'172.18.181.231','Name':'CI-335'},
                  {'IP':'172.18.181.230','Name':'CI-DO'},
                  {'IP':'172.18.178.120','Name':'SDW-FL2'},
                  {'IP':'172.18.177.204','Name':'ANX-A'},
                  {'IP':'172.19.55.10','Name':'ANX-B'},
                  {'IP':'172.18.186.18','Name':'RH-204'},
        ]

        self.ModelOID = '.1.3.6.1.2.1.43.5.1.1.16.1'
        self.InkLevels_baseOID = '.1.3.6.1.2.1.43.11.1.1.9.1'
        self.TrayNames_baseOID = '.1.3.6.1.2.1.43.8.2.1.13'
        self.TrayMaxCap_baseOID = '.1.3.6.1.2.1.43.8.2.1.9.1'
        self.TrayCurrCap_baseOID = '.1.3.6.1.2.1.43.8.2.1.10.1'
        self.Err_baseOID = '.1.3.6.1.2.1.43.18.1.1.8.1'

        self.c3504ex = tk.PhotoImage(
            file=resource_path('images/c3504ex.png')).subsample(4, 4)
        self.c6004ex = tk.PhotoImage(
            file=resource_path('images/c6004ex.png')).subsample(4, 4)
        self.c6503 = tk.PhotoImage(
            file=resource_path('images/c6503.png')).subsample(4, 4)
        self.c6503f = tk.PhotoImage(
            file=resource_path('images/c6503f.png')).subsample(4, 4)

        self.s=ttk.Style()
        self.s.theme_use('alt')
        self.s.configure('black.Horizontal.TProgressbar',
                         background='black')
        self.s.configure('cyan.Horizontal.TProgressbar',
                         background='cyan')
        self.s.configure('magenta.Horizontal.TProgressbar',
                         background='magenta')
        self.s.configure('yellow.Horizontal.TProgressbar',
                         background='yellow')

        self.styles=['black.Horizontal.TProgressbar',
                'cyan.Horizontal.TProgressbar',
                'magenta.Horizontal.TProgressbar',
                'yellow.Horizontal.TProgressbar',]

        root.title('Ricoh Resource Monitor')
        root.iconbitmap(resource_path('images/icon.ico'))

        self.deficit=tk.IntVar()
        self.deficit.set(0)

        self.reams=tk.IntVar()
        self.deficit.set(0)
        
        self.ItemFrame=ItemFrame(self)
        self.ItemFrame.pack(side="right", fill="y")
        self.SelectionPane=SelectionPane(self)
        self.SelectionPane.pack(side="left", fill="y", expand=True, padx=5, pady=5)

class SelectionPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs, padx=5, pady=5, borderwidth=2, relief=tk.RIDGE)
        self.parent = parent
        
        self.checklist=[]
        self.optionButtons=tk.Frame(self)
        self.nonecheck=tk.Checkbutton(self.optionButtons, text="None",
                                      command=lambda:self.none())
        self.allcheck=tk.Checkbutton(self.optionButtons, text="All",
                                     command=lambda:self.all())
        for entry in parent.printers:
            var=tk.IntVar()
            self.check=tk.Checkbutton(self, text=entry['Name'], variable=var,
                                 command=lambda var=var,entry=entry:
                                      self.shoutout(var.get(), entry))
            self.checklist.append([self.check, var])
            self.check.pack(anchor=tk.W)
            if entry['Name'] in ['CI-121',
                                 'CI-202L', 'CI-202R', 'CI-335', 'SDW-FL2', 'ANX-A',
                                 'ANX-B']:
                self.check.invoke()

        self.nonecheck.pack(side=tk.RIGHT)
        self.allcheck.pack(side=tk.LEFT)
        self.optionButtons.pack()

        self.deficitFrame=tk.Frame(self)
        self.deficitLabel=tk.Label(self.deficitFrame, text="Current deficit: ")
        self.deficitLabel.pack(side=tk.LEFT)
        self.totalDeficit=tk.Label(self.deficitFrame,
                                   textvariable=parent.deficit)
        self.totalDeficit.pack()
        self.deficitFrame.pack(anchor=tk.W, pady=(15,0))

        self.reamFrame=tk.Frame(self)
        self.reamLabel=tk.Label(self.reamFrame, text="Suggested reams: ")
        self.reamLabel.pack(side=tk.LEFT)
        self.reamCount=tk.Label(self.reamFrame, textvariable=parent.reams)
        self.reamCount.pack()
        self.reamFrame.pack(anchor=tk.W)
        self.activeID = None
        self.timeInput = None

        self.reloadFrame=tk.Frame(self)
        self.reloadFrame2=tk.Frame(self)
        self.reloadPrompt1=tk.Label(self.reloadFrame, text='Reload every ')
        self.reloadPrompt1.pack(side=tk.LEFT)
        self.reloadTime=tk.Entry(self.reloadFrame, width=3, insertontime=0)
        self.reloadTime.pack(side=tk.LEFT)
        self.reloadPrompt2=tk.Label(self.reloadFrame, text="seconds")
        self.reloadPrompt2.pack(side=tk.LEFT)
        self.refreshButton=tk.Button(self.reloadFrame2, text="Set",
                                    command=lambda:self.set_timeInput())
        self.reloadTime.insert(tk.END, 600)
        self.reloadPrompt3=tk.Label(self.reloadFrame2, text="(0 to stop)", bd=0)
        self.reloadPrompt3.pack(side=tk.LEFT)
        self.refreshButton.pack(side=tk.LEFT, padx=5)
        self.reloadFrame2.pack(side=tk.BOTTOM, anchor=tk.W)
        self.reloadFrame.pack(side=tk.BOTTOM, anchor=tk.W)

    def shoutout(self, status, name):
        self.nonecheck.deselect()
        print(name['Name'] + " toggled " + str(status))
        if status==1:
            self.PrinterInstance=PrinterFrame(self.parent.ItemFrame,name)
            self.PrinterInstance.pack(side=tk.LEFT, fill=tk.Y)
        elif status==0:
            self.allcheck.deselect()
            try:
                self.parent.deficit.set(
                    self.parent.deficit.get()-self.nametowidget(
                    '.!mainapplication.!itemframe.a'+name['Name']).deficit())
                self.parent.reams.set(self.parent.deficit.get()/500)
                self.nametowidget(
                    '.!mainapplication.!itemframe.a'+name['Name']).destroy()
                self.parent.update()
            except:
                return
            
    def none(self):
        for item in self.checklist:
            item[0].select()
            item[0].invoke()
        time.sleep(1)

    def all(self):
        self.allcheck.select()
        for item in self.checklist:
            item[0].deselect()
            item[0].invoke()
            
    def refresh(self):
        for item in self.checklist:
            if item[1].get()==1:
                self.parent.deficit.set(0)
                item[0].deselect()
                item[0].invoke()
        self.activeID = self.after(self.timeInput*1000, self.refresh)

    def set_timeInput(self):
        x=self.reloadTime.get()
        if x.isdigit():
            if int(x)>0:
                if self.activeID is not None:
                    self.after_cancel(self.activeID)
                    self.activeID=None
                    self.timeInput=int(x)
                    self.refresh()
                else:
                    self.timeInput=int(x)
                    self.refresh()
            else:
                if self.activeID  is not None:
                    self.after_cancel(self.activeID)
                    self.activeID=None
        else:
            if self.activeID is not None:
                self.after_cancel(self.activeID)
                self.activeID=None
            
class ItemFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

class PrinterFrame(tk.Frame):
    def __init__(self, parent, printer):
        tk.Frame.__init__(self, parent, name="a"+printer['Name'], padx=10)
        defaultbg = root.cget('bg')
        self.parent = parent
        self.IP=printer['IP']
        printerName=tk.Label(self, text=printer['Name'], font=(None, 14))
        printerName.pack()

        PrinterModel=tk.Label(self, text=get(printer['IP'], 'public',
                                             parent.parent.ModelOID))
        PrinterModel.pack()

        printerIP=tk.Label(self, text=printer['IP'], fg="blue",
                           font=(None, 8, 'underline'), cursor="hand2")
        url='http://' + printer['IP'] + '/web/guest/en/websys/webArch/getStatus.cgi'
        printerIP.bind("<Button-1>", lambda event,aurl=url:webbrowser.open(aurl))
        printerIP.pack()

        AlertFrame=tk.Frame(self)
        AlertFrame.pack()
        
        scrollbar=tk.Scrollbar(AlertFrame)

        AlertsList=tk.Listbox(AlertFrame, height=3, width=30, fg='red',
                              relief='flat', bg=defaultbg, activestyle='none',
                              borderwidth=0, selectbackground=defaultbg,
                              highlightthickness=0, selectforeground='red')
        AlertsList.pack(side=tk.LEFT, pady=(15,0))
        
        Alerts=walk(printer['IP'], 'public', parent.parent.Err_baseOID)
        AlertLength=0
        for item in Alerts:
            AlertsList.insert(tk.END, item[1].decode('utf-8'))
            AlertLength+=1
        if AlertLength>3:
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            AlertsList.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=AlertsList.yview)
        model=PrinterModel.cget("text").decode('utf-8')
        if model == 'MP C6004ex':
            PrinterImage=parent.parent.c6004ex
        elif model == 'MP C3504ex':
            PrinterImage=parent.parent.c3504ex
        elif model == 'MP C6503':
            LCT=0
            for item in walk(printer['IP'], 'public',
                             parent.parent.TrayNames_baseOID):
                if 'LCT' in item[1].decode('utf-8'):
                    LCT+=1
                else:
                    LCT+=0
            if LCT !=0:
                PrinterImage=parent.parent.c6503f
            else:
                PrinterImage=parent.parent.c6503

        PrinterImageCanvas=tk.Canvas(self, width=135, height=140)
        PrinterImageCanvas.pack()
        PrinterImageCanvas.create_image(135,140,image=PrinterImage, anchor='se')
        PrinterImageCanvas.image=PrinterImage

        InkFrame=tk.Frame(self)
        InkFrame.pack()
        for i, item in enumerate(walk(printer['IP'], 'public',
                                      parent.parent.InkLevels_baseOID)):
            if i==1:
                continue
            if i>1:
                i-=1
            FullInk=tk.Frame(InkFrame)
            InkBar=ttk.Progressbar(FullInk, value=item[1],
                                   style=parent.parent.styles[i])
            InkLevel=tk.Label(FullInk, text="   "+str(item[1])+"%",
                              foreground='red' if item[1]<=20 else 'black', bd=0)
            InkBar.pack(side=tk.LEFT, pady=0)
            InkLevel.pack(side=tk.RIGHT, pady=0)
            FullInk.pack(pady=0)
            
        TrayNames=[]
        TrayCurrentLevels=[]
        TrayMaxLevel=[]
        TrayFrame=tk.Frame(self)
        TrayFrame.pack(pady=(10,5))
        for item in walk(printer['IP'], 'public', parent.parent.TrayNames_baseOID):
            TrayNames.append(item[1].decode('utf-8').replace('Paper','').replace('Tray 3 (LCT)','LCT'))
        for item in walk(printer['IP'], 'public', parent.parent.TrayCurrCap_baseOID):
            TrayCurrentLevels.append(item[1])
        for item in walk(printer['IP'], 'public', parent.parent.TrayMaxCap_baseOID):
            TrayMaxLevel.append(item[1])

        self.PrinterDeficit=0
        
        for i, item in enumerate(TrayNames):
            if item=='Bypass Tray':
                continue
            self.PrinterDeficit+=TrayMaxLevel[i]-TrayCurrentLevels[i]
            TrayLine=tk.Frame(TrayFrame, height=20, width=170)
            TrayLine.pack_propagate(0)

            TrayInfo=tk.Frame(TrayLine, height=20, width=120)
            TrayInfo.pack_propagate(0)
            TrayInfo.pack(side=tk.RIGHT)
            
            TrayLabel=tk.Label(TrayLine, text=item + ": ", font=(None, 9, 'bold'))
            TrayLabel.pack(side=tk.LEFT, anchor=tk.W)
            Percent=int((TrayCurrentLevels[i]/TrayMaxLevel[i])*100)
            TrayPercent=tk.Label(TrayInfo, text=str(Percent)+'%',
                                 foreground='red' if Percent<=20 else 'black')
            TrayCurrentValue=tk.Label(TrayInfo, text='('+str(TrayCurrentLevels[i]))
            TrayMaxValue=tk.Label(TrayInfo, text=str(TrayMaxLevel[i])+')', anchor=tk.E)
            Slash=tk.Label(TrayInfo, text='/', bd=0)

            TrayPercent.pack(side=tk.LEFT, anchor=tk.W)
            TrayMaxValue.pack(side=tk.RIGHT)
            Slash.pack(side=tk.RIGHT)
            TrayCurrentValue.pack(side=tk.RIGHT)
            
            TrayLine.pack(anchor=tk.W, fill=tk.BOTH, expand=True)

        parent.parent.deficit.set(parent.parent.deficit.get()+self.PrinterDeficit)
        parent.parent.reams.set(parent.parent.deficit.get()/500)
    def deficit(self):
        return self.PrinterDeficit
            
            
if __name__ == "__main__":
    root=tk.Tk()
    root.resizable(False, False)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
