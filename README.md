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
python HomoIndex.py --genus Aegilops --gene gene-LOC109745798
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
gene-LOC109745798
```
2) multiple genes
```
less genes.txt
gene-LOC109745798
AetT093_7Dv1G030400
```

### Output files
```
==================== Query Results for (1/1): gene-LOC109745798 ====================

[JCVI Homology Group]: Found 3 clusters
species gene ID
Aegilops_tauschii-20171101      gene-LOC109745798
Aegilops_tauschii-20210527      AetT093_7Dv1G030400
Aegilops_umbellulata    AeUmb.TA1851.r1.7UG0045140

[BLASTP Best Hits]: Found 15 matches
Model Plant     Subject ID                     Identity(%)  AlignLen   E-value      BitScore
------------------------------------------------------------------------------------------
Arabidopsis     AT1G03430                      51.55        97         2.6e-26      97.1
Arabidopsis     AT3G29350                      48.45        97         1.4e-24      92.8
Arabidopsis     AT3G21510                      48.08        104        3.0e-24      91.7
Arabidopsis     AT5G39340                      50.52        97         2.5e-23      90.9
Arabidopsis     AT3G16360                      37.04        108        7.4e-23      87.8
Oryza           AGIS_Os08g041290               63.64        110        6.4e-47      150.0
Oryza           AGIS_Os09g043710               58.56        111        3.1e-40      133.0
Oryza           AGIS_Os01g046620               36.54        104        4.5e-20      82.0
Oryza           AGIS_Os05g008160               37.50        104        4.5e-20      82.0
Oryza           AGIS_Os05g038960               37.50        104        8.7e-20      81.3
Zea             Zm00014ba203390                65.45        110        4.3e-48      152.0
Zea             Zm00014ba124660                58.04        112        2.9e-40      132.0
Zea             Zm00014ba038710                61.96        92         7.4e-36      121.0
Zea             Zm00014ba307920                35.19        108        4.9e-19      78.6
Zea             Zm00014ba180850                34.62        104        1.6e-18      77.4
=====================================================================================
```

## Contact
* Mingzhu Yan:     ymz7113@163.com
* Zixin Yu:        18713111991@163.com
* Wenzhao Xie:     wzxie@hebtu.edu.cn
