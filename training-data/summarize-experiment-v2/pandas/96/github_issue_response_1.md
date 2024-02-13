GitHub Bug Title:
Pandas CustomBusinessHour date_range divides periods when adding holidays

Description:
When using pd.date_range with pd.offsets.CustomBusinessHour and adding holidays, the method produces an unexpected result. Instead of producing 14 periods, it generates more dates than intended. However, when replacing periods with the corresponding end date, the method works as expected. It is unclear why date_range has this behavior.

Expected Output:
pd.date_range with CustomBusinessHour and added holidays should produce the correct number of periods without dividing the dates unexpectedly.

Environment:
- Python: 3.7.3.final.0
- pandas: 1.1.1