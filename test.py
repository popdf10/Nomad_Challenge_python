a = 1
b = 'b'
c = True
d = 3.14
e = "Hello"
f = "World"


def swap():
    global e
    global f
    temp = e
    e = f
    f = temp


print(e, f)
swap()
print(e, f)
