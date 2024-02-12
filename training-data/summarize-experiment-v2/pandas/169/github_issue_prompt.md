You have been provided with a description for GitHub issue. However, it may be ambiguous, please simplify it and make it readable by developer while keeping the key information.


# A GitHub issue title for this bug
```text
DataFrame Quantile Broken with Datetime Data
```

## The GitHub issue's detailed description
```text
This works fine:

In [17]: pd.Series(pd.date_range('1/1/18', periods=5)).quantile()                                                                          
Out[17]: Timestamp('2018-01-03 00:00:00')
But the equivalent method with a DataFrame raises:

In [18]: pd.DataFrame(pd.date_range('1/1/18', periods=5)).quantile()                                                                       
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-18-68ffc067f6f0> in <module>
----> 1 pd.DataFrame(pd.date_range('1/1/18', periods=5)).quantile()

~/clones/pandas/pandas/core/frame.py in quantile(self, q, axis, numeric_only, interpolation)
   7569                                      axis=1,
   7570                                      interpolation=interpolation,
-> 7571                                      transposed=is_transposed)
   7572 
   7573         if result.ndim == 2:

~/clones/pandas/pandas/core/internals/managers.py in quantile(self, **kwargs)
    500 
    501     def quantile(self, **kwargs):
--> 502         return self.reduction('quantile', **kwargs)
    503 
    504     def setitem(self, **kwargs):

~/clones/pandas/pandas/core/internals/managers.py in reduction(self, f, axis, consolidate, transposed, **kwargs)
    473 
    474         # single block
--> 475         values = _concat._concat_compat([b.values for b in blocks])
    476 
    477         # compute the orderings of our original data

~/clones/pandas/pandas/core/dtypes/concat.py in _concat_compat(to_concat, axis)
    172                 to_concat = [x.astype('object') for x in to_concat]
    173 
--> 174     return np.concatenate(to_concat, axis=axis)
    175 
    176 

ValueError: need at least one array to concatenate
Expected Output
The DataFrame should return just as Series does
```