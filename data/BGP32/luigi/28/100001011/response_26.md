#### Bug Explanation:
The bug arises from a case sensitivity issue in the `table_exists` function. The function checks if the table exists in the Hive database by comparing the `table` variable directly with the `stdout` variable, which causes problems when the casing of the table name differs.

#### Bug Location:
The bug is located in the `return stdout and table in stdout` line for the condition where `partition` is None. It directly checks the table name with the stdout without considering the case sensitivity.

#### Bug Fix Strategy:
To fix the bug, we need to convert both the `table` and the `stdout` variable contents to lowercase so that the comparison becomes case-insensitive. This way, we can accurately determine if the table exists in the database regardless of the case.

#### Corrected Version:
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

By converting both the `table` and `stdout` variables to lowercase during the comparison, we address the case sensitivity issue, making the `table_exists` function case-insensitive as required by the GitHub issues.