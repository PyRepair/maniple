This error is caused by the misuse of the boolean condition in line "if IOLoop.current(instance=False) is None:". Here, a RuntimeError is expected to be raised when IOLoop already exists, but as per the current condition, the error is being raised when it does not exist. A simple fix to this code will be switching the conditional statements in make_current's if statement.

The fixed patch for the function would look like this:

    def initialize(self, make_current=None):
        if make_current is None:
            if IOLoop.current(instance=False) is not None:
                self.make_current()
        elif make_current:
            if IOLoop.current(instance=False) is not None:
                raise RuntimeError("current IOLoop already exists")
            self.make_current()


So, now the program will raise the 'current IOLoop already exists' error if the IOLoop object already exists when make_current is set to True.