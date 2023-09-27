# How to use *ladderpath.py*
The required Python modules and packages are: *random, os, numpy, pandas, graphviz*.

Place the script *ladderpath.py* and the folder *ladderpath_data_omega0* in the same directory. Also, ensure that the script you have written for calculating ladderpath is located in this directory. By doing so, you will be able to call and run it successfully. The command for calling it is as follows, using a single target sequence "CUCGACGACUAUCUCGACAAUGACU" as an example (refer to Figure 7 in the Methods section):

```python
import ladderpath
strs = ['CUCGACGACUAUCUCGACAAUGACU']
strsLP = ladderpath.ladderpath(strs, CalPOM=True)
```
Up to this point, the ladderpath of the target sequence and its relevant information are all stored in the variable *strsLP*.


## To get the *partially ordered multiset* representation of the ladderpath, use:

```python
strsLP.dispPOM()
# example output: { G, A(3), C(3), U(3) // AU, GAC // CUCGAC, GACU}

strsLP.POM
# example output:
# [[('G', 1), ('A', 3), ('C', 3), ('U', 3)],
#  [('AU', 1), ('GAC', 1)],
#  [('CUCGAC', 1), ('GACU', 1)]]
```

Inspecting the partially ordered multiset of the ladderpath for this sequence can also be achieved by directly calling the *POM* property within *strsLP*, which facilitates subsequent processing.

## To get *ladderpath-index*, *order-index*, and *size-index*, use:

```python
strsLP.disp3index()
# example output: ( Ladderpath-index:14,  Order-index:11,  Size-index:25 )

strsLP.index3
# example output: (14, 11, 25)
```

Reviewing the three indicators associated with the ladderpath of this sequence (ladderpath-index $\lambda$, order-index $\omega$, and size-index $S$) can also be accomplished by directly accessing the *index3* property within *strsLP*, which facilitates subsequent processing.

## To get *order-rate*, use:

```python
strsLP.getEta(nBase=4)
# example output: 0.420049710024855
```

The parameter *nBase* represents the number of basic building block types of the target sequence. For example, for an amino acid sequence, *nBase=20* (20 types of amino acids), for a decimal number sequence, *nBase=10* (ranging from 0 to 9), for RNA or DNA sequences, *nBase=4* (4 types of nucleotides), and for binary 01 sequences, *nBase=2*. It is worth noting that the current version only accommodates *nBase* values from the four numbers (to be further developed).

## To draw the *laddergraph*, use:

```python
strsLP.laddergraph_single(filename = "G", show_longer_than = 1, style = "ellipse", target_name = "")
```

This function currently only works when the target is a single sequence. The parameters: 

- *filename* is the file name of the figure.

- *show_longer_than*: When the length of the ladderon > *show_longer_than*, this ladderon will be displayed. Note that *show_longer_than* should always be >= 1, and the basic building blocks are also omitted. 

- *style* dictates how the laddergraph is displayed. It can either be "ellipse" (the sequence will not be displayed, but the size of the ellipse is positively related to the length of the sequence) or "box" (the sequence will be displayed). 

- *target_name* is the text displayed in the target sequence.



## Notes:

```python
strsLP = lp.ladderpath(strs, CalPOM=False)
```

In this function, setting *CalPOM* to *False* means that the program will only calculate the three parameters: ladderpath-index $\lambda$, order-index $\omega$, and size-index $S$, and skip the computation of the partially ordered multiset (POM). In this case, running *strsLP.POM* or *strsLP.dispPOM()* will yield an empty result. If you only need the indices in some cases, doing this can speed up the computation.

Note that for sequences below 2500 AA, the current version can handle everything efficiently. For sequences between 2500 and 10,000 AA, the code is efficient in all aspects except for determining the order-rate $\eta$, as computing the accurate value of $\omega_0(S)$ for $S > 2500$ AA requires significant computational power. A later version will work for larger $S$. If $\omega_0(S)$ for $S > 2500$ can be estimated in some way (e.g., interpolation), the $\eta$ value can be determined. For sequences exceeding 10,000 AA, the ladderpath calculation becomes too time-consuming and is not feasible for the current version.
