*******
Methods
*******

.. note:: **TODO** Merge this page into the API-description.

Escpos class
------------

Escpos inherits its methods to the printers. the following methods are
defined:

image("image\_name.ext")
^^^^^^^^^^^^^^^^^^^^^^^^

Prints an image. Its adjust the size in order to print it.

* ``image_name.ext`` is the complete file name and location of any image type (jpg, gif, png, bmp)

Raises ``ImageSizeError`` exception.

qr("text")
^^^^^^^^^^

Prints a QR code. The size has been adjusted to Version 4, so it can be
enough small to be printed but also enough big to be read by a smart
phone.

* ``text`` Any text that needs to be QR encoded. It could be a slogan,
  salutation, url, etc.

barcode("code", "barcode\_type", width, height, "position", "font")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prints a barcode.

* ``code`` is an alphanumeric code to be printed as bar code
* ``barcode_type`` must be one of the following type of codes:
   
  * UPC-A
  * UPC-E
  * EAN13
  * EAN8
  * CODE39
  * ITF
  * NW7
   
* ``width`` is a numeric value in the range between (1,255) *Default:* 64
* ``height`` is a numeric value in the range between (2,6) *Default:* 3
* ``position`` is where to place the code around the bars, could be one of the following values:
  
  * ABOVE
  * BELOW
  * BOTH
  * OFF > *Default:* BELOW
   
* ``font`` is one of the 2 type of fonts, values could be:
  
  * A
  * B > *Default:* A Raises ``BarcodeTypeError``, ``BarcodeSizeError``, ``BarcodeCodeError`` exceptions.
    
text("text")
^^^^^^^^^^^^

Prints raw text. Raises ``TextError`` exception.

set("align", "font", "type", width, height)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set text properties.
* ``align`` set horizontal position for text, the possible values are:
   
  * CENTER
  * LEFT
  * RIGHT > > *Default:* left
   
* ``font`` type could be ``A`` or ``B``. *Default:* A
* ``type`` type could be ``B`` (Bold), ``U`` (Underline) or ``normal``. *Default:* normal
* ``width`` is a numeric value, 1 is for regular size, and 2 is twice the standard size. *Default*: 1
* ``height`` is a numeric value, 1 is for regular size and 2 is twice the standard size. *Default*: 1

cut("mode")
^^^^^^^^^^^

Cut paper.
* ``mode`` set a full or partial cut. *Default:* full

**Partial cut is not implemented in all printers.**

cashdraw(pin)
^^^^^^^^^^^^^

Sends a pulse to the cash drawer in the specified pin.

* ``pin`` is a numeric value which defines the pin to be used to send the pulse, it could be 2 or 5. Raises ``CashDrawerError()``

hw("operation")
^^^^^^^^^^^^^^^

Hardware operations.

* ``operation`` is any of the following options:
    
  * INIT
  * SELECT
  * RESET

control("align")
^^^^^^^^^^^^^^^^

Carrier feed and tabs.
* ``align`` is a string which takes any of the following values:
  
  * LF *for Line Feed*
  * FF *for Form Feed*
  * CR *for Carriage Return*
  * HT *for Horizontal Tab*
  * VT *for Vertical Tab*
