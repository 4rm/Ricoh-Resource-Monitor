# Ricoh-Resource-Monitor

[![Build Status](https://travis-ci.org/4rm/Ricoh-Resource-Monitor.svg?branch=master)](https://travis-ci.org/4rm/Ricoh-Resource-Monitor) [![Github Release](https://img.shields.io/github/release/4rm/Ricoh-resource-monitor.svg?color=leaf)](https://github.com/4rm/Ricoh-Resource-Monitor/releases) [![Github All Releases](https://img.shields.io/github/downloads/4rm/Ricoh-Resource-Monitor/total.svg)]() [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

GUI to monitor ink and paper tray levels at work. Values are gathered using SNMP and displayed using TkInter.

<img src="https://i.imgur.com/lmd6ghC.png" alt="Ricoh Resource Monitor screenshot">

<table>
<tr><td><ul>
<b><p align="center">Contents</p></b>
<li><a href="#Tech">Technology used</a></li>
<li><a href="#How">How it works</a></li>
  <ul><li><a href="Editing">Editing printer list</a></li></ul>
<li><a href="#Known">Known Issues</a></li>
<li><a href="#Thanks">Thanks</a></li>
</ul></td></tr>
</table>

## <a name="Tech">Technology used</a>

<table>
  <tr>
  <td><a href="https://github.com/exhuma/puresnmp">puresnmp</a> (1.5.1) </td>
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

### <a name="Editing">Editing printer list</a>

You can add or remove a printer by going to `File -> Edit Printer List`

<img src="https://user-images.githubusercontent.com/3399474/117365336-26d44780-ae8d-11eb-8d9e-06d80bc00340.png" alt="Printer list screenshot" width=450>

To add a printer, the `Name`, `IP`, and `Default` fields are required; the `Serial` and `EID` fields are not, so their spaces can be left blank, eg: `123.12.123.123,My Printer,,,True`. The `Default` field determines whether the printer is loaded by default when launching the program.

`Reset Field` will return the printer list to its default state as of 5/6/21.

## <a name="Known">Known Issues</a>

- Printers will not report paper level changes unless they've been woken from Energy Saver Mode
- Some trays are split into left- and right-hand compartments, but Ricoh reports their fill levels as one value
- Log file may not be created in some locations unless RRM is launched as administrator

## <a name="Thanks">Thanks</a>
Thanks to takaakiaoki for their frozen [Pmw.py module](https://github.com/takaakiaoki/bundlepmw), which was needed to create the standalone .exe with pyinstaller.
