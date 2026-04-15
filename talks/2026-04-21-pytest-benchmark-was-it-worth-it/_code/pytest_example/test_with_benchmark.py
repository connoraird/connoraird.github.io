import time
import os

def inc_slow(x):
    if (os.getenv("SLOW")):
        time.sleep(1)
    return x + 1

def test_inc(benchmark):
    result = benchmark(inc_slow, 3)
    assert result == 4
