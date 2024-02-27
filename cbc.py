from encryptmode import EncryptMode

class CipherBlockChaining(EncryptMode):

    def encode(self, text: bytes):
        text = self.check_length(text)
        previous_block = self._c0
        result = bytearray()
        for i in range(0, len(text) - 15, 16):
            previous_block = self.encode_block(self.XOR(text[i:i+16], previous_block))
            result.extend(previous_block)
        return result

    def decode(self, text: bytes):
        text = self.check_length(text)
        previous_block = self._c0
        result = bytearray()
        for i in range(0, len(text) - 15, 16):
            result.extend(self.XOR(self.decode_block(text[i:i+16]), previous_block))
            previous_block = text[i:i+16]
        while result[-1] == 0:
            del result[-1]
        return result