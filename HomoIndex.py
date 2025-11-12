#!/usr/bin python3
# -*- coding: utf-8 -*-

"""
Script: HomoIndex.py
Function:
1. Count total species and orthogroups from Orthogroups.tsv of a given genus.
2. Query one or more gene IDs and output homologous genes in the same orthogroup.
3. Automatically locate the Orthogroups.tsv file from ./genus/<genus_name>/.
4. Write results to individual text files and generate a summary table (summary.tsv).
5. Provide clear error messages for missing genus or missing Orthogroups.tsv.

Usage:
    python HomoIndex.py --genus Arabidopsis --gene GWHPCBHR067821
    python HomoIndex.py --genus Arabidopsis --gene_list genes.txt
"""

import pandas as pd
import argparse
import os
import sys

def query_gene(database, gene_id, outdir):
    """Query homologous genes of one gene and save result to a text file."""
    df = pd.read_csv(database, sep='\t', dtype=str).fillna('')
    num_species = len(df.columns) - 1
    num_orthogroups = len(df)

    output_file = os.path.join(outdir, f"{gene_id}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Total species: {num_species}\n")
        f.write(f"Total orthogroups: {num_orthogroups}\n\n")

        mask = df.apply(lambda row: any(gene_id in str(cell) for cell in row[1:]), axis=1)
        results = df[mask]

        if results.empty:
            f.write(f"Gene '{gene_id}' not found in any orthogroup.\n")
            print(f"[INFO] Gene '{gene_id}' not found.")
            return None

        row = results.iloc[0]
        orthogroup = row.iloc[0]
        f.write(f"Gene '{gene_id}' belongs to Orthogroup: {orthogroup}\n")
        f.write("Homologous genes in the same orthogroup:\n\n")

        species_list = []
        gene_count = 0

        for species in df.columns[1:]:
            genes = str(row[species]).strip()
            if genes:
                gene_list = [g.strip() for g in genes.split(', ')]
                gene_count += len(gene_list)
                species_list.append(species)
                f.write(f"{species}: {', '.join(gene_list)}\n")

        f.write("\n---\n")

    print(f"[OK] Result written to: {output_file}")
    return {
        "Gene_ID": gene_id,
        "Orthogroup_ID": orthogroup,
        "Species_Count": len(species_list),
        "Gene_Count": gene_count,
        "Species_List": "; ".join(species_list)
    }


def list_available_genus():
    """List all available genus directories under ./genus/"""
    if not os.path.exists("genus"):
        print("[ERROR] Directory 'genus/' not found in current path.")
        sys.exit(1)
    available = [d for d in os.listdir("genus") if os.path.isdir(os.path.join("genus", d))]
    return sorted(available)


def main():
    parser = argparse.ArgumentParser(description="Query homologous genes by genus.")
    parser.add_argument("--genus", "-G", required=True, help="Genus name under ./genus/ directory")
    parser.add_argument("--gene", "-g", help="Single gene ID to query")
    parser.add_argument("--gene_list", "-l", help="Text file containing multiple gene IDs (one per line)")
    parser.add_argument("--outdir", "-o", default="results", help="Output directory (default: ./results/)")
    args = parser.parse_args()

    genus_dir = os.path.join("genus", args.genus)
    database_path = os.path.join(genus_dir, "Orthogroups.tsv")

    # 检查属目录是否存在
    if not os.path.exists(genus_dir):
        print(f"[ERROR] Genus '{args.genus}' directory not found!")
        print("Available genus names:")
        for g in list_available_genus():
            print(f"  - {g}")
        sys.exit(1)

    # 检查 Orthogroups.tsv 是否存在
    if not os.path.exists(database_path):
        print(f"[ERROR] Missing file: {database_path}")
        print("Make sure Orthogroups.tsv exists in this genus folder.")
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)
    summary_data = []

    # 查询单基因或多基因
    if args.gene:
        result = query_gene(database_path, args.gene, args.outdir)
        if result:
            summary_data.append(result)
    elif args.gene_list:
        with open(args.gene_list, "r") as infile:
            for line in infile:
                gene_id = line.strip()
                if gene_id:
                    result = query_gene(database_path, gene_id, args.outdir)
                    if result:
                        summary_data.append(result)
    else:
        print("[ERROR] Please provide either --gene or --gene_list")
        sys.exit(1)

    # 4️⃣ 生成 summary.tsv
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_file = os.path.join(args.outdir, "summary.tsv")
        summary_df.to_csv(summary_file, sep='\t', index=False)
        print(f"[OK] Summary table saved to: {summary_file}")


if __name__ == "__main__":
    main()

