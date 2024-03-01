### Bug Explanation
The bug occurs because the `table_exists` function is not correctly checking if the table exists in the returned output from the `run_hive_cmd` function. The current implementation only checks if the table name is contained in the output, leading to false positives in some cases.

### Bug Fix Strategy
To fix the bug, we need to modify the `table_exists` function to correctly parse the output of `run_hive_cmd` and determine if the table exists based on the provided input parameters.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By splitting the output of `run_hive_cmd` by newline characters and checking if the table name is in the returned list of tables, we can accurately determine if the table exists. Additionally, we can simply return `bool(stdout)` in the case where a partition is specified to indicate whether the table exists or not.