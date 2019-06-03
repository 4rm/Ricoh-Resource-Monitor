# Ricoh-Resource-Monitor
GUI to monitor ink and paper tray levels at work. All printers are checked at once to avoid manually checking each one.

<img src="https://i.imgur.com/gnVRCim.png" alt="Ricoh Resource Monitor screenshot">

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
  <li><del>Clean up presentation/alignment</del></li>
  <li><del>Red text when values fall below a certain threshold</del></li>
  <li><del>Tray percentages</del></li>
  <li><del>Move images to dedicated images folder</del></li>
  <li><del>Auto refresh option</del></li>
  <li><del>Avoid having alerts push down printer frame<del></li>
  <li>Clean up code, add comments, rename poorly named variables</li>
</ul>
