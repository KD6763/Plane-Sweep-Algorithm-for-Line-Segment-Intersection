# Line Segment Intersection

Solving Line Segment Intersection problem using BruteForce and Plane Sweep Algorithms. Language used is python 3.9

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Matplotlib.

```bash
pip install matplotlib
pip install sortedcontainers
pip install bisect
```

### Files Available
The folder contains 5 files in total
* BruteForce.py - Python file to call Bruteforce implementation
* LineSegmentIntersection.py - Python file to call Plane Sweep implementation
* input.txt - Input file with all the points

### Imports
```python
from sortedcontainers import SortedSet
import matplotlib.pyplot as plt
from bisect import bisect_right
import math
from matplotlib.animation import FuncAnimation
import sys
```

## Usage

### To run the Bruteforce Algorithm
```bash
python3 BruteForce.py filename
```
Where the filename is the input file (input.txt)

### To run the Plane Sweep Algorithm
```bash
python3 LineSegmentIntersection.py filename
```
Where the filename is the input file (input.txt)

## Outputs
* The outputs will be stored in the files output_bf.txt and output_ps.txt respectively.
* Also shows the plot with the segments and intersections
* Also we can see the visualization of the Plane Sweep Algorithm

## Points to consider
* The given plane sweep algorithm is implemented using sortedsets and list.
* Initially the entire algorithm was supposed to use sortedsets as they are implementation of red-black trees
* But, it resulted in issues with comparator overloading for the sweep data structure
* Resulting in implementing the event datastructure using sortedsets and sweep using lists
* Although the implementation is done is such a way that the list replicates the entire working of the sortedsets


