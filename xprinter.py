import win32print
import win32ui

def print_yc(text, size_stick):
    x = 20
    y = 20
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC()
    fontdata = win32ui.CreateFont({'name': 'Arial', 'height': size_stick})
    hDC.SelectObject(fontdata)
    hDC.StartDoc("Printing...")
    hDC.StartPage()
    hDC.TextOut(x, y, text)
    hDC.EndPage()
    hDC.EndDoc()