import pytest

# src code
def inc(x):
    return x + 1

# Basic example
def test_inc():
    assert inc(3) == 4

# Example with fixtures
@pytest.fixture(scope="session")
def inputs():
    return [1,2,3,4,5,6,7,8,9,10]

@pytest.fixture(scope="session")
def outputs():
    return [2,3,4,5,6,7,8,9,10,11]

def test_inc_with_fixtures(inputs, outputs):
    for i in range(len(inputs)):
      assert inc(inputs[i]) == outputs[i]
