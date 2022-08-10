class ViewRotator:
    def colourview(self, view_func):
        def inner(self):
            self.views.append(view_func)
        return inner

    def __init__(self):
        self.views = []
        self.view_index = 0

    def next(self):
        self.view_index = (self.view_index + 1) % len(self.views)

    def current(self):
        return self.views[self.view_index]

    @colourview
    def yellow(self):
        print("yellow!")

    @colourview
    def red(self):
        print("red!")


    @colourview
    def green(self):
        print("green!")


rotator = ViewRotator()

for i in range(0, 10):
    view = rotator.current()
    view()
    rotator.next()
