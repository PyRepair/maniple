### Bug Explanation
The bug in the `table_exists` function lies in the comparison logic for checking if the table exists. In the `else` block of the function, the condition checks if `stdout` has any value, regardless of the actual content of `stdout`. This leads to a faulty evaluation, causing the function to always return `True` in the `else` block.

### Bug Fix Strategy
To fix the bug, we need to adjust the comparison logic to correctly interpret the output in both branches of the function. We should consider the presence of the table name in the `stdout` output for the `if` block and check the existence of non-empty content in `stdout` for the `else` block.

### Corrected Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

The corrected version ensures that the function correctly returns `False` if `stdout` is empty in the `else` block, fixing the bug that caused incorrect evaluation and always returning `True`.