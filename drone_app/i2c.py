#TODO: conditionally import smbus based
#import os
#os.uname()
try:
    import smbus
except ImportError:
    from smbus_mock import smbus_mock as smbus


class I2C:

    def __init__(self, address, bus=smbus.SMBus(1)):
        self.address = address
        self.bus = bus
        self.misses = 0

    def writeByte(self, value):
        self.bus.write_byte(self.address, value)

    def write8(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def writeList(self, reg, list):
        self.bus.write_i2c_block_data(self.address, reg, list)

    def readU8(self, reg):
        result = self.bus.read_byte_data(self.address, reg)
        return result

    def readS8(self, reg):
        result = self.bus.read_byte_data(self.address, reg)
        result = result - 256 if result > 127 else result
        return result

    def readU16(self, reg):
        hibyte = self.bus.read_byte_data(self.address, reg)
        result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)
        return result

    def readS16(self, reg):
        hibyte = self.bus.read_byte_data(self.address, reg)
        hibyte = hibyte - 256 if hibyte > 127 else hibyte
        result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)
        return result

    def readList(self, reg, length):
        "Reads a byte array value from the I2C device. The content depends on the device.  The "
        "FIFO read return sequential values from the same register.  For all other, sequestial"
        "regester values are returned"
        result = self.bus.read_i2c_block_data(self.address, reg, length)
        return result


