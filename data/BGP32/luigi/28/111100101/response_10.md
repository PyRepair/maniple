### Bug Analysis:
The bug in the `table_exists` function is with the condition check for the presence of the table in the output of `run_hive_cmd`. The bug causes the function to sometimes return incorrect results. The issue lies in how the function checks for the existence of the table in the stdout.

### Bug Explanation:
1. In the first case, when the `table` is not found in the stdout, the function incorrectly returns `True`. This is because the condition `stdout and table in stdout` will evaluate to `True` if `stdout` is not an empty string, regardless of the presence of the `table` in it.
2. In the second case, when the `table` is found in the stdout, the function correctly returns `True`.
3. In the third case with a partition, the function relies on the `partition_spec` method to find the partition information. The bug in this case is similar to the first case, where the condition check for the presence of the table in the stdout can lead to incorrect results.
4. For the other cases, similar issues may arise leading to incorrect results.

### Bug Fix:
To fix the bug, we need to properly check if the `table` exists in the `stdout` returned by `run_hive_cmd`. We can simplify the conditions to improve readability and ensure the correct behavior.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split('\n')

    stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2});""".format(database, table, self.partition_spec(partition)))
    return any(partition in line for line in stdout.split('\n'))
```

By splitting the `stdout` on newlines and checking for the presence of the `table` or `partition`, we can ensure the correct behavior and pass all the test cases.