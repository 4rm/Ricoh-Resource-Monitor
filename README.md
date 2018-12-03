# Ricoh-Resource-Monitor
Small program that monitors ink and paper tray levels at work. I got tired of manually checking every individual printer, so this program checks them all at once.

<img src="https://i.imgur.com/QMumyZA.png" alt="Ricoh Resource Monitor screenshot">

<table>
<tr><td><ul>
<b><p align="center">Contents</p></b>
<li><a href="#Tech">Technology used</a></li>
<li><a href="#How">How it works</a></li>
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

<p align="center">
  <img width="50%" height="300" alt="screenshot of an example printer webpage" src="http://imgs.fyi/img/6t0w.png"><br>
  <i>Tray status is represented by /images/deviceStP75_16.gif, meaning it is at 75% capacity</i>
</p>

The images needed to be interpreted and returned as numerical values, 
