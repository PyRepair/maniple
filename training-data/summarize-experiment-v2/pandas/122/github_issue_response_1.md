GitHub Bug Title:
DataFrame.equals() returns True in case of identical blocks with different locations

Description:
The DataFrame.equals() method returns True when comparing two DataFrames with identical blocks but with different locations. This behavior is unexpected and should return False in such cases.

Expected Output:
When using the equals() method to compare two DataFrames with identical blocks but different locations, the method should return False.

Environment:
- Python: 3.6.8
- pandas: 0.25.0
- numpy: 1.16.4
- scipy: Not available
- matplotlib: 3.1.0
- xlrd: 1.2.0