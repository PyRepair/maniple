You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

def cli_bool_option(params, command_option, param, true_value='true', false_value='false', separator=None):
    param = params.get(param)
    if param is None:
        return []
    assert isinstance(param, bool)
    if separator:
        return [command_option + separator + (true_value if param else false_value)]
    return [command_option, true_value if param else false_value]



The test error on command line is following:

======================================================================
FAIL: test_cli_bool_option (test.test_utils.TestUtil)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/youtube-dl:17/test/test_utils.py", line 1187, in test_cli_bool_option
    {}, '--check-certificate', 'nocheckcertificate', 'false', 'true', '='),
  File "/Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/youtube-dl:17/youtube_dl/utils.py", line 2736, in cli_bool_option
    assert isinstance(param, bool)
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.006s

FAILED (failures=1)




The test source code is following:

    def test_cli_valueless_option(self):
        self.assertEqual(
            cli_bool_option(
                {'nocheckcertificate': True}, '--no-check-certificate', 'nocheckcertificate'),
            ['--no-check-certificate', 'true'])
        self.assertEqual(
            cli_bool_option(
                {'nocheckcertificate': True}, '--no-check-certificate', 'nocheckcertificate', separator='='),
            ['--no-check-certificate=true'])
        self.assertEqual(
            cli_bool_option(
                {'nocheckcertificate': True}, '--check-certificate', 'nocheckcertificate', 'false', 'true'),
            ['--check-certificate', 'false'])
        self.assertEqual(
            cli_bool_option(
                {'nocheckcertificate': True}, '--check-certificate', 'nocheckcertificate', 'false', 'true', '='),
            ['--check-certificate=false'])
        self.assertEqual(
            cli_bool_option(
                {'nocheckcertificate': False}, '--check-certificate', 'nocheckcertificate', 'false', 'true'),
            ['--check-certificate', 'true'])
        self.assertEqual(
            cli_bool_option(
                {'nocheckcertificate': False}, '--check-certificate', 'nocheckcertificate', 'false', 'true', '='),
            ['--check-certificate=true'])
        self.assertEqual(
            cli_bool_option(
                {}, '--check-certificate', 'nocheckcertificate', 'false', 'true', '='),
            [])


