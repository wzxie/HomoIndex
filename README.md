# HomoIndex

## Overview
**HomoIndex** is a light-weight and efficient tool designed to bridge genomic data fragmentation across independent research projects by rapidly identifying orthologous gene mappings both within the same genus (JCVI) and against model plant species (BLASTP against *Arabidopsis*, *Oryza*, and *Zea*).

## Environment & System Requirements
```
1. OS Support: Linux (x86_64)
2. Python Version: Python 3.7+
```

## Installation
```
1. git clone https://github.com/wzxie/HomIndex.git
2. chmod 755 /path/to/dist/HomIndex.py
3. export PATH=/path/to/dist:$PATH
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

options:
  -h, --help                             Show this help message and exit
  --genus GENUS, -G GENUS                Target genus name matching subdirectories in ./genus/ (e.g. Brassica, Acacia)
  --gene GENE, -g GENE                   Single gene ID to query
  --gene_list GENE_LIST, -l GENE_LIST    Text file containing multiple gene IDs (one ID per line)
  --outdir OUTDIR, -o OUTDIR             Output directory for query reports (default: .)

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
* GWHPEQVL000440.txt         # List of homologous genes
```

## Contact
* Yue-Miao Zhang:   13091255317@163.com
* Ming-Zhu Yan:     ymz7113@163.com
* Zi-Xin Yu:        18713111991@163.com
* Wen-Zhao Xie:     wzxie@hebtu.edu.cn
