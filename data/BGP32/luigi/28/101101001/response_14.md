### Bug Explanation:
The bug in the `table_exists` function is due to the incorrect logic in checking whether the table exists in the database. The function incorrectly checks for the presence of the table name in the output of the `run_hive_cmd` function. The logic should be more robust and should consider parsing the output properly to determine if the table exists.

### Bug Fix Strategy:
1. Modify the logic in the `table_exists` function to parse the output of the `run_hive_cmd` function more effectively to determine if the table exists in the database.
2. Update the return statements in the function to correctly reflect whether the table exists or not based on the parsed output.
3. Ensure that the function handles different cases of table names and output formats properly.

### Corrected Version:
```python
class HiveCommandClient(HiveClient):
   
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables in {0} like "{1}";'.format(database, table))
            return table in stdout.splitlines()  # Check if the table name is in the list of tables
        
        else:
            partition_str = ', '.join(["{0}='{1}'".format(k, v) for k, v in partition.items()])
            stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, partition_str))
  
            return bool(stdout)  # Check if partitions are returned
  
``` 

By implementing the corrected version of the `table_exists` function with the suggested modifications, the function should now properly handle the parsing of output from the `run_hive_cmd` function and reliably determine the existence of tables and partitions in the database.