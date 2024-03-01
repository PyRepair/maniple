### Bug Explanation
The bug in the `table_exists` function arises from the comparison between the expected table name and the output from the `run_hive_cmd` function. Specifically, the comparison `table in stdout` is case-sensitive, which causes issues when the table names do not match exactly due to case differences.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison to be case-insensitive when checking if the table exists in the output from `run_hive_cmd`.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.splitlines())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                          (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

In the corrected version, we convert both the expected table name and the output from `run_hive_cmd` to lowercase to ensure a case-insensitive comparison. This should resolve the bug and make the `table_exists` function more robust.