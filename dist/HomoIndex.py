#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script: HomoIndexPlain.py
Function: Query homologous gene information from plaintext SQLite databases.
		  Supports single gene query (-g) or batch query via gene list file (-l).
		  Uses genus/<genus>/<genus>.db when it already exists.
		  Otherwise downloads the plaintext database from the published Zenodo records.
Usage:
   - Single Gene:  python HomoIndexPlain.py --genus Aegilops --gene AeUmb.TA1851.r1.7UG0045140
   - Batch Query:  python HomoIndexPlain.py --genus Aegilops --gene-list genes.txt -o batch_output.txt
"""

import argparse
import os
import sqlite3
import sys
import urllib.request

# 新版本四个已发布记录。草稿在点击 Publish 之后，这些 ID 才能公开下载。
ZENODO_RECORD_IDS = [
	"23383060",  # HomoIndex Genomic Database (Part 1)
	"23383076",  # HomoIndex Genomic Database (Part 2)
	"23383086",  # HomoIndex Genomic Database (Part 3)
	"23383085",  # HomoIndex Genomic Database (Part 4)
]

SQLITE_MAGIC = b"SQLite format 3\x00"


def get_file_urls_for_all_records(genus_name):
	"""遍历四个 Zenodo Record，生成明文库的公开下载链接。"""
	filename = f"{genus_name}.db"
	urls = []

	for record_id in ZENODO_RECORD_IDS:
		urls.append(
			f"https://zenodo.org/records/{record_id}/files/{filename}?download=1"
		)
		urls.append(
			f"https://zenodo.org/api/records/{record_id}/files/{filename}/content"
		)

	return urls


def download_file_with_retry(urls, dest_path):
	"""尝试多条公开链接下载文件，成功即止。"""
	opener = urllib.request.build_opener()
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

	last_exception = None
	for url in urls:
		req = urllib.request.Request(url, headers=headers)
		try:
			with opener.open(req) as response, open(dest_path, "wb") as out_file:
				total_size = response.headers.get("Content-Length")
				if total_size is not None:
					total_size = int(total_size)

				downloaded = 0
				chunk_size = 1024 * 1024

				while True:
					chunk = response.read(chunk_size)
					if not chunk:
						break
					out_file.write(chunk)
					downloaded += len(chunk)

					if total_size:
						percent = (downloaded / total_size) * 100
						mb_downloaded = downloaded / (1024 * 1024)
						mb_total = total_size / (1024 * 1024)
						sys.stdout.write(
							f"\r[Downloading] {percent:5.1f}% ({mb_downloaded:6.1f} / {mb_total:.1f} MB)"
						)
					else:
						mb_downloaded = downloaded / (1024 * 1024)
						sys.stdout.write(
							f"\r[Downloading] {mb_downloaded:6.1f} MB transferred"
						)
					sys.stdout.flush()

				sys.stdout.write("\n")
				sys.stdout.flush()

			with open(dest_path, "rb") as handle:
				magic = handle.read(len(SQLITE_MAGIC))
			if magic != SQLITE_MAGIC:
				raise ValueError("downloaded file is not a SQLite database")
			return True
		except Exception as e:
			last_exception = e
			if os.path.exists(dest_path):
				os.remove(dest_path)
			continue

	raise last_exception


def ensure_genus_database(genus):
	"""使用本地 genus/<genus>/<genus>.db；没有则从 Zenodo 下载并保留。"""
	genus_dir = os.path.join("genus", genus)
	db_path = os.path.join(genus_dir, f"{genus}.db")

	if os.path.exists(db_path):
		return db_path

	os.makedirs(genus_dir, exist_ok=True)
	filename = f"{genus}.db"

	print(f"[INFO] Local database for genus '{genus}' not found.")
	print(f"[INFO] Connecting to Zenodo repository to download '{filename}' ...")
	print("[INFO] Network transfer in progress. Please wait for completion.")

	try:
		download_file_with_retry(get_file_urls_for_all_records(genus), db_path)
		print(f"[OK] Downloaded successfully to '{db_path}'.")
	except Exception as e:
		print(f"\n[ERROR] Failed to download database for genus '{genus}'.")
		print(f"[ERROR] Details: {e}")
		print("--------------------------------------------------------------------------------")
		print("【排查建议】：")
		print("1. 检查网络连接或网络代理是否正常。")
		print(f"2. 确认 '{filename}' 已上传，并且对应的新版本草稿已经 Publish。")
		print("--------------------------------------------------------------------------------\n")
		if os.path.exists(db_path):
			os.remove(db_path)
		sys.exit(1)

	return db_path


def query_homology_batch(db_path, gene_ids, output_path=None):
	"""批量查询 JCVI 与 BLASTP 表并支持保存结果。"""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	lines = []
	total_genes = len(gene_ids)

	for idx, gene_id in enumerate(gene_ids, 1):
		lines.append(
			f"==================== Query Results for ({idx}/{total_genes}): {gene_id} ===================="
		)

		cursor.execute(
			"""
			SELECT homolog_id FROM jcvi WHERE gene_id = ?
		""",
			(gene_id,),
		)
		homolog_res = cursor.fetchone()

		if homolog_res:
			homolog_id = homolog_res[0]
			cursor.execute(
				"""
				SELECT species_name, gene_id FROM jcvi WHERE homolog_id = ?
			""",
				(homolog_id,),
			)
			cluster_genes = cursor.fetchall()

			lines.append(
				f"\n[JCVI Homology Group]: Found {len(cluster_genes)} clusters"
			)
			lines.append("species\tgene ID")
			for sp, g_id in cluster_genes:
				lines.append(f"{sp}\t{g_id}")
		else:
			lines.append(
				"\n[JCVI Homology Group]: No JCVI record found for this gene."
			)

		cursor.execute(
			"""
			SELECT subject_id, identity, align_len, evalue, bit_score, model_plant
			FROM blastp
			WHERE query_id = ?
		""",
			(gene_id,),
		)
		blast_res = cursor.fetchall()

		if blast_res:
			lines.append(f"\n[BLASTP Best Hits]: Found {len(blast_res)} matches")
			lines.append(
				f"{'Model Plant':<15} {'Subject ID':<30} {'Identity(%)':<12} {'AlignLen':<10} {'E-value':<12} {'BitScore':<10}"
			)
			lines.append("-" * 90)
			for sub, iden, alen, evalue, score, plant in blast_res:
				lines.append(
					f"{plant:<15} {sub:<30} {iden:<12.2f} {alen:<10} {evalue:<12.1e} {score:<10.1f}"
				)
		else:
			lines.append(
				"\n[BLASTP Best Hits]: No BLASTP matches found for this gene."
			)

		lines.append(
			"======================================================================\n"
		)

	conn.close()

	output_content = "\n".join(lines)
	print(output_content)

	if output_path:
		with open(output_path, "w", encoding="utf-8") as f:
			f.write(output_content + "\n")
		print(f"[OK] Batch query results written to: {output_path}")


def main():
	parser = argparse.ArgumentParser(
		description="HomoIndex plaintext database query client."
	)
	parser.add_argument(
		"--genus", "-G", required=True, help="Genus name (e.g., Aegilops)"
	)
	parser.add_argument("--gene", "-g", help="Single gene ID to query")
	parser.add_argument(
		"--gene-list",
		"-l",
		help="File containing list of gene IDs (one ID per line)",
	)
	parser.add_argument(
		"--output",
		"-o",
		help="Output file path for query results (optional)",
	)

	args = parser.parse_args()

	if not args.gene and not args.gene_list:
		print("[ERROR] Please specify either --gene (-g) or --gene-list (-l).")
		sys.exit(1)

	gene_ids = []
	if args.gene:
		gene_ids.append(args.gene.strip())

	if args.gene_list:
		if not os.path.exists(args.gene_list):
			print(f"[ERROR] Gene list file '{args.gene_list}' not found.")
			sys.exit(1)
		with open(args.gene_list, "r", encoding="utf-8") as f:
			for line in f:
				gid = line.strip()
				if gid and not gid.startswith("#"):
					gene_ids.append(gid)

	if not gene_ids:
		print("[ERROR] No valid gene IDs provided for query.")
		sys.exit(1)

	db_path = ensure_genus_database(args.genus)
	query_homology_batch(db_path, gene_ids, args.output)


if __name__ == "__main__":
	main()
