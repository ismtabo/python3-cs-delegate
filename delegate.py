#! python3

class Delegate:

    def __init__(self, *funcs):
        self.__funcs=[]
        self.__funcs.extend(funcs)
        self.__iter = None
        
    def __iter__(self):
        self.__iter = iter(self.__funcs)
        return self.__iter
        
    def __next__(self):
        return next(self.__iter)
        
    def __reversed__(self):
        self.__iter = iter(self.__funcs[::-1])
        return self.__iter

    def __add__(self, func):
        if not callable(func):
            raise TypeError("Parameter must be a function or lambda.")
        return Delegate(*(self.__funcs+[func]))
        
    def __iadd__(self, func):
        if not callable(func):
            raise TypeError("Parameter must be a function or lambda.")
        self.__funcs.append(func)
        return self

    def __sub__(self, func):
        if not func in self:
            raise ValueError("Function %s not found at delegate instance" % func.__name__)
        return Delegate(*([f for f in self.__funcs if f is not func]))

    def __isub__(self, func):
        if not func in self:
            raise ValueError("Function %s not found at delegate instance" % func.__name__)
        self.__funcs.remove(func)
        return self
        
    def __call__(self):
        for f in self:
            f()
            
    def __len__(self):
        return len(self.__funcs)
        
    def __contains__(self, func):
        return func in self.__funcs

    def __eq__(self, other):
        return len(self) == len(other) and all(f is fo for f, fo in zip(self, other))
        

if __name__ == '__main__':
    deleg = Delegate()
    
    print("# Test: Delegate::__iadd__")
    print("> Hello world")
    deleg += lambda: print("Hello world")
    deleg()
    
    print("# Test: Delegate::__add__")
    print("> Hello world")
    print("> Launched from deleg1")
    deleg1 = deleg + (lambda: print("Launched from deleg1"))
    deleg1()

    print("# Test: deleg and deleg1 are different instances")
    print("> True")
    print(deleg1 is not deleg)
    

    deleg2 = Delegate()
    
    def f():
         print("Hello from f")
    
    deleg2 += f  

    print("# Test: Delegate::__contains__")
    print("> True")
    print(f in deleg2)

    print("# Test: Delegate::__sub__")
    print("> ")
    deleg3 = deleg2 - f
    deleg3()

    print("# Test: Delegate::__isub__")
    print("> ")
    deleg2 -= f
    deleg2()

    print("# Test: Delegate::__contains__")
    print("> False")
    print(f in deleg2)

    print("# Test: Delegate::__eq__ (deleg2 and deleg3 are equivalents, both empty)")
    print("> True")
    print(deleg2 == deleg3)

    deleg2 += f
    deleg3 += f

    print("# Test: Delegate::__eq__ (deleg2 and deleg3 are equivalents, both contains [f])")
    print("> True")
    print(deleg2 == deleg3)

    print("# Test: Delegate::__iadd__ with not callable argument")
    print("> Failed")
    try:
        deleg2 += 1
    except TypeError:
        print("Failed")

    print("# Test: Delegate::__add__ with not callable argument")
    print("> Failed")
    try:
        deleg3 = deleg2 + 1
    except TypeError:
        print("Failed")
