from abc import ABCMeta, abstractmethod
from magenta import Magenta


class EncryptMode(Magenta, metaclass=ABCMeta):

    def __init__(self, key, c0):
        key = self.check_key(key)
        super().__init__(key)
        self.check_c0(c0)

    @abstractmethod
    def encode(self, text: bytes):
        '''
        Encode text.
        '''

    @abstractmethod
    def decode(self, text: bytes):
        '''
        Decode text.
        '''

    def check_length(self, text: bytes):
        if len(text) % 16 != 0:
            return text + bytes(16 - len(text) % 16)
        return text

    def check_c0(self, c0):
        if len(c0) < 16:
            self._c0 = c0 + bytes(16 - len(c0))
        elif len(c0) > 16:
            self._c0 = c0[:16]
        else:
            self._c0 = c0

    def check_key(self, key: bytes):
        key_length = len(key)

        if key_length == 16 or key_length == 24 or key_length == 32:
            return key

        if key_length < 16:
            return key + bytes(16 - key_length)

        elif key_length < 24:
            return key + bytes(24 - key_length)

        elif key_length < 32:
            return key + bytes(32 - key_length)
        else:
            return key[:32]
