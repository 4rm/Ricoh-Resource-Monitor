import pprint
import webbrowser
import os
import tkinter as tk
from tkinter import ttk
from puresnmp import walk, get

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller. Found on stackoverflow """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def  myWalk(IP, OID):
    """ Creates a list of StringVar from walk result """
    results=[]
    for row in walk(IP, 'public', OID):
        newResult=tk.StringVar()
        if type(row[1])==bytes:
            value=row[1].decode('utf=8')
        else:
            value=row[1]
        newResult.set(value)
        results.append(newResult)
    if len(results)==0:
        newResult=tk.StringVar()
        newResult.set('')
        results.append(newResult)
    return results

def mySet(varList, walkResults, index):
    """ Updates a list of StringVars with new values, accounting for possible change in list length """
    if len(varList[index])>len(walkResults):
        for i in range(len(varList[index])-len(walkResults)):
            newEntry=tk.StringVar()
            newEntry.set('')
            walkResults.append(newEntry)
    elif len(varList[index])<len(walkResults):
        for i in range(len(walkResults)-len(varList[index])):
            newEntry=tk.StringVar()
            newEntry.set('')
            varList[index].append(newEntry)
    if type(varList[index])==list:
        for q,item in enumerate(varList[index]):
            varList[index][q].set(walkResults[q].get())
    elif type(varList[index])==dict:
        for q,item in enumerate(varList[index]):
            varList[index][item].set(walkResults[q].get())
    return varList

def imgGet(string, printers, index):
    """ Returns proper image name from Model OID and presence of LCT """
    check=0
    if string == 'MP C6004ex':
        return c6004ex
    elif string == 'MP C3504ex':
        return c3504ex
    elif string == 'MP C6503':
        for i,tray in enumerate(printers[index]['Trays']):
            if list(tray.keys())[0] == 'LCT':
                check=1
                return  c6503f
        if check!=1:
            return c6503
            
printers=[
          {'IP':'172.18.181.227','Name':'CI-121'},
          {'IP':'172.18.166.19','Name':'CI202-L'},
          {'IP':'172.18.166.92','Name':'CI202-R'},
          #{'IP':'172.18.181.232','Name':'CI-214'},
          #{'IP':'172.18.181.244','Name':'CI-301'},
          {'IP':'172.18.181.231','Name':'CI-335'},
          #{'IP':'172.18.181.230','Name':'CI-DO'},
          {'IP':'172.18.178.120','Name':'SDW-FL2'},
          {'IP':'172.18.177.204','Name':'ANX-A'},
          {'IP':'172.19.55.10','Name':'ANX-B'},
          #{'IP':'172.18.186.18','Name':'RH-204'},
          ]

ModelOID = '.1.3.6.1.2.1.43.5.1.1.16.1'
SerialOID = '.1.3.6.1.2.1.43.5.1.1.17.1'
InkNames_baseOID = '.1.3.6.1.2.1.43.11.1.1.6'
InkLevels_baseOID = '.1.3.6.1.2.1.43.11.1.1.9.1'
TrayNames_baseOID = '.1.3.6.1.2.1.43.8.2.1.13'
TrayMaxCap_baseOID = '.1.3.6.1.2.1.43.8.2.1.9.1'
TrayCurrCap_baseOID = '.1.3.6.1.2.1.43.8.2.1.10.1'
Err_baseOID = '.1.3.6.1.2.1.43.18.1.1.8.1'

root=tk.Tk()
root.title('Ricoh Resource Monitor')
root.iconbitmap(resource_path('images/icon.ico'))
masterPrinterFrame = tk.Frame(root)

totalMax=0 #Total paper capacity of all printers
deficit=tk.IntVar() #Amount of paper that needs to be refilled
reams=tk.IntVar() #Number of reams needed to refill

s=ttk.Style()
s.theme_use('alt')
s.configure('black.Horizontal.TProgressbar', background='black')
s.configure('cyan.Horizontal.TProgressbar', background='cyan')
s.configure('magenta.Horizontal.TProgressbar', background='magenta')
s.configure('yellow.Horizontal.TProgressbar', background='yellow')

#Create a list of styles to iterate through later
styles=['black.Horizontal.TProgressbar',
        'cyan.Horizontal.TProgressbar',
        'magenta.Horizontal.TProgressbar',
        'yellow.Horizontal.TProgressbar',]

c3504ex = tk.PhotoImage(file=resource_path('images/c3504ex.png')).subsample(4, 4)
c6004ex = tk.PhotoImage(file=resource_path('images/c6004ex.png')).subsample(4, 4)
c6503 = tk.PhotoImage(file=resource_path('images/c6503.png')).subsample(4, 4)
c6503f = tk.PhotoImage(file=resource_path('images/c6503f.png')).subsample(4, 4)
link = tk.PhotoImage(file=resource_path('images/link.png')).subsample(40, 40)

#Define the main index value early so I can define localReload outside of the loop
i=0

#Create the master lists of StringVars. These are the value that will be updated upon a reload
alertVarsList=[]
inkVarsList=[]
currTrayVarsList=[]
trayFillPercent=[]

for i,item in enumerate(printers):
    #Begin gathering information
    printers[i]['Model']=get(printers[i]['IP'], 'public', ModelOID).decode('utf-8')
    
    inkNames=[]
    for row in walk(printers[i]['IP'], 'public', InkNames_baseOID):
        inkNames.append(row[1].decode('utf-8'))  
    Inks=[] #Will hold ink names and current level
    tempInkVarList={}
    for inkIndex in range(len(inkNames)):
        inkLevel=get(printers[i]['IP'], 'public', InkLevels_baseOID+'.'+str(inkIndex+1))
        newInk=tk.StringVar()
        newInk.set(inkLevel)
        tempInkVarList[inkNames[inkIndex]]=newInk
        Inks.append({inkNames[inkIndex]:inkLevel})
    inkVarsList.append(tempInkVarList)
    printers[i]['Inks']=Inks
    
    trayNames=[]
    for row in walk(printers[i]['IP'], 'public', TrayNames_baseOID):
        #if row[1].decode('utf-8') != 'Bypass Tray':
            trayNames.append((row[1].decode('utf-8')).replace('Paper','').replace('Tray 3 (LCT)','LCT'))
    Trays=[] #Will hold tray names and current/max paper levels
    tempTrayVarList={}
    tempTrayPercentList={}
    tempMax=0 #Total paper capacity of current printer
    for trayIndex in range(len(trayNames)):
        currLevel=get(printers[i]['IP'], 'public', TrayCurrCap_baseOID+'.'+str(trayIndex+1))
        maxLevel=get(printers[i]['IP'], 'public', TrayMaxCap_baseOID+'.'+str(trayIndex+1))
        newTray=tk.StringVar()
        newTrayPercent=tk.StringVar()
        newTray.set(currLevel)
        newTrayPercent.set(int((currLevel/maxLevel)*100))
        tempTrayVarList[trayNames[trayIndex]]=newTray
        tempTrayPercentList[trayNames[trayIndex]]=newTrayPercent
        Trays.append({trayNames[trayIndex]:{'maxLevel':maxLevel,'currLevel':currLevel}})
        tempMax+=maxLevel
    currTrayVarsList.append(tempTrayVarList)
    trayFillPercent.append(tempTrayPercentList)
    totalMax+=tempMax
    printers[i]['Trays']=Trays
    
    Alerts=[]
    for row in walk(printers[i]['IP'], 'public', Err_baseOID):
        Alerts.append(row[1].decode('utf-8'))
    printers[i]['Alerts']=Alerts
    alertVarsList.append(myWalk(printers[i]['IP'], Err_baseOID))
    
    #Begin drawing frames
    printerFrame = tk.Frame(masterPrinterFrame, padx=17)
    #printerFrame.grid(row=1, column=i)
    printerFrame.pack(side=tk.LEFT, fill=tk.Y)

    nameFrame = tk.Frame(printerFrame)
    Name=tk.Label(nameFrame, text=printers[i]['Name'], font=(None, 14))
    Name.pack(side=tk.LEFT)
    url='http://' + printers[i]['IP'] + '/web/guest/en/websys/webArch/getStatus.cgi'
    linkButton = tk.Button(nameFrame, command=lambda aurl=url:webbrowser.open(aurl))
    linkButton.config(image=link)
    linkButton.pack(side=tk.RIGHT, padx=5)
    nameFrame.grid(row=0, column=i)
    
    IP=tk.Label(printerFrame, text=printers[i]['IP'], font=(None, 8))
    IP.grid(row=2, column=i)
    Model=tk.Label(printerFrame, text=printers[i]['Model'], font=(None, 9))
    Model.grid(row=1, column=i)

    alertFrame = tk.Frame(printerFrame)
    for item, alert in enumerate(alertVarsList[i]):
        alert = tk.Label(alertFrame, textvariable=alertVarsList[i][item], fg='red')
        alert.pack()
    alertFrame.grid(row=4, column=i)

    printerImageCanvas = tk.Canvas(printerFrame, width=135, height=140)
    printerImageCanvas.grid(row=5, column=i)
    printerImageCanvas.create_image(135, 140, image=imgGet(printers[i]['Model'], printers, i), anchor='se')
    
    inkFrame=tk.Frame(printerFrame)
    counter=0
    for t, ink in enumerate(inkVarsList[i]):
        if t==1:
            #Skip the waste toner 
            continue
        
        Frame=tk.Frame(inkFrame)
        
        Bar=ttk.Progressbar(Frame, variable=inkVarsList[i][ink], style=styles[counter])
        Bar.pack(side=tk.LEFT)
        
        Label=tk.Label(Frame, textvariable=inkVarsList[i][ink], bd=0, width=3, anchor='e',
                       foreground='red' if int(inkVarsList[i][ink].get())<=20 else 'black')
        percent=tk.Label(Frame, text='%', bd=0, foreground='red' if int(inkVarsList[i][ink].get())<=20 else 'black')
        percent.pack(side=tk.RIGHT)
        Label.pack(side=tk.RIGHT)
        
        Frame.pack()
        counter+=1
    inkFrame.grid(row=6, column=i)

    trayFrame=tk.Frame(printerFrame)
    for u, tray in enumerate(currTrayVarsList[i]):
        if tray == 'Bypass Tray':
            #Bypass tray doesn't need to be refilled - no sense monitoring it
            continue
        Frame=tk.Frame(trayFrame)

        trayName=tk.Label(Frame, text=list(printers[i]['Trays'][u].keys())[0]+':', anchor='w', width=6, padx=4)
        trayName.pack(side=tk.LEFT)

        trayLabel=tk.Frame(Frame, height=20, width=110)
        trayLabel.pack_propagate(0)

        percentFrame=tk.Frame(trayLabel, width=0)
        trayPercent=tk.Label(percentFrame, textvariable=trayFillPercent[i][tray], bd=0,
                             foreground='red' if int(trayFillPercent[i][tray].get())<=20 else 'black')
        percentLabel=tk.Label(percentFrame, text='% ', bd=0,
                             foreground='red' if int(trayFillPercent[i][tray].get())<=20 else 'black')
        percentLabel.pack(side=tk.RIGHT)
        trayPercent.pack(side=tk.LEFT)
        percentFrame.pack(side=tk.LEFT)
        
        openParen=tk.Label(trayLabel, text='(')
        trayCurrLevel=tk.Label(trayLabel, textvariable=currTrayVarsList[i][tray], anchor='e', bd=0)
        slash=tk.Label(trayLabel, text='/', anchor='e', bd=0)
        trayMaxLevel=tk.Label(trayLabel, text=str(printers[i]['Trays'][u][tray]['maxLevel']), anchor='e', bd=0)
        closeParen=tk.Label(trayLabel, text=')', bd=0)

        closeParen.pack(side=tk.RIGHT)
        trayMaxLevel.pack(side=tk.RIGHT)
        slash.pack(side=tk.RIGHT)
        trayCurrLevel.pack(side=tk.RIGHT)
        openParen.pack(side=tk.RIGHT)

        
        trayLabel.pack(fill=tk.BOTH, expand=True)
        
        Frame.pack()
    trayFrame.grid(row=7, column=i, pady=20)
    
    print("Done: " + printers[i]['Name'])

def getDeficit():
    deficit.set(0)
    for i in range(len(currTrayVarsList)):
            for key in currTrayVarsList[i]:
                    deficit.set(deficit.get()+int(currTrayVarsList[i][key].get()))
    deficit.set(totalMax-deficit.get()-len(printers)*100) #Subtract 100 per printer to avoid including bypass tray
    reams.set(deficit.get()/500)
    
getDeficit()

def myDivide(currentTray, maxTray):
    for i,item in enumerate(currentTray):
        item.set(int((int(item.get())/maxTray[i])*100))
    return currentTray

def masterReload():
    for masterReloadIndex in range(len(printers)):
        mySet(alertVarsList, myWalk(printers[masterReloadIndex]['IP'],Err_baseOID), masterReloadIndex )
        mySet(inkVarsList, myWalk(printers[masterReloadIndex]['IP'],InkLevels_baseOID), masterReloadIndex )
        mySet(currTrayVarsList, myWalk(printers[masterReloadIndex]['IP'],TrayCurrCap_baseOID), masterReloadIndex )
        mySet(trayFillPercent, myDivide(myWalk(printers[masterReloadIndex]['IP'],TrayCurrCap_baseOID),[list(item.values())[0]['maxLevel'] for item in printers[masterReloadIndex]['Trays']]), masterReloadIndex )
        getDeficit()

infoFrame = tk.Frame(root)

info = tk.Frame(infoFrame)
deficitLabel = tk.Label(info, text='Current deficit: ')
reamLabel = tk.Label(info, text='| Suggested reams: ')
deficitCount = tk.Label(info, textvariable=deficit)
reamCount = tk.Label(info, textvariable=reams)
deficitLabel.pack(side=tk.LEFT)
deficitCount.pack(side=tk.LEFT)
reamLabel.pack(side=tk.LEFT)
reamCount.pack(side=tk.LEFT)
info.pack(side=tk.RIGHT)


masterReloadButton = tk.Button(infoFrame, text='Reload', command=masterReload, bg='light blue', activebackground='steel blue')
masterReloadButton.pack(side=tk.LEFT, padx=2, pady=2)
masterPrinterFrame.pack(side=tk.TOP)

infoFrame.pack(side=tk.LEFT, fill=tk.X, expand=True)

root.mainloop()
