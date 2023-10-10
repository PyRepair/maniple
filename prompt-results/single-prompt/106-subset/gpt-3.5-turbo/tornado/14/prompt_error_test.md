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



The test error on command line is following:

======================================================================
ERROR: test_force_current (tornado.test.ioloop_test.TestIOLoopCurrent)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:14/tornado/test/ioloop_test.py", line 443, in test_force_current
    self.io_loop = IOLoop(make_current=True)
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:14/tornado/util.py", line 221, in __new__
    instance.initialize(*args, **init_kwargs)
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:14/tornado/platform/kqueue.py", line 91, in initialize
    super(KQueueIOLoop, self).initialize(impl=_KQueue(), **kwargs)
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:14/tornado/ioloop.py", line 664, in initialize
    super(PollIOLoop, self).initialize(**kwargs)
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/tornado:14/tornado/ioloop.py", line 253, in initialize
    raise RuntimeError("current IOLoop already exists")
RuntimeError: current IOLoop already exists

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)



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


