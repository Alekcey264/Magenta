class Magenta():

    def __init__(self, key: bytes):
        self._s = self.generate_S_block()
        self._key = key
        self.get_key_order(key)

    def get_key_order(self, key: bytes):
        key_len = len(key)
        assert key_len == 16 or key_len == 24 or key_len == 32
        if key_len == 16:
            k1, k2 = self._key[:8], self._key[8:]
            self._key_order = (k1, k1, k2, k2, k1, k1)

        elif key_len == 24:
            k1, k2, k3 = key[:8], key[8:16], key[16:24]
            self._key_order = (k1, k2, k3, k3, k2, k1)

        elif key_len == 32:
            k1, k2, k3, k4 = key[:8], key[8:16], key[16:24], key[24:32]
            self._key_order = (k1, k2, k3, k4, k4, k3, k2, k1)

    def encode_block(self, input_block: bytes):
        work_block = input_block
        for k in self._key_order:
            work_block = self.FK(k, work_block)

        return work_block

    def decode_block(self, input_block: bytes):
        return self.V(self.encode_block(self.V(input_block)))
    
    @staticmethod
    def XOR(b1: bytes, b2: bytes):
        assert len(b1) == 16 and len(b2) == 16

        result = bytearray()
        for i in range(16):
            result.append(b1[i] ^ b2[i])

        return result
    
    def F(self, input_block: bytes):
        '''
        F полагают равной первым 8 байтам от S(C(3,(X2Kn))
        '''
        assert len(input_block) == 16
        result = self.S(self.C(3, input_block))

        return result[:8]

    def FK(self, key: bytes, input_block: bytes):
        '''
        Раундовая функция
        '''
        assert len(key) == 8 and len(input_block) == 16

        x1, x2 = input_block[:8], input_block[8:]

        work_block = self.F(x2 + key)
        array = bytearray()
        for i in range(8):
            array.append(work_block[i] ^ x1[i])

        return x2 + array

    @staticmethod
    def generate_S_block():
        '''
        Генерирует S блок
        '''
        el = 1
        S_array = [1]
        for _ in range(255):
            el <<= 1
            if el > 255:
                el = (0xFF & el) ^ 101
            S_array.append(el)
        S_array[255] = 0

        return S_array

    def f(self, x: int):
        '''
        Возвращает элемент с номером x в S-блоке
        '''
        assert 0 <= x <= 255

        return self._s[x]

    def A(self, x: int, y: int):
        '''
        f(x ⊕ f(y))
        '''
        assert 0 <= x <= 255 and 0 <= y <= 255

        return self.f(x ^ self.f(y))

    def PE(self, x: int, y: int):
        '''
        (A(x, y)A(y, x)) — конкатенирует результаты A(x, y) и A(y, x)
        '''
        assert 0 <= x <= 255 and 0 <= y <= 255

        return (self.A(x, y), self.A(y, x))

    def P(self, array_x: bytes):
        '''
        X=X0X1...X14X15
        (PE(X0,X8)PE(X1,X9)...PE(X6,X14)PE(X7,X15)) - конкатенирует результаты PE(Xi,Xi+8) i=0...7, Xi имеет размер 1 байт.
        '''
        assert len(array_x) == 16

        result = bytearray()
        for i in range(8):
            result.extend(self.PE(array_x[i], array_x[i+8]))

        return result

    def T(self, array_x: bytes):
        '''
        П(П(П(П(X)))) — применяет к X 4 раза функцию П.
        '''
        assert len(array_x) == 16

        result = array_x
        for _ in range(4):
            result = self.P(result)

        return result

    @staticmethod
    def S(array_x: bytes):
        '''
        (X0X2X4…X14X1X3X5…X15) — выполняет перестановку байтов X: сначала записываются байты с четным порядковым номером затем с нечетным.
        '''
        assert len(array_x) == 16

        order = [0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15]
        result = bytearray()
        for item in order:
            result.append(array_x[item])

        return result

    def C(self, k: int, array_x: bytes):
        '''
        Рекурсивная функция:
        С(1,X) = T(X))
        С(k,X) = T(X ⊕ S(C(k-1,X)))
        '''
        assert k >= 1 and len(array_x) == 16

        if k == 1:
            return self.T(array_x)

        work_block = self.S(self.C(k-1, array_x))

        result = self.XOR(array_x, work_block)

        return self.T(result)

    @staticmethod
    def V(array: bytes):
        '''
        Меняет местами первую и вторую половины
        '''
        assert len(array) == 16

        return array[8:] + array[:8]
    