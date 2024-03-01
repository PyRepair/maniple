### Bug Explanation
The bug in the `table_exists` function lies in how it checks for the existence of a table in the Hive database. In the case when the table name is present in the list of tables obtained from the Hive command, the function should return true. However, due to the way the condition is written, it returns true only if the stdout is not None and the table name is in stdout. This logic is incorrect and leads to failing test cases.

### Bug Fix Strategy
To fix the bug, we need to adjust the conditions for returning true in both cases: when there is no partition and when there is a specified partition. We should check if the table name is present in the stdout obtained from the Hive commands and return true accordingly.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout is not None and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout is not None and table in stdout
``` 

By modifying the conditions to check if stdout is not None and if the table name is in stdout, we ensure that the function correctly determines the existence of the table in the Hive database. This corrected version should pass all the failing test cases and have the expected behavior.