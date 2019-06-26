import os
import Pmw
import time
import os.path
import datetime
import traceback
import webbrowser
import tkinter as tk
from tkinter import ttk
from puresnmp import walk, get

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        def resource_path(relative_path):
            #Get absolute path to resource, works for dev and for
            #PyInstaller - Found on stackoverflow
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath('.')
            return os.path.join(base_path, relative_path)

        #Define printer names and IP address
        self.printers=[
                  {'IP':'172.18.181.227','Name':'CI-121',
                   'Serial':'C068C400217','EID':'14072973'},
                  {'IP':'172.18.166.19','Name':'CI-202L',
                   'Serial':'C068C400212','EID':'14072975'},
                  {'IP':'172.18.166.92','Name':'CI-202R',
                   'Serial':'C068C300002','EID':'14072974'},
                  {'IP':'172.18.181.232','Name':'CI-214',
                   'Serial':'C758M520307','EID':'14072971'},
                  {'IP':'172.18.181.244','Name':'CI-301',
                   'Serial':'C728M810465','EID':'14143593'},
                  {'IP':'172.18.181.231','Name':'CI-335',
                   'Serial':'C068C400148','EID':'14072972'},
                  {'IP':'172.18.181.230','Name':'CI-DO',
                   'Serial':'C758M520011','EID':'14072970'},
                  {'IP':'172.18.178.120','Name':'SDW-FL2',
                   'Serial':'C758M520012','EID':'14072977'},
                  {'IP':'172.18.177.204','Name':'ANX-A',
                   'Serial':'C068C400209','EID':'14072979'},
                  {'IP':'172.19.55.10','Name':'ANX-B',
                   'Serial':'C068C400222','EID':'14072976'},
                  {'IP':'172.18.186.18','Name':'RH-204',
                   'Serial':'C727M810074','EID':'14381339'},
        ]

        #Define OIDs for Ricoh brand printers
        self.model_OID = '.1.3.6.1.2.1.43.5.1.1.16.1'
        self.ink_levels_base_OID = '.1.3.6.1.2.1.43.11.1.1.9.1'
        self.tray_names_base_OID = '.1.3.6.1.2.1.43.8.2.1.13'
        self.tray_max_capacity_base_OID = '.1.3.6.1.2.1.43.8.2.1.9.1'
        self.tray_current_capacity_base_OID = '.1.3.6.1.2.1.43.8.2.1.10.1'
        self.error_base_OID = '.1.3.6.1.2.1.43.18.1.1.8.1'

        #Create printer images
        self.c3504ex = tk.PhotoImage(
            file=resource_path('images/c3504ex.png')).subsample(4, 4)
        self.c6004ex = tk.PhotoImage(
            file=resource_path('images/c6004ex.png')).subsample(4, 4)
        self.c6503 = tk.PhotoImage(
            file=resource_path('images/c6503.png')).subsample(4, 4)
        self.c6503f = tk.PhotoImage(
            file=resource_path('images/c6503f.png')).subsample(4, 4)
        self.no_connection = tk.PhotoImage(
            file=resource_path('images/NoConnection.png')).subsample(4, 4)

        #Create styles for progress bars
        self.style=ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('black.Horizontal.TProgressbar',
                         background='black')
        self.style.configure('cyan.Horizontal.TProgressbar',
                         background='cyan')
        self.style.configure('magenta.Horizontal.TProgressbar',
                         background='magenta')
        self.style.configure('yellow.Horizontal.TProgressbar',
                         background='yellow')

        #Create list with different progress bar styles for easy reference
        #Second item is None because there are actually 5 ink results, with the
        #second being waste toner
        self.styles=[('black.Horizontal.TProgressbar','Black'),
                     (None,None),
                     ('cyan.Horizontal.TProgressbar','Cyan'),
                     ('magenta.Horizontal.TProgressbar','Magenta'),
                     ('yellow.Horizontal.TProgressbar','Yellow')]

        #Define window properties
        root.title('Ricoh Resource Monitor v3.4.1')
        root.iconbitmap(resource_path('images/icon.ico'))

        #Grab the current time for logfile creation
        self.current_time=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

        #Create variables to hold current paper deficit
        self.deficit=tk.IntVar()
        self.deficit.set(0)

        self.reams=tk.IntVar()
        self.deficit.set(0)

        #Create frame that will hold the printers
        self.item_frame=ItemFrame(self)
        self.item_frame.pack(side="right", fill="y")

        #Create frame that will hold the checkbuttons
        self.selection_pane=SelectionPane(self)
        self.selection_pane.pack(side="left", fill="y", expand=True,
                                 padx=5, pady=5)

        #Create the hover label in the bottom right
        self.q=tk.Label(self.item_frame, text="?", bd=0,
                        font=(None, 6), cursor="hand2")
        self.q.pack(side=tk.RIGHT, anchor=tk.S)
        self.balloon = Pmw.Balloon(parent)
        self.balloon.bind(self.q, 'RRM v3.4.1\n'
                          'Emilio Garcia\n'
                          'SC&I IT Helpdesk')
        self.q.bind("<Button-1>",
                    lambda event: webbrowser.open(
                        'https://github.com/4rm/Ricoh-Resource-Monitor/releases'
                        )
                    )

class SelectionPane(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs,
                          padx=5, pady=5, borderwidth=2, relief=tk.RIDGE)
        self.parent = parent

        #Initialize list to hold checkbox variables and checkbutton objects
        self.checklist=[]

        #Create frame to hold 'all' and 'none' buttons
        self.option_buttons=tk.Frame(self)
        self.none_check=tk.Checkbutton(self.option_buttons, text="None",
                                      command=lambda:self.none(),
                                       cursor="hand2")
        self.all_check=tk.Checkbutton(self.option_buttons, text="All",
                                     command=lambda:self.all(),
                                      cursor="hand2")
        self.none_check.pack(side=tk.RIGHT)
        self.all_check.pack(side=tk.LEFT)
        
        #For each defined printer, generate a Checkbutton
        for entry in parent.printers:
            var=tk.IntVar()
            self.check=tk.Checkbutton(self, text=entry['Name'], variable=var,
                                 command=lambda var=var,entry=entry:
                                      self.spawn_despawn(var.get(), entry),
                                 cursor="hand2")
            self.checklist.append([self.check, var])
            self.check.pack(anchor=tk.W)
            #If the printer is one that we refill on our paper route, autoload
            if entry['Name'] in ['CI-121', 'CI-202L', 'CI-202R',
                                 'CI-335', 'SDW-FL2', 'ANX-A',
                                 'ANX-B']:
                self.check.invoke()

        #Pack options below other checkbuttons
        self.option_buttons.pack()

        #Create frame for current paper deficit
        self.deficit_frame=tk.Frame(self)
        self.deficit_label=tk.Label(self.deficit_frame,
                                    text="Current deficit: ",
                                    font=(None, 9, 'italic'))
        self.deficit_label.pack(side=tk.LEFT)
        self.total_deficit=tk.Label(self.deficit_frame,
                                   textvariable=parent.deficit)
        self.total_deficit.pack(side=tk.RIGHT)
        self.deficit_frame.pack(anchor=tk.W, pady=(10,0), fill=tk.BOTH)

        #Create frame for suggested ream count
        self.ream_frame=tk.Frame(self)
        self.ream_label=tk.Label(self.ream_frame,
                                 text="Suggested reams: ",
                                 font=(None, 9, 'italic'))
        self.ream_label.pack(side=tk.LEFT)
        self.ream_count=tk.Label(self.ream_frame,
                                 textvariable=parent.reams)
        self.ream_count.pack(side=tk.RIGHT)
        self.ream_frame.pack(anchor=tk.W, fill=tk.BOTH)

        #Create frame for variable refresh options/prompt
        self.reload_frame=tk.Frame(self)
        self.reload_frame_2=tk.Frame(self)
        self.reload_prompt_1=tk.Label(self.reload_frame, text='Reload every ')
        self.reload_prompt_1.pack(side=tk.LEFT)
        self.reload_time=tk.Entry(self.reload_frame, width=3, insertontime=0)
        self.reload_time.pack(side=tk.LEFT)
        self.reload_prompt_2=tk.Label(self.reload_frame, text="seconds")
        self.reload_prompt_2.pack(side=tk.LEFT)
        self.reload_time.insert(tk.END, 600)
        self.stop_button=tk.Button(self.reload_frame_2, text="Stop",
                                   command=lambda:self.reset_timer(),
                                   width=9, cursor="hand2")
        self.stop_button.pack(side=tk.RIGHT)
        self.refresh_button=tk.Button(self.reload_frame_2, text="Set",
                                      command=lambda:self.set_timeInput(),
                                      width=9, cursor="hand2")
        self.refresh_button.pack(side=tk.LEFT)
        self.reload_frame_2.pack(side=tk.BOTTOM, anchor=tk.E, fill=tk.X)
        self.reload_frame.pack(side=tk.BOTTOM, anchor=tk.W, pady=(10,5))

        #Define variables for variable refresh
        self.active_ID = None
        self.time_input = None

    def spawn_despawn(self, status, name):
        self.none_check.deselect()
        print(name['Name'] + " toggled " + str(status))
        if status==1:
            #If checkbox is checked, spawn printer frame
            self.printer_instance=PrinterFrame(self.parent.item_frame,name)
            self.printer_instance.pack(side=tk.LEFT, fill=tk.Y)
        elif status==0:
            #If unchecked, subtract deficit and destroy printer frame
            self.all_check.deselect()
            try:
                #Try reducing the total deficit
                self.parent.deficit.set(
                    self.parent.deficit.get()-self.nametowidget(
                    '.!mainapplication.!itemframe.a'+name['Name']).deficit())
                self.parent.reams.set(self.parent.deficit.get()/500)
            except Exception as e:
                #Might fail if a "No Connection" frame is spawned
                print(e)
            try:
                #Remove printer frames by name
                self.nametowidget(
                    '.!mainapplication.!itemframe.a'+name['Name']).destroy()
                self.parent.update()
            except Exception as e:
                #When 'none' is called, it may try to destroy unspawned printer
                print(e)
                return
            
    def none(self):
        for item in self.checklist:
            item[0].select()
            item[0].invoke()

    def all(self):
        #prevent double counting deficits by resetting to 0
        self.parent.deficit.set(0)
        for item in self.checklist:
            item[0].deselect()
            item[0].invoke()
            
    def refresh(self):
        self.parent.deficit.set(0)
        for item in self.checklist:
            if item[1].get()==1:
                item[0].deselect()
                item[0].invoke()
        self.active_ID = self.after(self.time_input*1000, self.refresh)

    def set_timeInput(self):
        reset_interval=self.reload_time.get()
        if reset_interval.isdigit():
            if int(reset_interval)>0:
                if self.active_ID is not None:
                    #if there's a current 'after' process...
                    self.after_cancel(self.active_ID)
                    self.active_ID=None
                    self.time_input=int(reset_interval)
                    self.refresh()
                else:
                    #if there's no current 'after' process
                    self.time_input=int(reset_interval)
                    self.refresh()
            else:
                if self.active_ID  is not None:
                    #stop 'after' process on <=0 input
                    self.after_cancel(self.active_ID)
                    self.active_ID=None
        else:
            self.reload_time.delete(0, tk.END)
            self.reload_time.insert(tk.END, 600)
            if self.active_ID is not None:
                #stop 'after' process on non-numeric input
                self.after_cancel(self.active_ID)
                self.active_ID=None

    def reset_timer(self):
        self.reload_time.delete(0, tk.END)
        self.reload_time.insert(tk.END, 0)
        if self.active_ID is not None: 
            self.after_cancel(self.active_ID)
            self.active_ID=None
            
class ItemFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        #Create a frame object that inherits variables from MainApplication

class PrinterFrame(tk.Frame):
    def __init__(self, parent, printer):
        tk.Frame.__init__(self, parent, name="a"+printer['Name'], padx=5)
        #initialize frame with name of printer (preface with 'a' because name
        #can't start with a capital letter
        
        default_bg = root.cget('bg')
        #grab the default background color to create pseudo-transparent object
        
        self.parent = parent
        self.IP=printer['IP']
        
        balloon = Pmw.Balloon(parent)
        
        printer_name=tk.Label(self, text=printer['Name'], font=(None, 14))
        balloon.bind(printer_name, 'Serial: ' + printer['Serial'] +
                     '\nEID: ' +printer['EID'])
        printer_name.pack()

        try:
            printer_model=tk.Label(self, text=get(printer['IP'], 'public',
                                                 parent.parent.model_OID))
            printer_model.pack()

            url='http://' + printer['IP'] + '/web/guest/en/websys/webArch/mainFrame.cgi'
            printer_IP=tk.Label(self, text=printer['IP'], fg="blue",
                               font=(None, 8, 'underline'), cursor="hand2")
            balloon.bind(printer_IP, 'Go to printer control panel')
            printer_IP.bind("<Button-1>",
                            lambda event,aurl=url:webbrowser.open(aurl))
            #Bind event property to label to create a hyperlink
            printer_IP.pack()

            alert_frame=tk.Frame(self)
            alert_frame.pack()
            
            scrollbar=tk.Scrollbar(alert_frame)
            alerts_list=tk.Listbox(alert_frame, height=3, width=30, fg='red',
                                  relief='flat', bg=default_bg, activestyle='none',
                                  borderwidth=0, selectbackground=default_bg,
                                  highlightthickness=0, selectforeground='red')
            alerts_list.pack(side=tk.LEFT, pady=(5,0))
            alerts=walk(printer['IP'], 'public', parent.parent.error_base_OID)
            alert_length=0
            #alerts is returned as an interator, so we define a counter to track
            #its size
            for item in alerts:
                alerts_list.insert(tk.END, item[1].decode('utf-8'))
                alert_length+=1
            if alert_length>3:
                #Only pack the scrollbar if there are 3 or more messages
                #The scrollbar must be at least 3 lines long, so this is the
                #smallest possible size
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                alerts_list.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=alerts_list.yview)

            #Start finding the correct picture to match the model    
            model=printer_model.cget('text').decode('utf-8')
            printer_image=None
            if model == 'MP C6004ex':
                printer_image=parent.parent.c6004ex
            elif model == 'MP C3504ex':
                printer_image=parent.parent.c3504ex
            elif model == 'MP C6503':
                #The C6503 may or may not have an LCT
                for item in walk(printer['IP'],
                                 'public',
                                 parent.parent.tray_names_base_OID
                                 ):
                    #Check if the tray names contain 'LCT'
                    if 'LCT' in item[1].decode('utf-8'):
                        printer_image=parent.parent.c6503f
                        break
                if printer_image is None:
                    #If the image still has not been set, it must be non-LCT C6503
                    printer_image=parent.parent.c6503

            #Now that we know where the image should point to, create image object
            printer_image_canvas=tk.Canvas(self, width=135, height=140)
            printer_image_canvas.pack()
            printer_image_canvas.create_image(135,140,image=printer_image,
                                              anchor='se')
            printer_image_canvas.image=printer_image

            #Start drawing ink bars
            ink_frame=tk.Frame(self)
            ink_frame.pack()
            for i, item in enumerate(walk(printer['IP'], 'public',
                                          parent.parent.ink_levels_base_OID)):
                if i==1:
                    #Skip waste toner cartridge
                    continue
                inner_ink_frame=tk.Frame(ink_frame)
                inner_ink_frame.pack(pady=0)
                ink_bar=ttk.Progressbar(inner_ink_frame, value=item[1],
                                       style=parent.parent.styles[i][0])
                ink_level=tk.Label(inner_ink_frame, text="   "+str(item[1])+"%",
                                   foreground='red' if item[1]<=20 else 'black',
                                   bd=0)
                ink_bar.pack(side=tk.LEFT, pady=0)
                ink_level.pack(side=tk.RIGHT, pady=0)
                balloon.bind(ink_bar, parent.parent.styles[i][1])

            #Start grabbing tray info
            tray_names=[]
            tray_current_level=[]
            tray_max_level=[]
            for item in walk(printer['IP'],
                             'public',
                             parent.parent.tray_names_base_OID
                             ):
                tray_names.append(item[1].decode('utf-8').replace('Paper','').replace('Tray 3 (LCT)','LCT'))
            for item in walk(printer['IP'],
                             'public',
                             parent.parent.tray_current_capacity_base_OID
                             ):
                tray_current_level.append(item[1])
            for item in walk(printer['IP'],
                             'public',
                             parent.parent.tray_max_capacity_base_OID
                             ):
                tray_max_level.append(item[1])

            tray_frame=tk.Frame(self)
            tray_frame.pack(pady=(10,5))
            #Start counting info now, now that we can ignore the Bypass Tray
            self.printer_deficit=0
            self.max_capacity=0
            for i, item in enumerate(tray_names):
                if item=='Bypass Tray':
                    continue
                self.max_capacity+=tray_max_level[i]
                self.printer_deficit+=tray_max_level[i]-tray_current_level[i]
                tray_line=tk.Frame(tray_frame, height=20, width=170)
                #Set propogate to 0 so we can manually define frame size
                tray_line.pack_propagate(0)

                tray_info=tk.Frame(tray_line, height=20, width=120)
                tray_info.pack_propagate(0)
                tray_info.pack(side=tk.RIGHT)
                
                tray_label=tk.Label(tray_line, text=item + ": ",
                                    font=(None, 9, 'bold'))
                tray_label.pack(side=tk.LEFT, anchor=tk.W)
                percent=int((tray_current_level[i]/tray_max_level[i])*100)
                tray_percent=tk.Label(tray_info, text=str(percent)+'%',
                                      foreground='red' if percent<=50 else 'black',
                                      anchor=tk.E, width=5)
                tray_current_value=tk.Label(tray_info,
                                            text='('+str(tray_current_level[i]))
                tray_max_value=tk.Label(tray_info, text=str(tray_max_level[i])+')',
                                        anchor=tk.E)
                slash=tk.Label(tray_info, text='/', bd=0)

                tray_percent.pack(side=tk.LEFT)
                tray_max_value.pack(side=tk.RIGHT)
                slash.pack(side=tk.RIGHT)
                tray_current_value.pack(side=tk.RIGHT)
                
                tray_line.pack(anchor=tk.W, fill=tk.BOTH, expand=True)

            #Update the master record of loaded printer deficits/reams needed
            parent.parent.deficit.set(
                parent.parent.deficit.get()+self.printer_deficit
                )
            parent.parent.reams.set(parent.parent.deficit.get()/500)

            #Start drawing the paper fill bar
            self.paper_percentage=int(
                ((self.max_capacity-self.printer_deficit)/self.max_capacity)*100
                )
            bar_width=165
            paper_level_canvas=tk.Canvas(self, width=bar_width, height=20)
            paper_level_canvas.pack(side=tk.BOTTOM)
            paper_level_canvas.create_rectangle(2, 2, bar_width-1, 14,
                                                fill="gainsboro", outline="#757575")
            tray_fill_bar_width=int((self.paper_percentage*bar_width)/100)-1
            #Subtract 1 to avoid edge-to-edge overlap
            paper_level_canvas.create_rectangle(3, 3, tray_fill_bar_width, 14,
                                                fill='darkgray',
                                                width=0
                                                )
            paper_level_canvas.create_text(80,8, font=(None, 8),
                                           text='Paper fill: ' +
                                           str(self.paper_percentage)+'%'
                                           )
            balloon.bind(paper_level_canvas, '-' + str(self.printer_deficit)
                         + ' pages' + ' | -' +
                         str(self.printer_deficit/500) + ' reams')
            
        except Exception as err:
            #Display error image
            no_connection_canvas=tk.Canvas(self, width=155, height=150)
            no_connection_canvas.pack(pady=(100,0))
            no_connection_canvas.create_image(155, 150,
                                              image=parent.parent.no_connection,
                                              anchor=tk.SE)
            no_connection_canvas.image=parent.parent.no_connection
            no_connection_label=tk.Label(self, text="No connection!\n"
                                         "Check the log file for more info",
                                         foreground='red')
            no_connection_label.pack()

            #log error and stack trace to logfile
            log=open('RRM_log_' + parent.parent.current_time + '.txt','a')
            log.write('(' + datetime.datetime.now().strftime('%H:%M') + ') ' +
                      printer['Name'] + ': ' + str(err) + '\n' +
                      traceback.format_exc() + '\n')
                
    def deficit(self):
        #Return the printer's paper deficit to subtract when despawning frame
        return self.printer_deficit
            
if __name__ == "__main__":
    root=tk.Tk()
    #Set resizable to False in X,Y. Trust the program to resize itself :)
    root.resizable(False, False)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
