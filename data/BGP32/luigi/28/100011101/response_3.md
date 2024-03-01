### Bug Explanation
The bug in the provided function lies in the comparison of the `table` name with the `stdout` output retrieved from the `run_hive_cmd` function. In the existing implementation, the function checks if the `table` name is present in the `stdout` string obtained from the `show tables` command. However, this comparison fails in some cases due to the absence of an exact match, especially when the output contains multiple table names or when the table name is in a different case. 

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to perform a more strict check. We can split the `stdout` by newlines and then check for each individual table name to see if it matches the provided `table` name exactly.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database)).split()

        return table in stdout
    else:
        stdout = run_hive_cmd(f"use {database}; show partitions {table} partition ({self.partition_spec(partition)})").split()

        return table in stdout
``` 

The corrected implementation splits the `stdout` by newlines into a list of table names and then directly checks if the provided `table` name is in that list, ensuring an exact match. This should resolve the issue with non-matching comparisons and make the function return the correct results according to the provided test cases.