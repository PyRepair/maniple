## Bug Explanation
The bug in the `table_exists` function is caused by the way the function checks for the existence of a table in the Hive database. In the first case, the check `return stdout and table in stdout` is being incorrectly evaluated because the `stdout` only contains the output `OK` and not the actual table names. This results in a false negative when checking for table existence.

Additionally, in the second case, the check `return True if stdout else False` is redundant and can be simplified.

## Bug Fix
To fix the bug, we need to modify the way the function checks for the table existence. We can extract the table names from the `stdout` and then perform the existence check.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and any(table == line.strip() for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

This corrected version properly extracts the table names from the `stdout` and checks if the provided table is present in the retrieved names, ensuring the correct behavior for checking table existence in the Hive database.