### Bug Explanation:
The bug in the `table_exists` function arises from the comparison of the `table` name with the output `stdout` from the `run_hive_cmd` function. In the current implementation, the function checks if the `table` name is in the `stdout` by performing a substring search, which results in incorrect outcomes.

### Bug Fix Strategy:
To fix the bug, we need to modify the method of checking if the table exists in the output `stdout`. Instead of just performing a substring search, we should split the `stdout` by lines and then check if the `table` name exists on any of those lines.

### Corrected Function:

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

### Justification:
- In the corrected version, we split the `stdout` by lines using `split('\n')` before checking if the `table` name exists in any of the lines.
- For the partition case, we simplified the return to directly return the boolean value of `stdout`, as it either contains the partition information or it does not.

By making these changes, the corrected function now properly checks the existence of the specified table and partitions in the given database and returns the correct boolean values as expected.