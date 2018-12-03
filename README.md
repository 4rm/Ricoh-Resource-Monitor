# Ricoh-Resource-Monitor
Small program that monitors ink and paper tray levels at work. I got tired of manually checking every individual printer, so this program checks them all at once.

<img src="https://i.imgur.com/QMumyZA.png" alt="Ricoh Resource Monitor screenshot">

<table>
<tr><td><ul>
<b><p align="center">Contents</p></b>
<li><a href="#Tech">Technology used</a></li>
<li><a href="#How">How it works</a></li><ul>
<li><a href="#ink">Ink levels</a></li>
<li><a href="#paper">Paper levels</a></li></ul>
<li><a href="future">Future improvements</a></li>
</ul></td></tr>
</table>

## <a name="Tech">Technology used</a>

<table>
  <tr>
  <td><a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a> (4.6.3) </td>
    <td>Python library for webpage scraping</td>
  </tr>
</table>

## <a name="How">How it works</a>

Each of the main printers we're responsible for at work have their paper and ink levels accessible over the internet. Each statistic has to be scraped in a different way because of how the information is presented.

### <a name="ink">Ink levels</a>

The ink levels are given by a small 1x18 .gif, with its width modified up to 160px to display the currently available amount
<p align="center">
  <img width="50%" height="300" alt="screenshot of an example printer webpage" src="https://i.imgur.com/nKY4v1o.png"><br>
  <i>/images/deviceStTnBarK.gif has a width of 128 out of a possible 160: 80% full</i>
</p>

Using BeautifulSoup, we can scrape the webpage to grab the width of `/images/deviceStTnBarK.gif` and assign it to  our dictionary of printers:

```python
printers[i]['black']=(float(soup.find('img',{"src":"/images/deviceStTnBarK.gif"})['width'])/160)*100
```

It's a bit more difficult to grab the paper tray levels, since they're reported only in images.

### <a name="paper">Paper levels</a>

<p align="center">
  <img width="50%" height="300" alt="screenshot of an example printer webpage" src="http://imgs.fyi/img/6t0w.png"><br>
  <i>Tray status is represented by /images/deviceStP75_16.gif, meaning it is at 75% capacity</i>
</p>

The images needed to be interpreted and returned as numerical values, so the `ignoreTray()` function is used on each call:

```python
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
```

When the program asks for the tray values, it takes the soup object and the tray string we're looking for, and searches for the image filename associated with it. `deviceStPNend16.gif` really means the tray is almost out of paper, but I thought letting it represent 5% was a bit cleaner. 

The program searches over a list of trays, and assigns the results accordingly. I looked through every printer and what its trays were called, and decided where they had the possibility of being stored.

All possible trays, and where I assigned them:

| Key           | Possible Value 
| ------------- |--------------- 
| Tray 1        | Tray 1, Paper Tray 1  
| Tray 2        | Tray 2, Paper Tray 2       
| Tray 3        | Tray 3, Paper Tray 3, Paper Tray 3(LCT)       
| Tray 4        | Paper Tray 4 
| LCT           | LCT 

Then, Beautiful Soup searches through the page for any of the values, and assigned them to the proper key in our printers dict:
```python
printers[i]['Tray 1']=ignoreTray(soup,'Tray 1') if ignoreTray(soup,'Tray 1') != -1 else ignoreTray(soup,'Paper Tray 1')
```
The above line tries to assign a 'Tray 1' value to printers[i]['Tray 1'], but if it isn't found, it will instead assign the 'Paper Tray 1' value since either value is sure to exist. For something like Tray 4, which isn't always sure to exist, a simple if-statement checks with `ignoreTray()` to make sure the tray exists before assigning it to the dictionary.

After we've gotten the ink and paper levels, all that needs to be done is present it prettily (somewhat) in a tkinter GUI, which is really just a bunch of rectangles drawn at "`column=i`"

## <a name="future">Future improvements</a>
<ul>
  <li>Store previous information in a file, to avoid automatic reloading at the start</li>
  <li>Add a way to refresh the information from within the app, instead of restarting it</li>
  <li>Add a way to manually refresh a single printer, to avoid reloading every single printer</li>
  <li>Find a way to refresh data on the actual website without remotely restarting the printer (some of the website info becomes outdated)</li>
</ul>
