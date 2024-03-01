### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the presence of the table name in the output received from the `run_hive_cmd` function. The issue arises due to how the function interprets the `stdout` variable, leading to incorrect boolean evaluations.

In the cases provided, when the `stdout` is `'OK'`, the function incorrectly evaluates the expression `stdout and table in stdout`, resulting in `True` even though the table is not in the output ('mytable' in 'OK'). Similarly, in the case where `stdout` is `'OK\nmytable'`, the function evaluates `table in stdout` without considering the newline character, causing it to return `False`.

### Bug Fix Strategy
To fix this bug, we need to modify the condition where we check for the table name in the output of the `run_hive_cmd` function. We should split the `stdout` string by newline characters and then check if the table name is present in the resulting list of lines. This way, we will accurately determine if the table exists in the specified database.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

This corrected version of the `table_exists` function splits the `stdout` by newlines before checking if the table name exists in the result. This modification ensures that the function correctly handles the output from the `run_hive_cmd` function and provides the expected behavior for determining table existence in Hive.