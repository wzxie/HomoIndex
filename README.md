# HomoIndex

## Overview
The widespread issue of data silos significantly hinders the integration and utilization of genomic resources within the same genus. To address this challenge, we developed "HomIndex" to bridge data fragmentation across independent research projects by rapidly identifying orthologous gene mappings among congeneric species.

## Installation
Run the following command to install HomIndex.
```
1. git clone https://github.com/wzxie/HomIndex.git
2. chmod 755 /path/to/HomIndex.py
3. export PATH=/path/to:$PATH
```

## Example
### 1. Perform a homology search for a single gene.
```
python HomoIndex.py --genus Brassica --gene GWHPEQVL000440
```
### 2. Perform a homology search for multiple genes
```
python HomoIndex.py --genus Brassica --gene_list genes.txt
```

## Usage
### Quick start
```
usage: HomoIndex.py [-h] --genus GENUS [--gene GENE] [--gene_list GENE_LIST] [--outdir OUTDIR]

Query homologous genes by genus.

options:
  -h, --help            show this help message and exit
  --genus GENUS, -G GENUS
                        Genus name under ./genus/ directory
  --gene GENE, -g GENE  Single gene ID to query
  --gene_list GENE_LIST, -l GENE_LIST
                        Text file containing multiple gene IDs (one per line)
  --outdir OUTDIR, -o OUTDIR
                        Output directory (default: ./results/)

See more information at https://github.com/wzxie/HomoIndex.
```

## Inputs and Outputs
### Input files
1) single gene
```
GWHPEQVL000440
```
2) multiple genes
```
less genes.txt
GWHPEQVL000440
GWHPEQVL002200
GWHPEQVL019729
```

### Output files
```
* results/GWHPEQVL000440.txt         # List of homologous genes
* results/summary.tsv                # Statistics of homologous genes
```

## Contact
* Yue-Miao Zhang:   13091255317@163.com
* Ming-Zhu Yan:     ymz7113@163.com
* Zi-Xin Yu:        18713111991@163.com
* Wen-Zhao Xie:     wzxie@hebtu.edu.cn

