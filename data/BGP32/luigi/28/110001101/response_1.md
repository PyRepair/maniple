### Bug Explanation
The bug in the `table_exists` function stems from the inconsistency between the expected behavior and the actual behavior when checking if a table exists in the database. The function is not correctly parsing the output of the `run_hive_cmd` function to determine if the table exists. In cases where the table does exist, the function is not able to properly identify it in the stdout output.

### Bug Fix Strategy
To fix the bug, we need to modify the way we check whether the table exists in the database. By properly parsing the output of the `run_hive_cmd` function and checking the presence of the table name in the stdout, we can ensure that the function behaves as expected.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return table in stdout.split()
        else:
            stdout = run_hive_cmd("use {0}; show partitions {1}({2});".format(database, table, self.partition_spec(partition)))
    
            return len(stdout.strip()) > 0
``` 

By splitting the `stdout` based on spaces, we can check if the table name is present in the list of tables returned by the `show tables` command. Additionally, we ensure that there is actual output from the `show partitions` command before determining that the table exists.