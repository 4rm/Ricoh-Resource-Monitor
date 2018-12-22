# Ricoh-Resource-Monitor
Small program that monitors ink and paper tray levels at work. I didn't want to manually check every individual printer, so this program checks them all at once.

<img src="https://i.imgur.com/noWoyA2.png" alt="Ricoh Resource Monitor screenshot">

<table>
<tr><td><ul>
<b><p align="center">Contents</p></b>
<li><a href="#Tech">Technology used</a></li>
<li><a href="#How">How it works</a></li>
<li><a href="future">Future improvements</a></li>
</ul></td></tr>
</table>

## <a name="Tech">Technology used</a>

<table>
  <tr>
  <td><a href="https://github.com/exhuma/puresnmp">puresnmp</a> (1.4.2rc1) </td>
    <td>Python SNMPv2 Library </td>
  </tr>
</table>

## <a name="How">How it works</a>

All of the printers are networked with publicly available SNMP values. This program grabs the values and displays them in a nice TkInter window.

## <a name="future">Future improvements</a>
<ul>
  <li>~~Clean up presentation/alignment~~</li>
  <li>Red text when values fall below a certain threshold</li>
  <li>Tray percentages</li>
</ul>
