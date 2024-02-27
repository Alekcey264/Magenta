from encryptmode import EncryptMode

class OutputFeedBack(EncryptMode):

    def encode(self, text: bytes):
        text = self.check_length(text)
        result = bytearray()
        previous_block = self._c0
        for i in range(0, len(text) - 15, 16):
            previous_block = self.encode_block(previous_block)
            result.extend(self.XOR(previous_block, text[i:i+16]))
        return result

    def decode(self, text: bytes):
        text = self.check_length(text)
        result = self.encode(text)
        while result[-1] == 0:
            del result[-1]
        return result