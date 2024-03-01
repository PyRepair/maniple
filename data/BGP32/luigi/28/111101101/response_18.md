### Bug Explanation
The bug in the `table_exists` function arises from the condition where it checks if the table is in the `stdout` string returned by the `run_hive_cmd` function. The bug occurs because the check is done directly on the string without splitting it into lines, resulting in incorrect output evaluation.

In the failing test cases, the buggy function fails to correctly handle the `stdout` string from the `run_hive_cmd` function, leading to incorrect evaluation of whether the table exists or not.

### Bug Fix Strategy
To fix the bug, the `stdout` string returned by the `run_hive_cmd` function needs to be split into lines before checking if the table exists in it. This way, each line of the output can be evaluated independently to accurately determine the existence of the table.

### Corrected Version of the Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

By splitting the `stdout` string by lines and then performing the table existence check, the corrected function ensures that the presence of the table is accurately determined, fixing the bug.