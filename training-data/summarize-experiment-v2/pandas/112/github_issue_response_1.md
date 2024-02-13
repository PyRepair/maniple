GitHub Bug Title: Round method fails when columns are CategoricalIndex of IntervalIndex

Description:
The round method fails whenever the columns are CategoricalIndex made from an IntervalIndex. This can occur when using pivot_table and the pd.cut function. 

Expected Output:
The round method should work normally when the columns are CategoricalIndex of IntervalIndex.