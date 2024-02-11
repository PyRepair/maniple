Input value and type pair:
(0, int) (1, int) 0.05, float, increasing True

Output value and type pair:
0.0, float  1.0, float  False, bool  1.0, float

Input value and type pair:
(-0.5, float) (1.5, float) 0.05, float, increasing True

Output value and type pair:
False, bool 1.5, float

Input value and type pair:
(0.5, float) (-0.5, float) 0.05, float, increasing True

Output value and type pair:
-0.5, float 0.5, float  True, bool 0.5, float

Input value and type pair:
(-inf, float) (inf, float) 0.05, float, increasing True

Input value and type pair:
(-20000, int16) (20000, int16) 0.1, float, increasing True

Output value and type pair:
-20000.0, float 20000.0, float  False, bool 20000.0, float

Input value and type pair:
(-20000.0, float64) (20000.0, float64) 0.05, float, increasing True

Output value and type pair:
-20000.0, float 20000.0, float  False, bool 20000.0, float

Input value and type pair:
(-32768, int16) (0, int16) 0.1, float, increasing True

Output value and type pair:
-32768.0, float 0.0, float  False, bool 32768.0, float

Input value and type pair:
(-32768.0, float64) (0.0, float64) 0.05, float, increasing True

Output value and type pair:
-32768.0, float 0.0, float  False, bool 32768.0, float