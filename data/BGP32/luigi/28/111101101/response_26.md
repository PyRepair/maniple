### Bug Explanation
The bug in the `table_exists` function arises from the comparison logic used to check if a table exists in the output of a Hive command. The function checks if the table name is present in the output without considering the formatting of the output. In some cases, the table name might be part of a longer string in the stdout.

### Bug Fix Strategy
To fix the bug, we need to update the comparison logic to ensure that the table name is matched correctly in the output string. Instead of a simple string containment check, we should split the stdout by lines and then check if the table name appears in any of the lines.

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

By splitting the stdout by lines and then checking for the table name in each line, we ensure a more accurate check for the existence of the table in the Hive output. This corrected version should now pass the failing tests.