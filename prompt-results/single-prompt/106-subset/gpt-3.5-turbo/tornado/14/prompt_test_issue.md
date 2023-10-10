You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

    def initialize(self, make_current=None):
        if make_current is None:
            if IOLoop.current(instance=False) is None:
                self.make_current()
        elif make_current:
            if IOLoop.current(instance=False) is None:
                raise RuntimeError("current IOLoop already exists")
            self.make_current()



The test source code is following:

# automatically set as current.
class TestIOLoopCurrent(unittest.TestCase):
    def setUp(self):
        self.io_loop = None
        IOLoop.clear_current()

    def tearDown(self):
        if self.io_loop is not None:
            self.io_loop.close()

    def test_default_current(self):
        self.io_loop = IOLoop()
        # The first IOLoop with default arguments is made current.
        self.assertIs(self.io_loop, IOLoop.current())
        # A second IOLoop can be created but is not made current.
        io_loop2 = IOLoop()
        self.assertIs(self.io_loop, IOLoop.current())
        io_loop2.close()

    def test_non_current(self):
        self.io_loop = IOLoop(make_current=False)
        # The new IOLoop is not initially made current.
        self.assertIsNone(IOLoop.current(instance=False))
        def f():
            # But it is current after it is started.
            self.current_io_loop = IOLoop.current()
            self.io_loop.stop()
        self.io_loop.add_callback(f)
        self.io_loop.start()
        self.assertIs(self.current_io_loop, self.io_loop)
        # Now that the loop is stopped, it is no longer current.
        self.assertIsNone(IOLoop.current(instance=False))

    def test_force_current(self):
        self.io_loop = IOLoop(make_current=True)
        self.assertIs(self.io_loop, IOLoop.current())
        with self.assertRaises(RuntimeError):
            # A second make_current=True construction cannot succeed.
            IOLoop(make_current=True)
        # current() was not affected by the failed construction.
        self.assertIs(self.io_loop, IOLoop.current())



The raised issue description for this bug is:
ioloop.py(line 252) is None or not None

line 252， IOLoop.current(instance=False) is None。why then raise "already exists"?