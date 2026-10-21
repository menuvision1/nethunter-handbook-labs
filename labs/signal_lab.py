"""Generate and analyze a mathematical tone; not an RF capture."""
import math
import cmath
SAMPLE_RATE = 1024
COUNT = 128
TONE = 64
samples = [math.sin(2*math.pi*TONE*n/SAMPLE_RATE) for n in range(COUNT)]
magnitudes = [abs(sum(x*cmath.exp(-2j*math.pi*k*n/COUNT)
                     for n,x in enumerate(samples))) for k in range(COUNT//2+1)]
peak = max(range(len(magnitudes)), key=magnitudes.__getitem__)
if __name__ == '__main__':
    print('origin=synthetic')
    print(f'sample_rate_hz={SAMPLE_RATE}')
    print(f'samples={COUNT}')
    print(f'peak_hz={peak*SAMPLE_RATE//COUNT}')
