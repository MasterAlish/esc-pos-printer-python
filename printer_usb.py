# coding=utf-8
from datetime import datetime
from escpos import *

LEFT = 0
CENTER = 1
RIGHT = 2


class PrinterUSB(object):
    VENDOR_ID = 0x04b8
    DEVICE_ID = 0x0e15

    def __init__(self):
        self.epson = printer.Usb(self.VENDOR_ID, self.DEVICE_ID)

    def fix_cyrillic(self, string):
        function = {
            'А': '\x80', 'Б': '\x81', 'В': '\x82', 'Г': '\x83', 'Д': '\x84', 'Е': '\x85', 'Ё': '\xf0', 'Ж': '\x86',
            'З': '\x87', 'И': '\x88', 'Й': '\x89', 'К': '\x8a', 'Л': '\x8b', 'М': '\x8c', 'Н': '\x8d', 'О': '\x8e',
            'П': '\x8f', 'Р': '\x90', 'С': '\x91', 'Т': '\x92', 'У': '\x93', 'Ф': '\x94', 'Х': '\x95', 'Ц': '\x96',
            'Ч': '\x97', 'Ш': '\x98', 'Щ': '\x99', 'Ъ': '\x9a', 'Ы': '\x9b', 'Ь': '\x9c', 'Э': '\x9d', 'Ю': '\x9e',
            'Я': '\x9f', 'Ө': '\x8e', 'Ү': '\x93', 'Ң': '\x8d',
            'а': '\xa0', 'б': '\xa1', 'в': '\xa2', 'г': '\xa3', 'д': '\xa4', 'е': '\xa5', 'ё': '\xf1', 'ж': '\xa6',
            'з': '\xa7', 'и': '\xa8', 'й': '\xa9', 'к': '\xaa', 'л': '\xab', 'м': '\xac', 'н': '\xad', 'о': '\xae',
            'п': '\xaf', 'р': '\xe0', 'с': '\xe1', 'т': '\xe2', 'у': '\xe3', 'ф': '\xe4', 'х': '\xe5', 'ц': '\xe6',
            'ч': '\xe7', 'ш': '\xe8', 'щ': '\xe9', 'ъ': '\xea', 'ы': '\xeb', 'ь': '\xec', 'э': '\xed', 'ю': '\xee',
            'я': '\xef', 'ө': '\xae', 'ү': '\xe3', 'ң': '\xad',
        }
        for key, val in function.items():
            string = string.replace(key, val)
        return string

    def print_receipt(self):
        self.epson._raw('\x1b@')  # Init printer
        self.epson._raw('\x1C\x2E')  # Cancel Kandji
        self.epson._raw('\x1Bt\x11')  # Set code page 17 - Cyrillic
        printable = self.get_test_receipt()
        cyrillic = self.fix_cyrillic(printable)
        self.epson._raw(cyrillic)
        self.epson.cut()
        return True

    def align(self, alignment):
        if alignment == 0:
            return "\x1ba\x00"
        elif alignment == 1:
            return "\x1ba\x01"
        else:
            return "\x1ba\x02"

    def invert_colors(self, invert):
        return "\x1dB" + ("\x01" if invert else "\x00")

    def emphasized(self, emphasized):
        return "\x1bE" + ("\x01" if emphasized else "\x00")

    def font_size(self, size):
        return "\x1d\x21" + size

    def get_test_receipt(self):
        r = "************************************************\n"
        r += self.align(CENTER)
        r += " Tatooine Cantina \n"
        r += "************************************************\n"
        r += self.align(LEFT)
        r += "Дата:   %s\n" % str(datetime.now().strftime("%d.%m.%Y %H:%M"))
        r += "Кассир: Асанов Үсөн\n"
        r += "----------------------ЗАКАЗ---------------------\n"
        total_price = 160.0
        for i in range(1, 6):
            r += self.align(LEFT)
            r += "%d. Рис (кг)\n" % i
            r += self.align(RIGHT)
            r += "4 x 10.0 = 40.0\n"
        r += "------------------------------------------------\n"
        r += self.align(LEFT)
        r += self.emphasized(True)
        r += "Всего:\n"
        r += self.align(RIGHT)
        r += self.font_size("\x09")
        r += " %.2f \n" % total_price
        r += self.font_size("\x00")
        r += self.align(LEFT)
        r += "Скидка:\n"
        r += self.align(RIGHT)
        r += self.font_size("\x09")
        r += " 10% \n"
        r += self.font_size("\x00")
        r += self.align(LEFT)
        r += "К оплате:\n"
        r += self.align(RIGHT)
        r += self.invert_colors(True)
        r += self.font_size("\x11")
        r += " 150.0 \n"
        r += self.font_size("\x00")
        r += self.invert_colors(False)
        r += self.emphasized(False)
        r += self.align(LEFT)
        r += "------------------------------------------------\n"
        r += "  Чек N:1312313123\n"
        return r

    def barcode(self, num):
        self.epson.barcode(num, 'EAN13', 64, 2, '', '')

    def qrcode(self, text):
        t = self.epson.qr(text)