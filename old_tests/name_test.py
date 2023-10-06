import inspect

class meow():
    animal = "cat"

    def check(self):
        print(f"The name of the method is: {inspect.stack()[0][3]} ")
        print(meow.check.__qualname__)
        return

a = meow()
a.check()