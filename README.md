# HomoIndex

## Overview
**HomoIndex** is a light-weight and efficient tool designed to bridge genomic data fragmentation across independent research projects. It enables rapid identification of orthologous gene mappings both within the same genus (via **JCVI** syntenic blocks) and across model plant species (**BLASTP** against *Arabidopsis thaliana*, *Oryza sativa*, and *Zea mays*).


## Key Features
- **Zero Database Setup**: Automatically checks, fetches, and decrypts the required genus-level genomic database from **Zenodo** repositories upon query.
- **Dual-Layer Homology Assessment**: Combines intra-genus synteny/homology groups (JCVI) with cross-species best hits against model plants (BLASTP).
- **Lightweight & High-Performance**: Operates on compressed, encrypted SQLite storage without requiring heavy local database servers.
- **Flexible Workflow**: Supports both single-gene quick queries and high-throughput batch list processing.


## System Requirements & Prerequisites
- **OS**: Linux (x86_64) or macOS
- **Python**: Python 3.7+
- **Python Dependencies**: `cryptography` (required for on-the-fly database decryption)


## Installation
```
git clone https://github.com/wzxie/HomIndex.git
chmod 755 /path/to/dist/HomIndex.py
export PATH=/path/to/dist:$PATH
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
  -h, --help                     Show this help message and exit
  --genus/-G GENUS               Target genus name matching subdirectories in ./genus/ (e.g. Brassica, Acacia)
  --gene/-g GENE                 Single gene ID to query
  --gene_list/-l GENE_LIST       Text file containing multiple gene IDs (one ID per line)
  --outdir/-o OUTDIR             Output directory for query reports (default: .)
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
