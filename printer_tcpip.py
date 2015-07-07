# coding=utf-8
import socket
from datetime import datetime

import qrcode

LEFT = 0
CENTER = 1
RIGHT = 2


def byte(bits):
    res = 0
    for idx, x in enumerate(bits[::-1]):
        res |= (x << idx)
    return res


class PrinterTCPIP(object):
    HOST = '192.168.123.100'
    PORT = 9100
    sock = None

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
        for res in socket.getaddrinfo(self.HOST, self.PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
            except socket.error as msg:
                self.sock = None
                continue
            try:
                self.sock.connect(sa)
            except socket.error as msg:
                print(msg)
                self.sock.close()
                self.sock = None
                continue
            break
        if self.sock is None:
            return False
        self.sock.send('\x1b@')  # Init printer
        self.sock.send('\x1C\x2E')  # Cancel Kandji
        self.sock.send('\x1Bt\x11')  # Set code page 17 - Cyrillic

        for i in range(3):
            self.sock.send("\x1c\x28\x4c\x02\x00\x42"+chr(48))
            self.sock.send('Mos-Eisley Cantina\n\n')
            self.sock.send("\x1c\x28\x4c\x02\x00\x42" + chr(48))
        printable = self.test_page()
        cyrillic = self.fix_cyrillic(printable)
        self.sock.send(cyrillic)
        self.sock.send('\x1D\x56\x30')  # Cut paper
        self.sock.close()
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

    def qr_code(self, text):

        qr_code = qrcode.QRCode(version=4, box_size=4, border=1)
        qr_code.add_data(text)
        qr_code.make(fit=True)
        qr_matrix = qr_code.get_matrix()

        paper_width = 36
        dot_size = 2
        qr_w = len(qr_matrix)
        qr_h = len(qr_matrix[0])

        qr = []
        for x in range(qr_w):
            for i in range(dot_size):
                qr.append([])
                for y in range(qr_h):
                    qr[x*dot_size+i].extend([1 if qr_matrix[x][y] else 0]*dot_size)
                while len(qr[x*dot_size+i]) % 8 > 0:
                    qr[x * dot_size + i].append(0)
        while len(qr) % 8 >0:
            qr.append([0]*len(qr[0]))

        bytes_lines = []

        for part in range(0, len(qr), 8):
            bytes = []
            bits = []
            for y in range(len(qr[0])):
                for x in range(part, part+8):
                    bit = qr[x][y]
                    bits.append(bit)
                    if len(bits) == 8:
                        bytes.append(byte(bits))
                        bits = []
            bytes_lines.append(bytes)

        qr_command = ""
        for bytes in bytes_lines:
            x = len(bytes)/8
            qr_command += "\x1D\x2A"+chr(x)+"\x01"
            for i in range(len(bytes)):
                qr_command += chr(bytes[i])
            qr_command += "\x1D\x2F\x03"

        return qr_command+"\n\n\n"

    def test_page(self):
        r = "************************************************\n"
        r += self.align(CENTER)
        r += "Магия\n"
        r += "************************************************\n"
        r += self.align(LEFT)
        r += "Дата:   %s\n" % str(datetime.today().strftime("%d.%m.%Y %H:%M"))
        r += "Кассир: %s\n" % "Post Printer masterAlish".encode('utf8')
        r += "-----------------НАИМЕНОВАНИЯ-------------------\n"
        r += "----------------------ЗАКАЗ---------------------\n"
        i = 1
        total_price = 0.0
        for item in range(3):
            r += self.align(LEFT)
            r += "%d. %s (%s)\n" % (i, u"Что-то вкусное и новоеЧто-то вкусное и новоеЧто-то вкусное и новоеЧто-то вкусное и новое".encode("utf8"), u"кг".encode("utf-8"))
            r += self.align(RIGHT)
            count = ("%."+str(2)+"f") % 123.43
            r += "%s x %.2f = %.2f\n" % (count, 34.4, 4000.4)
            total_price += 4000.4
            i += 1
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
        r += " %d%% \n" % 0
        r += self.font_size("\x00")
        r += self.align(LEFT)
        r += "К оплате:\n"
        r += self.align(RIGHT)
        r += self.invert_colors(True)
        r += self.font_size("\x11")
        r += " %.2f \n" % 12123123
        r += self.font_size("\x00")
        r += self.invert_colors(False)
        r += self.emphasized(False)
        r += self.align(LEFT)
        r += "------------------------------------------------\n"
        r += self.align(CENTER)
        r += "  Чек N:%d\n" % 12312
        r += "\x1d\x6b\x02123456789123\x00"
        r += "123456789123"
        r += "\n\n\n"
        return r


PrinterTCPIP().print_receipt()