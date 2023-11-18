# I made this because the template GitHub Action config crashes if no tests are pulled.
# I could've removed the line that runs pytest... but maybe this will convince me to write some damn tests?

def func (x):
    return True

def test_answer():
    assert(func(4))