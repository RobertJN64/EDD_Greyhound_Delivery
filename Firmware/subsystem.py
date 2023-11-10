import threading

class Subsystem:
    def __init__(self):
        print(f"Creating a subsystem of class: {self.__class__}")
        self.should_kill = False
        self.setup()
        print(f"Subsystem setup complete, starting subsystem loop")
        threading.Thread(target=self.loop).start()

    def setup(self):
        pass

    def loop(self):
        pass
