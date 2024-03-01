### Bug Explanation
The bug in the `table_exists` function arises from the condition check on the `stdout` variable. In the first part of the `if` block, the code checks if `stdout` is not empty and if the `table` exists in it. However, this check is incorrect because even if the `table` exists in `stdout`, the condition will be false if `stdout` itself is not empty.

### Bug Fix Strategy
To fix the bug, we need to adjust the condition check on `stdout` in the first part of the `if` block. We should check if `table` exists in `stdout` only when `stdout` is not empty.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout.strip():
            return table in stdout.splitlines()
        else:
            return False
```

The corrected version includes `stdout.strip()` to account for cases where `stdout` might contain whitespace characters that should be removed. Additionally, it splits the lines in `stdout` to properly check if `table` exists in the output.