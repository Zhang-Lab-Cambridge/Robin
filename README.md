Assembled code for experimental data analysis and figure making. The idea is that this is organised, and organised in such a manner that it is: a) usable by other people b) makes sense, can be edited easily down the line c) has some crude version of a user interface for ease of use

This is set up as essentially a python library. If a file is created in the main folder, then 'ras' functions as a python module, and the files within it have callable functions in. For example, just as one can say:

import numpy as np

One can say:

import ras.echem as echem

and then use any function in ras.echem in the file. When adding to this, either add functions inside a file (with proper commentary etc) or you can add an entire new file full of functions to do eg image data analysis for confocal microscopy.

All functions are commented with a general description and each variable in/out is given an expected class.

When updating anything, submit as a pull request.

I'm very much in the process of reorganising this, and there will be a lot of changes. 

Using test_tkinter currently will allow you to look at photocurrent traces, if something goes wrong let me know.
