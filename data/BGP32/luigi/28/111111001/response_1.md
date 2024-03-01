### Bug Explanation

The bug in the `table_exists` function is related to the comparison made in the return statement. The function checks if the table name is present in the stdout output from running a Hive command, but the comparison is not handling the newline character properly. In the failing test cases, when the stdout includes the table name with a newline character, the comparison fails.

### Bug Fix Strategy

To fix the bug, we need to modify the comparison to properly handle the newline character in the stdout. One approach could be to strip any newline characters from both the table name and the stdout before making the comparison.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.strip().split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

In the corrected version:
1. We use `strip()` to remove any leading or trailing whitespace, including the newline character.
2. We can also modify the comparison to check for the presence of the table name after splitting the stdout by newline characters.
3. We return directly the result of `bool(stdout)` for the case where partition is not None, as an empty stdout will evaluate to False and True otherwise. 

This corrected version should address the bug and make the failing tests pass.