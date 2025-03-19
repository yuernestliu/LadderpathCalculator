# LadderpathCalculator_v1.0

## Introduction
Repository associated with the research paper "Evolutionary tinkering enriches the hierarchical and nested structures in amino acid sequences, Physical Review Research, 6: 023215, 2024" (https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.6.023215) on the hierarchical and nested structures in amino acid sequences. This paper is first available online on 2023.10.15 (https://www.researchsquare.com/article/rs-3440555/v1).

This repository serves as a supplement, providing the necessary tools (also useful tools for you to calculate the ladderpath of sequences) and datasets to understand and replicate our findings.


## Repository Structure
- The folder **Data**: Contains all the data generated and other associated scripts:

    - *six_proteome_output_fig6a.txt*: It records the ladderpath-associated indicators for every protein shown in Fig. 6 of the main text.

    - *cal_Rk.py*: Script to calculate $R_k$, which was used in Fig. 3 of the main text.


- The folder **LadderpathCalculator**: Contains scripts and data for calculating the ladderpath, including:

    - *README.md*: Instructions on how to use the ladderpath calculation tool.

    - *ladderpath.py*: Main script for ladderpath calculation.

    - *ladderpath_data_omega0*: The folder containing supporting data for *ladderpath.py*. Do not modify.


- The folder **LadderpathCalculator-InclOrigData**: Normally, you do not need this folder. 
    > This folder is intended for developers who wish to contribute to calculating $\omega_0$ for large $S$. This folder contains the same files as the *LadderpathCalculator* folder. Additionally, within *ladderpath_data_omega0/nBase2/* (*ladderpath_data_omega0/nBase4/*, *ladderpath_data_omega0/nBase10/*, etc.), there is a folder named *OriginalData* which describes how the corresponding .csv file (namely, $\omega_0(S)$) was calculated.




## Usage

For a quick start on how to use the ladderpath calculation tool, navigate to the **LadderpathCalculator** folder and see the provided README for more detailed usage and options. Quick example:

```python
import ladderpath
strs = ['CUCGACGACUAUCUCGACAAUGACU']
strsLP = ladderpath.ladderpath(strs, CalPOM=True)

strsLP.dispPOM()
# example output: { G, A(3), C(3), U(3) // AU, GAC // CUCGAC, GACU}

strsLP.disp3index()
# example output: ( Ladderpath-index:14,  Order-index:11,  Size-index:25 )
```
