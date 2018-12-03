import requests
import webbrowser
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup

def ignoreTray(soup,tray):
    try:
        filename = soup.body.find(text=tray).parent.parent.img['src']
        if filename=='/images/deviceStP100_16.gif':
            return 100
        elif filename=='/images/deviceStP75_16.gif':
            return 75
        elif filename=='/images/deviceStP50_16.gif':
            return 50
        elif filename=='/images/deviceStP25_16.gif':
            return 25
        elif filename=='/images/deviceStPNend16.gif':
            return 5
        elif filename=='/images/deviceStPend16.gif':
            return 0
        elif filename=='/images/deviceStError16.gif':
            return 'Error'
    except:
        return -1

def errCheck(tray):
    if bool(type(tray)==int):
        return tray
    elif bool(type(tray)==str):
        return -1

root = tk.Tk()
root.title('Ricoh Resource Monitor')
tk.Label(root, text="Ricoh Resource Monitor", font=(None,15)).grid(row=0, pady=5,columnspan=2)

printers=[
          {'IP':'172.18.181.227','Name':'CI-121'},
          {'IP':'172.18.166.19','Name':'CI202-L'},
          {'IP':'172.18.166.92','Name':'CI202-R'},
##          {'IP':'172.18.181.232','Name':'CI-214'},
##          {'IP':'172.18.181.244','Name':'CI-301'},
          {'IP':'172.18.181.231','Name':'CI-335'},
##          {'IP':'172.18.181.230','Name':'CI-DO'},
          {'IP':'172.18.178.120','Name':'SDW-FL2'},
          {'IP':'172.18.177.204','Name':'ANX-A'},
          {'IP':'172.19.55.10','Name':'ANX-B'},
##          {'IP':'172.18.186.18','Name':'RH-204'},
          ]

for i,item in enumerate(printers):
    url='http://' + item['IP'] + '/web/guest/en/websys/webArch/getStatus.cgi'
    try:
        page=requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        tk.Label(root, text=printers[i]['Name']+' - OFFLINE').grid(row=1,column=i)
        tk.Button(root, text='Link', command=lambda: webbrowser.open(url)).grid(row=2, column=i, pady=(8,10))
        canvas=tk.Canvas(width=140, height=42)
        canvas.grid(row=3, column=i, pady=2)
        continue
    soup=BeautifulSoup(page.text,'html.parser')
    printers[i]['black']=(float(soup.find('img',{"src":"/images/deviceStTnBarK.gif"})['width'])/160)*100
    printers[i]['cyan']=(float(soup.find('img',{"src":"/images/deviceStTnBarC.gif"})['width'])/160)*100
    printers[i]['magenta']=(float(soup.find('img',{"src":"/images/deviceStTnBarM.gif"})['width'])/160)*100
    printers[i]['yellow']=(float(soup.find('img',{"src":"/images/deviceStTnBarY.gif"})['width'])/160)*100
    printers[i]['Tray 1']=ignoreTray(soup,'Tray 1') if ignoreTray(soup,'Tray 1') != -1 else ignoreTray(soup,'Paper Tray 1')
    printers[i]['Tray 2']=ignoreTray(soup,'Tray 2') if ignoreTray(soup,'Tray 2') != -1 else ignoreTray(soup,'Paper Tray 2')
    printers[i]['Tray 3']=max({ignoreTray(soup, 'Tray 3'),ignoreTray(soup,'Paper Tray 3'),ignoreTray(soup,'Paper Tray 3 (LCT)')})
    if ignoreTray(soup,'Paper Tray 4') != -1:
        printers[i]['Tray 4']=ignoreTray(soup,'Paper Tray 4')
    if ignoreTray(soup,'LCT') != -1:
        printers[i]['LCT']=ignoreTray(soup,'LCT')
    tk.Label(root, text=printers[i]['Name']).grid(row=1,column=i)
    tk.Button(root, text='Link', command=lambda aurl=url:webbrowser.open(aurl)).grid(row=2, column=i, pady=(8,10))
    canvas=tk.Canvas(width=140, height=42)
    canvas.grid(row=3, column=i, pady=2)
    canvas.create_rectangle(0,2,100,11,fill='#abb2b9')
    canvas.create_rectangle(0,12,100,21,fill='#abb2b9')
    canvas.create_rectangle(0,22,100,31,fill='#abb2b9')
    canvas.create_rectangle(0,32,100,41,fill='#abb2b9')
    canvas.create_rectangle(0,2,printers[i]['black'],11,fill='#000000')
    canvas.create_rectangle(0,12,printers[i]['cyan'],21,fill='#00FFFF')
    canvas.create_rectangle(0,22,printers[i]['magenta'],31,fill='#FF00FF')
    canvas.create_rectangle(0,32,printers[i]['yellow'],41,fill='#FFFF00')
    canvas.create_text(115,7,text=str(int(printers[i]['black']))+'%',font=(None,8),fill='red' if int(printers[i]['black'])<=20 else 'black')
    canvas.create_text(115,17,text=str(int(printers[i]['cyan']))+'%',font=(None,8),fill='red' if int(printers[i]['cyan'])<=20 else 'black')
    canvas.create_text(115,27,text=str(int(printers[i]['magenta']))+'%',font=(None,8),fill='red' if int(printers[i]['magenta'])<=20 else 'black')
    canvas.create_text(115,37,text=str(int(printers[i]['yellow']))+'%',font=(None,8),fill='red' if int(printers[i]['yellow'])<=20 else 'black')
    papercanvas=tk.Canvas(width=130, height=75)
    papercanvas.grid(row=4, column=i)
    papercanvas.create_text(5,6,text="Tray 1: " + str(printers[i]['Tray 1'])+('%' if errCheck(printers[i]['Tray 1'])>=0 else ''),anchor=tk.W,fill='red' if errCheck(printers[i]['Tray 1']) <=25 else 'black')
    papercanvas.create_text(5,21,text="Tray 2: " + str(printers[i]['Tray 2'])+('%' if errCheck(printers[i]['Tray 2'])>=0 else ''),anchor=tk.W,fill='red' if errCheck(printers[i]['Tray 2']) <=25 else 'black')
    papercanvas.create_text(5,36,text="Tray 3: " + str(printers[i]['Tray 3'])+('%' if errCheck(printers[i]['Tray 3'])>=0 else ''),anchor=tk.W,fill='red' if errCheck(printers[i]['Tray 3']) <=25 else 'black')
    offset=0
    if 'Tray 4' in printers[i]:
        papercanvas.create_text(5,51,text="Tray 4: " + str(printers[i]['Tray 4'])+('%' if errCheck(printers[i]['Tray 4'])>=0 else ''),anchor=tk.W,fill='red' if errCheck(printers[i]['Tray 4']) <=25 else 'black')
        offset=15
    if 'LCT' in printers[i]:
        papercanvas.create_text(5,51+offset,text="LCT: " + str(printers[i]['LCT'])+('%' if errCheck(printers[i]['LCT'])>=0 else ''),anchor=tk.W,fill='red' if errCheck(printers[i]['LCT']) <=25 else 'black')
    print(item['Name'] + " done...")

root.mainloop()
