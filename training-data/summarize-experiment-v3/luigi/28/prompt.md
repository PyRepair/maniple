Please fix the buggy function provided below and output a corrected version. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.


# The source code of the buggy function
```python
# The relative path of the buggy file: luigi/contrib/hive.py



    # this is the buggy function you need to fix
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            if stdout:
                return True
            else:
                return False
    
```


# The source code of the buggy function
```python
# The relative path of the buggy file: luigi/contrib/hive.py



    # this is the buggy function you need to fix
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            if stdout:
                return True
            else:
                return False
    
```# The declaration of the class containing the buggy function
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """


# This function from the same file, but not the same class, is called by the buggy function
def run_hive_cmd(hivecmd, check_return_code=True):
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def partition_spec(self, partition):
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def partition_spec(self, partition):
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def partition_spec(self, partition):
    # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def partition_spec(self, partition):
        # Please ignore the body of this function

# A failing test function for the buggy function
```python
# The relative path of the failing test file: test/contrib/hive_test.py

    @mock.patch("luigi.contrib.hive.run_hive_cmd")
    def test_table_exists(self, run_command):
        run_command.return_value = "OK"
        returned = self.client.table_exists("mytable")
        self.assertFalse(returned)

        run_command.return_value = "OK\n" \
                                   "mytable"
        returned = self.client.table_exists("mytable")
        self.assertTrue(returned)

        # Issue #896 test case insensitivity
        returned = self.client.table_exists("MyTable")
        self.assertTrue(returned)

        run_command.return_value = "day=2013-06-28/hour=3\n" \
                                   "day=2013-06-28/hour=4\n" \
                                   "day=2013-07-07/hour=2\n"
        self.client.partition_spec = mock.Mock(name="partition_spec")
        self.client.partition_spec.return_value = "somepart"
        returned = self.client.table_exists("mytable", partition={'a': 'b'})
        self.assertTrue(returned)

        run_command.return_value = ""
        returned = self.client.table_exists("mytable", partition={'a': 'b'})
        self.assertFalse(returned)
```


# A failing test function for the buggy function
```python
# The relative path of the failing test file: test/contrib/hive_test.py

    @mock.patch("luigi.contrib.hive.run_hive_cmd")
    def test_apacheclient_table_exists(self, run_command):
        run_command.return_value = "OK"
        returned = self.apacheclient.table_exists("mytable")
        self.assertFalse(returned)

        run_command.return_value = "OK\n" \
                                   "mytable"
        returned = self.apacheclient.table_exists("mytable")
        self.assertTrue(returned)

        # Issue #896 test case insensitivity
        returned = self.apacheclient.table_exists("MyTable")
        self.assertTrue(returned)

        run_command.return_value = "day=2013-06-28/hour=3\n" \
                                   "day=2013-06-28/hour=4\n" \
                                   "day=2013-07-07/hour=2\n"
        self.apacheclient.partition_spec = mock.Mock(name="partition_spec")
        self.apacheclient.partition_spec.return_value = "somepart"
        returned = self.apacheclient.table_exists("mytable", partition={'a': 'b'})
        self.assertTrue(returned)

        run_command.return_value = ""
        returned = self.apacheclient.table_exists("mytable", partition={'a': 'b'})
        self.assertFalse(returned)
```


Here is a summary of the test cases and error messages:

The stack traces closely related to the fault location are: 1) test_table_exists function in the file test/contrib/hive_test.py, and 2) test_apacheclient_table_exists function in the same file. The simplified error message in both cases is AssertionError: False is not true.


## Summary of Runtime Variables and Types in the Buggy Function

The relevant input/output values are 
- Case 1:
    - Input parameters: database (value: 'default', type: str), table (value: 'mytable', type: str)
    - Output: stdout (value: 'OK', type: str)
  
- Case 2:
    - Input parameters: database (value: 'default', type: str), table (value: 'MyTable', type: str)
    - Output: stdout (value: 'OK\nmytable', type: str)
    
- Case 3:
    - Input parameters: partition (value: {'a': 'b'}, type: dict), database (value: 'default', type: str), table (value: 'mytable', type: str)
    - Output: stdout (value: 'day=2013-06-28/hour=3\nday=2013-06-28/hour=4\nday=2013-07-07/hour=2\n', type: str)
    
The rational for this choice is that these inputs and outputs are likely relevant to the bug since they are related to the execution of the `run_hive_cmd` function and could lead to incorrect results.


## Summary of Expected Parameters and Return Values in the Buggy Function

The `table_exists` function is supposed to check for the existence of a table in a database and return a boolean value based on the result. However, in the failing test cases, the function is not returning the expected values. In Case 1, the expected value of `stdout` is 'OK', but the function is not returning this value. Similarly, in Case 2, the expected value of `stdout` is 'OK\nmytable', but the function is not returning this value. These discrepancies indicate that the function is not working properly and needs to be fixed.


## Summary of the GitHub Issue Related to the Bug

The issue with the `table_exists` function is that it is not case insensitive. When checking for an existing table, the function does not account for the fact that hive is case insensitive and returns table names in lowercase. This results in failures when checking for tables with capitalized names. The issue description suggests checking stdout against `table.lower()` to avoid case issues. This oversight in the function's implementation causes it to fail when dealing with tables that are defined with capitalized names, and the proposed fix would address this problem.


