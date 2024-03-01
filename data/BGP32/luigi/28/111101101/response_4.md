### Bug Explanation
The bug in the `table_exists` function lies in the condition checking part where the existence of the table is evaluated. In the case where there is no partition specified, the function checks if the table name is in the stdout output from the `run_hive_cmd` function. However, the condition check is incorrect as it should be checking if the table name is equal to an element in the list of tables from stdout, not the entire string.

### Bug Fix Strategy
To fix the bug, we need to modify the condition check in the case where there is no partition specified to check if the table name exists in the list of tables obtained from the stdout, instead of checking if it's in the entire output string.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            # Split the stdout by newlines to get a list of tables
            tables = stdout.split('\n')
            return tables and table in tables
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

            if stdout:
                return True
            else:
                return False
``` 

By splitting the stdout string by newlines in the first condition check, we can compare the table name with each element in the list of tables, ensuring a correct evaluation of the table's existence.