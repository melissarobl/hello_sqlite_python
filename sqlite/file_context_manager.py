## Not just databases - files can use context managers too

with open('test.txt', 'w') as f:
    f.write('hello context manager')
    # no need to close - the context manager does that for us

# This is equivalent

f = open('text2.txt', 'w')
f.write('hello file without context manager')
f.close()
