    import xml.etree.ElementTree as ET
    from xml.etree.ElementTree import XML
    import zipfile
    SPREADSHEET_NAMESPACE = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    CELL  = SPREADSHEET_NAMESPACE + 'c'
    VALUE = SPREADSHEET_NAMESPACE + 'v'
    FORMULA  = SPREADSHEET_NAMESPACE + "f"
    document = zipfile.ZipFile(path)
    xml_content = document.read('xl/worksheets/sheet1.xml')
    document.close()
    #tree = XML(xml_content)
    root = ET.fromstring(xml_content)
    print("BEFORE:",xml_content)
    print("root.tag:",root.tag)
    for cell in root.getiterator(CELL):
        children = cell.getchildren()
        formulas = list(filter(lambda child:child.tag==FORMULA,children))
        values   = list(filter(lambda child:child.tag==VALUE,children))
        
        if not formulas and len(values)==1:
            ov = values[0].text
            values[0].text = round_str(values[0].text)
            nv = values[0].text
            print("value: {} --> {}".format(ov,nv))
            continue

        if len(formulas)==1 and len(values)==1:
            # Delete the value
            cell.remove(values[0])

        print(dir(cell))
        print("=======")
    print("AFTER:",dir(root))
    print(ET.dump(root))
