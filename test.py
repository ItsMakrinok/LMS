class A:
    def __init__(self, *args):
        print('init', args)

    def __new__(cls, *args, **kwargs):
        print('new', args)
        return super().__new__(cls)


a1 = A('h')
a2 = A('j')
a3 = A('p')
a4 = A()
print(a1)
