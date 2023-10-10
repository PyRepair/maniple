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



The raised issue description for this bug is:
ioloop.py(line 252) is None or not None

line 252， IOLoop.current(instance=False) is None。why then raise "already exists"?