# Ricoh-Resource-Monitor

[![Build Status](https://travis-ci.org/4rm/Ricoh-Resource-Monitor.svg?branch=master)](https://travis-ci.org/4rm/Ricoh-Resource-Monitor) [![Github Release](https://img.shields.io/github/release/4rm/Ricoh-resource-monitor.svg?color=leaf)](https://github.com/4rm/Ricoh-Resource-Monitor/releases) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

GUI to monitor ink and paper tray levels at work. Values are gathered using SNMP and displayed using TkInter.

<img src="https://i.imgur.com/reFqhNs.png" alt="Ricoh Resource Monitor screenshot">

<table>
<tr><td><ul>
<b><p align="center">Contents</p></b>
<li><a href="#Tech">Technology used</a></li>
<li><a href="#How">How it works</a></li>
<li><a href="#Thanks">Thanks</a></li>
<li><a href="Future">Future improvements</a></li>
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

All of the printers are networked with publicly available SNMP values. As long as the host machine is on the same network, this program grabs the values using generic OIDs and displays them in a nice TkInter window. OIDs used are as follows:

|OID|Value|Method|
|-|-|-|
|Serial Number|.1.3.6.1.2.1.43.5.1.1.17.1|Get|
|Printer Model|.1.3.6.1.2.1.43.11.1.1.6|Get|
|Ink Names|.1.3.6.1.2.1.43.11.1.1.6|Walk|
|Ink Levels|.1.3.6.1.2.1.43.11.1.1.9.1|Walk|
|Tray Names|.1.3.6.1.2.1.43.8.2.1.13|Walk|
|Current Tray Fill|.1.3.6.1.2.1.43.8.2.1.10.1|Walk|
|Max Tray Fill|.1.3.6.1.2.1.43.8.2.1.9.1|Walk|
|Printer Errors|.1.3.6.1.2.1.43.18.1.1.8.1|Walk|

## <a name="Thanks">Thanks</a>
Thanks to takaakiaoki's frozen [Pmw.py module](https://github.com/takaakiaoki/bundlepmw), which was needed to create the standalone .exe with pyinstaller.

## <a name="Future">Future improvements</a>
<ul>
  <li><del>Clean up presentation/alignment</del></li>
  <li><del>Red text when values fall below a certain threshold</del></li>
  <li><del>Tray percentages</del></li>
  <li><del>Move images to dedicated images folder</del></li>
  <li><del>Auto refresh option</del></li>
  <li><del>Avoid having alerts push down printer frame</del></li>
  <li><del>Clean up code, add comments, rename poorly named variables</del></li>
</ul>
