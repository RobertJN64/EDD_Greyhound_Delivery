import threading

class Subsystem:
    def __init__(self):
        print(f"Created a subsystem of class: {self.__class__}")
        self._should_kill = False
        threading.Thread(target=self.loop).start()

    def loop(self):
        print(f"Did you forget to override subsystem loop for {self.__class__}")

    def kill(self):
        """Trigger an async kill"""
        self._should_kill = True
