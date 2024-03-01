### Bug Explanation
The bug in the `table_exists` function lies in the logic used to check if a table exists in the database. In the provided implementation, the function returns `False` only if the `stdout` is empty, otherwise it returns `True`. The bug occurs when the `stdout` contains the table name, but the function incorrectly returns `False`.

### Bug Location
The bug is located in the `if stdout:` condition where the function should return `True` if the table is found in the output but instead returns `False`.

### Bug Cause
The bug occurs due to incorrect handling of the condition to determine if the table exists in the database. The function incorrectly returns `False` even if the table is found in the `stdout` output.

### Fix Strategy
To fix the bug, we need to modify the logic in the `if stdout:` condition to correctly identify when the table exists in the database and return `True` in that case.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return table in stdout
``` 

By changing the return value in the `else` block to `return table in stdout`, we properly handle the case where the table is found in the `stdout`. This corrected version should pass the failing test cases.