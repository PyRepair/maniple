The relevant input/output values are:
- `proc` (value: `<MagicMock name='Popen()' id='140254489932816'>`, type: `MagicMock`)
- `version` (value: `'3.5.9'`, type: `str`)

Rational: This case shows that the `proc` variable is being mocked and not actually executing the command to get the `FISH_VERSION`. This is likely the cause of the bug as it's not retrieving the correct version of the shell.