Assembled code for experimental data analysis and figure making. The idea is that this is organised, and organised in such a manner that it is: a) usable by other people b) makes sense, can be edited easily down the line c) has some crude version of a user interface for ease of use

This is set up as essentially a python library. If a file is created in the main folder, then 'echem', 'gen' and 'gui' function as python modules. For example, just as one can say:

import numpy as np

One can say:

import echem.chrono as c

and then use any function in echem.chrono in the file. When adding to this, either add functions inside a file (with proper commentary etc) or you can add an entire new module to do eg image data analysis for confocal microscopy.

All functions are commented with a general description and each variable in/out is given an expected class.

When updating anything, submit as a pull request.

I'm very muhc in the process of reorganising this, and there will be a lot of changes. Please DO NOT EDIT until I am done basically :)
