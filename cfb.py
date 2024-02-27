from encryptmode import EncryptMode

class CFB(EncryptMode):

    def encode(self, text: bytes):
        text = self.check_length(text)
        result = bytearray()
        previous_block = self._c0
        for i in range(0, len(text) - 15, 16):
            previous_block = self.XOR(self.encode_block(previous_block), text[i:i+16])
            result.extend(previous_block)
        return result

    def decode(self, text: bytes):
        result = bytearray()
        previous_block = self._c0
        for i in range(0, len(text) - 15, 16):
            result.extend(self.XOR(self.encode_block(previous_block), text[i:i+16]))
            previous_block = text[i:i+16]
        while result[-1] == 0:
            del result[-1]
        return result