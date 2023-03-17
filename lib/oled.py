# -*- coding:utf-8 _*-

# Import the SSD1306 module.
import adafruit_ssd1306
import busio
from PIL import Image, ImageDraw, ImageFont
# Import all board pins.
from board import SCL, SDA


class oled:
    """
    See: https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
    """

    def __init__(self, type):
        self._error = ''
        self._initflag = False
        self._type = type
        # init oled
        self._init_oled()

    def get_errorinfi(self):
        return self._error

    def _init_oled(self):
        # Raspberry Pi pin configuration:
        RST = None  # on the PiOLED this pin isnt used
        # Note the following are only used with SPI:
        DC = 23
        SPI_PORT = 0
        SPI_DEVICE = 0

        # Create the I2C interface.
        i2c = busio.I2C(SCL, SDA)
        if 'i2c-128*32' == self._type:
            # 128x32 display with hardware I2C:
            # Create the SSD1306 OLED class.
            # The first two parameters are the pixel width and pixel height.  Change these
            # to the right size for your display!
            # Alternatively you can change the I2C address of the device with an addr parameter:
            # display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)
            self._disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        elif 'i2c-128*64' == self._type:
            # 128x64 display with hardware I2C:
            self._disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        else:
            self._initflag = False
            self._error = 'no this type : %s,just i2c-128*32/i2c-128*64' % self._type
            return False

        # Clear the display.  Always call show after changing pixels to make the display
        # update visible!
        self._disp.fill(0)
        self._disp.show()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self._width = self._disp.width
        self._height = self._disp.height
        self._image = Image.new('1', (self._width, self._height))

        # Get drawing object to draw on image.
        self._draw = ImageDraw.Draw(self._image)

        # Draw a black filled box to clear the image.
        self._draw.rectangle((0, 0, self._width, self._height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        self._top = padding
        bottom = self._height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self._x = 0

        # Load default font.
        self._font = ImageFont.load_default()

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('Minecraftia.ttf', 8)
        return True

    def flush(self, data):
        # Draw a black filled box to clear the image.
        self._draw.rectangle((0, 0, self._width, self._height), outline=0, fill=0)

        # Write two lines of text.
        self._draw.text((self._x, self._top), data[0], font=self._font, fill=255)
        self._draw.text((self._x, self._top + 8), data[1], font=self._font, fill=255)
        self._draw.text((self._x, self._top + 16), data[2], font=self._font, fill=255)
        self._draw.text((self._x, self._top + 24), data[3], font=self._font, fill=255)
        if 'i2c-128*64' == self._type:
            self._draw.text((self._x, self._top + 32), data[4], font=self._font, fill=255)
            self._draw.text((self._x, self._top + 40), data[5], font=self._font, fill=255)
            self._draw.text((self._x, self._top + 48), data[6], font=self._font, fill=255)
            self._draw.text((self._x, self._top + 56), data[7], font=self._font, fill=255)
        # Display image.
        self._disp.image(self._image)
        self._disp.show()

        return True
