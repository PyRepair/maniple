### Bug Explanation
The bug in the `table_exists` function lies in the conditional check to determine if a table exists in the database. The issue arises in the comparison of the table name with the output obtained from the `run_hive_cmd` function. The function incorrectly checks if the output contains the table name as a substring, leading to erroneous results.

In the failing test scenario, the output `OK\nmytable` is treated as containing the table name `mytable`, causing the function to return `True`. However, the correct behavior should validate an exact match for the table name in the output.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison operation to ensure that the table name is an exact match with the output obtained from the `run_hive_cmd` function. This adjustment will accurately determine the existence of the table in the database and resolve the failing test scenarios.

### Corrected Function
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

By splitting the output obtained from `run_hive_cmd` on the new line character (`\n`) and checking the exact table name in the resulting list, the corrected function will accurately identify the presence of the table. This modification ensures that the function behaves as expected and passes the failing test cases.