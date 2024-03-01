### Bug Explanation
The bug in the `table_exists` function lies in the conditional statements that check the output (`stdout`) of the `run_hive_cmd` function. The bug causes the function to return incorrect results based on the `stdout` content, leading to test failures.

In the provided failing tests, we can see that the expected behavior is to check if the table exists based on the output of the `run_hive_cmd` function. If the table name is present in the output, the function should return `True`, otherwise `False`. However, due to incorrect handling of the `stdout` variable in the conditionals, the function doesn't behave as expected.

### Bug Fix Strategy
To fix the bug, we need to correctly handle the comparison of the `table` variable with the `stdout` output. We should check whether the table name is present in the `stdout` output correctly.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
        
        return any(partition in line for line in stdout.split('\n'))
``` 

With this corrected version, the function will split the `stdout` by newlines and check if the table name is in the split lines, which aligns with the expected behavior in the failing tests.