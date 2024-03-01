### Bug Explanation
The bug in the `table_exists` function lies in the comparison between the table name and the output from the Hive command which might not match due to case sensitivity. Since Hive is case insensitive, the comparison should be case insensitive as well. The issue reported on GitHub highlights this problem and suggests a solution to make the comparison case insensitive by using lowercase versions of both the table name and the output for comparison.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison to be case insensitive. This can be achieved by converting both the table name and the stdout output to lowercase before comparing them.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                         (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

In the corrected version, both `table` and `stdout` are converted to lowercase before comparison to make it case insensitive. This change aligns with the suggestion provided in the GitHub issue.