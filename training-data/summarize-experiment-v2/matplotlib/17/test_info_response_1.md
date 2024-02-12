The original error messages mention that a RuntimeWarning related to overflow was encountered in scalar subtract and scalar absolute:

    * In the case "clim = (-20000, 20000)", it stated:
      `E       RuntimeWarning: overflow encountered in scalar subtract`
      "lib/matplotlib/transforms.py:2799: RuntimeWarning"
 
    * In the case "clim = (-32768, 0)", it stated:
      `E       RuntimeWarning: overflow encountered in scalar absolute`
      "lib/matplotlib/transforms.py:2794: RuntimeWarning"

Here's a simplified version of the error messages that points to the source of the problem:
  
    * The "clim = (-20000, 20000)" case had the warning about overflow during scalar subtraction.
  
    * The "clim = (-32768, 0)" case had the warning about overflow during scalar absolute.