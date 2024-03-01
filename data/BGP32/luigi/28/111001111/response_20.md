### Bug Explanation:
The bug in the `table_exists` function arises from the case sensitivity when comparing the table name in the `stdout` obtained from running the Hive command with the input table name. Hive is case insensitive, so comparing the table name in lowercase would prevent issues where the table name's case differs in the Hive output.

### Bug Fix Strategy:
To fix the bug, we need to ensure that we compare the table name in lowercase form to handle case-insensitive matching between the input table name and the table names retrieved from Hive.

### Corrected Function:
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

The corrected function ensures case-insensitive comparison by converting both the table name and the Hive output to lowercase before performing the comparison. This fix aligns with the issue reported on GitHub and addresses the case sensitivity problem in the `table_exists` function.