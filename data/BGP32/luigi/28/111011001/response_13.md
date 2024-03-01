### Explanation:
The bug in the `table_exists` function lies in the comparison of the `table` name in the `stdout` variable. When checking if the `table` exists in the `stdout` output, the function does a simple string comparison. However, the current implementation does not handle cases where the table name might be part of another string in the `stdout`. For example, in Case 2, the `table` name is `MyTable`, but it is found within the string `'OK\nmytable'`, causing the function to incorrectly return `False`.

### Strategy for fixing the bug:
To fix the bug, we should modify the comparison logic to make sure that the `table` name is matched exactly in the `stdout`. One way to achieve this is to split the `stdout` into lines and check if any line exactly matches the `table` name. This approach will prevent false positives when the `table` name appears within other strings.

### Corrected version of the buggy function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By splitting the `stdout` on newlines and then checking if the `table` exists in any of the resulting lines, we ensure that the function correctly identifies the presence of the table in the output.