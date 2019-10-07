import binascii
import unittest

from stratatools.manager import Manager
from stratatools.crypto import Desx_Crypto
from stratatools.cartridge_pb2 import Cartridge
from stratatools.checksum import Crc16_Checksum
from google.protobuf.text_format import MessageToString, Merge

CARTRIDGE_TEXT = """
serial_number: 1234.0
material_name: "ABS_RED"
manufacturing_lot: "5678"
manufacturing_date {
  seconds: 978310861
}
last_use_date {
  seconds: 1012615322
}
initial_material_quantity: 11.1
current_material_quantity: 22.2
key_fragment: "4142434441424344"
version: 1
signature: "TESTTEST1"
"""

PACKED_CARTRIDGE_HEX = ("0000000000489340000000000000f03f35363738000000000000"
                        "0000000000000000000001000000650001010101010066000202"
                        "0202020033333333333326400440000000000000414243444142"
                        "4344dc2f00000000000033333333333336400000a8de00000000"
                        "544553545445535431")

class TestManager(unittest.TestCase):
    def test_pack(self):
        cartridge = Cartridge()
        Merge(CARTRIDGE_TEXT, cartridge)

        expected_packed_eeprom = binascii.unhexlify(PACKED_CARTRIDGE_HEX)

        crypto = Desx_Crypto()
        checksum = Crc16_Checksum()
        manager = Manager(crypto, checksum)
        packed_eeprom = manager.pack(cartridge)

        assert expected_packed_eeprom == packed_eeprom
