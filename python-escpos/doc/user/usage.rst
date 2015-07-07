*****
Usage
*****

Define your printer
-------------------

USB printer
^^^^^^^^^^^

Before start creating your Python ESC/POS printer instance, you must see
at your system for the printer parameters. This is done with the 'lsusb'
command.

First run the command to look for the "Vendor ID" and "Product ID", then
write down the values, these values are displayed just before the name
of the device with the following format:

::

    xxxx:xxxx

Example:

::

    # lsusb
    Bus 002 Device 001: ID 04b8:0202 Epson ...

Write down the the values in question, then issue the following command
so you can get the "Interface" number and "End Point"

::

    # lsusb -vvv -d xxxx:xxxx | grep iInterface
        iInterface              0
    # lsusb -vvv -d xxxx:xxxx | grep bEndpointAddress | grep OUT
          bEndpointAddress     0x01  EP 1 OUT

The first command will yields the "Interface" number that must be handy
to have and the second yields the "Output Endpoint" address.

**USB Printer initialization**

::

    Epson = printer.Usb(0x04b8,0x0202)

By default the "Interface" number is "0" and the "Output Endpoint"
address is "0x01", if you have other values then you can define with
your instance. So, assuming that we have another printer where in\_ep is
on 0x81 and out\_ep=0x02, then the printer definition should looks like:

**Generic USB Printer initialization**

::

    Generic = printer.Usb(0x1a2b,0x1a2b,0,0x81,0x02)

Network printer
^^^^^^^^^^^^^^^

You only need the IP of your printer, either because it is getting its
IP by DHCP or you set it manually.

**Network Printer initialization**

::

    Epson = printer.Network("192.168.1.99")

Serial printer
^^^^^^^^^^^^^^

Must of the default values set by the DIP switches for the serial
printers, have been set as default on the serial printer class, so the
only thing you need to know is which serial port the printer is hooked
up.

**Serial printer initialization**

::

    Epson = printer.Serial("/dev/tty0")

Other printers
^^^^^^^^^^^^^^

Some printers under /dev can't be used or initialized with any of the
methods described above. Usually, those are printers used by printcap,
however, if you know the device name, you could try the initialize
passing the device node name.

::

    Epson = printer.File("/dev/usb/lp1")

The default is "/dev/usb/lp0", so if the printer is located on that
node, then you don't necessary need to pass the node name.

Define your instance
--------------------

The following example demonstrate how to initialize the Epson TM-TI88IV
on USB interface

::

    from escpos import *
    """ Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
    Epson = printer.Usb(0x04b8,0x0202)
    # Print text
    Epson.text("Hello World\n")
    # Print image
    Epson.image("logo.gif")
    # Print QR Code
    Epson.qr("You can readme from your smartphone")
    # Print barcode
    Epson.barcode('1324354657687','EAN13',64,2,'','')
    # Cut paper
    Epson.cut()

How to update your code for USB printers
----------------------------------------

Old code

::

    Epson = escpos.Escpos(0x04b8,0x0202,0)

New code

::

    Epson = printer.Usb(0x04b8,0x0202)

Nothe that "0" which is the interface number is no longer needed.
