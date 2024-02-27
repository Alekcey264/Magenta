from encryptmode import EncryptMode

class ElectronicCodeBook(EncryptMode):

    def __init__(self, key):
        super().__init__(key, bytes())

    def encode(self, text: bytes):
        text = self.check_length(text)
        result = bytearray()
        for i in range(0, len(text) - 15, 16):
            result.extend(self.encode_block(text[i:i+16]))
        return result

    def decode(self, text: bytes):
        text = self.check_length(text)
        result = bytearray()
        for i in range(0, len(text) - 15, 16):
            result.extend(self.decode_block(text[i:i+16]))
        while result[-1] == 0:
            del result[-1]
        return result