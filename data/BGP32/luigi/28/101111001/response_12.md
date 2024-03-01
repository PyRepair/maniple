### Bug Explanation
The bug in the `table_exists` function lies in the logic of checking whether a table exists in the database. The function checks the output from `run_hive_cmd` to determine if the table exists or not, but the current implementation does not handle the case-insensitive nature of table names in a consistent manner. This leads to failing test cases where the function incorrectly evaluates the existence of tables based on case sensitivity.

### Bug Fix Strategy
To fix this bug, we need to ensure that the comparison between the table names is case-insensitive. This can be achieved by converting both the table name from the database and the table name being checked to lowercase before comparison. This approach will provide consistent behavior and pass the failing test cases.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By converting both the table name and the output from `run_hive_cmd` to lowercase before comparison, the function will correctly identify whether the table exists or not, regardless of the case of the table name. This corrected version should pass the failing test cases.