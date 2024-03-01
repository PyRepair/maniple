## Correction:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd(f'use {database}; show tables like "{table}";')
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd(f'use {database}; show partitions {table} partition ({self.partition_spec(partition)})')
        return bool(stdout)
``` 

This corrected version of the `table_exists` function now utilizes the `table.lower()` and `stdout.lower()` comparison to make the function case-insensitive when checking for table existence. This modification resolves the issue mentioned in the GitHub posting and ensures that the function behaves as expected in the provided test cases.