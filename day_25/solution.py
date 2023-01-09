import time

with open('aoc_day25.txt', 'r') as f:
    SNAFS = f.read().splitlines()


SNAF_DICT = {'1': 1, '0': 0, '2': 2, '-': -1, '=': -2}
RECTIF = {'4':'2', '3': '1', '2': '0', '1': '-', '0': '='}
INT_DICT = {v: k for k, v in SNAF_DICT.items()}

class PartI:
    def snafu_to_int(self, s:str) -> int:
        bit = 0
        ans = 0
        for c in reversed(s):
            ans += SNAF_DICT[c] * 5 ** bit
            bit += 1
        return ans
    
    def msd(self, n, base):
        k = 0
        while n >= base ** k:
            k += 1
        return k - 1
    
    def regular_base_5(self, n:int) -> str:
        if n == 0:
            return ''
        k = self.msd(n, 5)
        rem = self.regular_base_5(n % 5 ** k)
        return str(n // 5 ** k) + '0' * (k - len(rem)) + rem

    def int_to_snaf(self, n:int) -> str:
        k = self.msd(n, 5)
        k = k + 1 if n // 5 ** k > 2 else k
        n += int('2' * (k + 1), 5)
        s = self.regular_base_5(n)
        return ''.join(RECTIF[c] for c in s)

    def __call__(self):
        s = time.time()
        n = sum(map(self.snafu_to_int, SNAFS))
        ans = self.int_to_snaf(n)
        e = time.time()
        print(f'Answer part I: {ans} in {e - s:.3f}s')

if __name__ == '__main__':
    PartI()()
