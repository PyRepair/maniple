You need to fix a bug in a python code snippet, which failed on test and got 'ValueError' on line 5.

The buggy source code is following:

    def is_in_obj(gpr) -> bool:
        if not hasattr(gpr, "name"):
            return False
        try:
            return gpr is obj[gpr.name]
        except (KeyError, IndexError):
            return False

And the raised issue description for this bug is 'Bug in Series.groupby would raise ValueError when grouping by PeriodIndex level'.


You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.