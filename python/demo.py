SPREADSHEET_NAMESPACE = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
CELL  = SPREADSHEET_NAMESPACE + 'c'
VALUE = SPREADSHEET_NAMESPACE + 'v'
FORMULA  = SPREADSHEET_NAMESPACE + "f"

xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac" xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"><dimension ref="A1:C5" /><sheetViews><sheetView tabSelected="1" showRuler="0" zoomScale="85" workbookViewId="0"><selection activeCell="A5" sqref="A5:C5" /></sheetView></sheetViews><sheetFormatPr baseColWidth="10" defaultRowHeight="16" x14ac:dyDescent="0.2" /><sheetData><row r="1" spans="1:3" x14ac:dyDescent="0.2"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c><c r="C1" t="s"><v>2</v></c></row></sheetData><pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3" /></worksheet>"""

import xml.etree.ElementTree as ET
root = ET.fromstring(xml)
print(ET.dump(root))
