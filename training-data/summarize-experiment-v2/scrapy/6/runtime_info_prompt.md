You have been given the source code of a function that is currently failing its test cases.

Image you are in the middle of debugging process and you have logged the variable values from this buggy function. Your mission involves analyzing each test case of runtime input/output values step by step and compare it with the core logic of the function. Using this comparisons, formulate the reason for the discrepancy and
summarise it.


# Runtime value and type of variables inside the buggy function
Each case below includes input parameter value and type, and the value and type of relevant variables at the function's return, derived from executing failing tests. If an input parameter is not reflected in the output, it is assumed to remain unchanged. Note that some of these values at the function's return might be incorrect. Analyze these cases to identify why the tests are failing to effectively fix the bug.

## Case 1
### Runtime value and type of the input parameters of the buggy function
image.format, value: `'JPEG'`, type: `str`

image, value: `<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=100x100 at 0x7F2A1F05ECD0>`, type: `JpegImageFile`

image.mode, value: `'RGB'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

## Case 2
### Runtime value and type of the input parameters of the buggy function
image.format, value: `'JPEG'`, type: `str`

image, value: `<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=100x100 at 0x7F2A1F05ECD0>`, type: `JpegImageFile`

image.mode, value: `'RGB'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

size, value: `(10, 25)`, type: `tuple`

### Runtime value and type of variables right before the buggy function's return
image, value: `<PIL.Image.Image image mode=RGB size=10x10 at 0x7F2A1E7A71F0>`, type: `Image`

image.size, value: `(10, 10)`, type: `tuple`

## Case 3
### Runtime value and type of the input parameters of the buggy function
image.format, value: `'PNG'`, type: `str`

image, value: `<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=100x100 at 0x7F2A1E7A76A0>`, type: `PngImageFile`

image.mode, value: `'RGBA'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

### Runtime value and type of variables right before the buggy function's return
image, value: `<PIL.Image.Image image mode=RGB size=100x100 at 0x7F2A1E7A7BB0>`, type: `Image`

image.mode, value: `'RGB'`, type: `str`

background, value: `<PIL.Image.Image image mode=RGBA size=100x100 at 0x7F2A1E7A7B80>`, type: `Image`

## Case 4
### Runtime value and type of the input parameters of the buggy function
image, value: `<PIL.Image.Image image mode=P size=100x100 at 0x7F2A1E79CC10>`, type: `Image`

image.mode, value: `'P'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

### Runtime value and type of variables right before the buggy function's return
image, value: `<PIL.Image.Image image mode=RGB size=100x100 at 0x7F2A1E79C6D0>`, type: `Image`

image.mode, value: `'RGB'`, type: `str`

background, value: `<PIL.Image.Image image mode=RGBA size=100x100 at 0x7F2A1E79C880>`, type: `Image`