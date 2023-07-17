# https://stackoverflow.com/questions/58925648/registering-a-function-to-be-called-on-an-event-in-python
class myEvent:
    def __init__(self):
        self.callbacks = list()

    def registerCallback(self, callback):
        self.callbacks.append(callback)

    def call(self):
        for callback in self.callbacks:
            callback()
