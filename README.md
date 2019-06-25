# Ricoh-Resource-Monitor
GUI to monitor ink and paper tray levels at work. Values are gathered using SNMP and displayed using TkInter.

<img src="https://i.imgur.com/reFqhNs.png" alt="Ricoh Resource Monitor screenshot">

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
  <tr>
  <td><a href="https://github.com/takaakiaoki/bundlepmw">takaakiaoki's bundlepmw</a></td>
    <td>Modernized Pmw bundle</td>
  </tr>
</table>

## <a name="How">How it works</a>

All of the printers are networked with publicly available SNMP values. As long as the host machine is on the same network, this program grabs the values using generic OIDs and displays them in a nice TkInter window.

Executable made with the help of takaakiaoki's frozen [Pmw.py module](https://github.com/takaakiaoki/bundlepmw), which was needed to create the standalone .exe with pyinstaller.

## <a name="future">Future improvements</a>
<ul>
  <li><del>Clean up presentation/alignment</del></li>
  <li><del>Red text when values fall below a certain threshold</del></li>
  <li><del>Tray percentages</del></li>
  <li><del>Move images to dedicated images folder</del></li>
  <li><del>Auto refresh option</del></li>
  <li><del>Avoid having alerts push down printer frame</del></li>
  <li><del>Clean up code, add comments, rename poorly named variables</del></li>
</ul>
