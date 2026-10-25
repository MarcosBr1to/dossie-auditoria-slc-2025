"""Divide o CSV sintético em partes menores e gera prévia de 5.000 linhas.

Execute na pasta que contém a base: python split_base.py
Arquivos da pasta base_partes/ são cópias completas, sem omissões, quando unidos
na ordem do manifesto; não são registros reais da SLC Agrícola.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "base_imobilizado_sintetica_500000.csv"
PART_DIR = HERE / "base_partes"
PART_DIR.mkdir(exist_ok=True)
PART_SIZE = 25_000
PREVIEW_EVERY = 100

parts = []
writer = None
handle = None
count = 0
part_count = 0
part_sum = 0
total_sum = 0
preview_count = 0

with SOURCE.open(encoding="utf-8-sig", newline="") as source, \
     (HERE / "base_sintetica_previa_5000.csv").open("w", encoding="utf-8-sig", newline="") as sample_file:
    reader = csv.DictReader(source)
    assert reader.fieldnames is not None
    sample_writer = csv.DictWriter(sample_file, fieldnames=reader.fieldnames)
    sample_writer.writeheader()
    for row in reader:
        if count % PART_SIZE == 0:
            if handle is not None:
                handle.close()
                parts[-1]["linhas"] = part_count
                parts[-1]["valor_contabil_centavos"] = part_sum
            part_number = len(parts) + 1
            name = f"base_sintetica_parte_{part_number:02d}.csv"
            handle = (PART_DIR / name).open("w", encoding="utf-8-sig", newline="")
            writer = csv.DictWriter(handle, fieldnames=reader.fieldnames)
            writer.writeheader()
            parts.append({"arquivo": name})
            part_count = 0
            part_sum = 0
        assert writer is not None
        writer.writerow(row)
        value = int(row["valor_contabil_centavos"])
        part_count += 1
        part_sum += value
        total_sum += value
        if count % PREVIEW_EVERY == 0:
            sample_writer.writerow(row)
            preview_count += 1
        count += 1
if handle is not None:
    handle.close()
    parts[-1]["linhas"] = part_count
    parts[-1]["valor_contabil_centavos"] = part_sum

assert count == 500_000 and len(parts) == 20 and preview_count == 5_000
assert sum(p["linhas"] for p in parts) == count
assert sum(p["valor_contabil_centavos"] for p in parts) == total_sum == 711_188_500_000
for p in parts:
    file = PART_DIR / p["arquivo"]
    p["tamanho_bytes"] = file.stat().st_size
    p["sha256"] = hashlib.sha256(file.read_bytes()).hexdigest()
manifest = {
    "aviso": "DADOS SINTETICOS; nenhuma linha e registro real da SLC Agricola",
    "arquivo_original": SOURCE.name,
    "linhas_original": count,
    "partes": parts,
    "previa": "base_sintetica_previa_5000.csv",
    "linhas_previa": preview_count,
    "regra_previa": "cada 100o registro; somente navegacao visual, nao e amostra de auditoria",
    "valor_total_centavos": total_sum,
    "sha256_original": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
}
(PART_DIR / "manifesto_partes.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{count} registros divididos em {len(parts)} arquivos de {PART_SIZE}; prévia com {preview_count} registros")
