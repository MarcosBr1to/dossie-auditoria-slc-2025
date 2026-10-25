"""Gera cadastro sintético de imobilizado da SLC Agrícola para exercício didático.

Não contém registros reais. Valores de controle são saldos publicados, em R$ mil.
Execução: python codigo/generate_base.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from caminhos import ROOT, caminho

HERE = ROOT
OUT = ROOT
OUT.mkdir(exist_ok=True)
SEED = 24120631
RNG = random.Random(SEED)

# Nota 14, demonstrações consolidadas de 31/12/2025, R$ mil.
CLASSES = [
    ("terras_cultura", 1_000, 3_315_500),
    ("correcao_solo", 350_000, 1_052_113),
    ("predios_benfeitorias", 10_000, 797_295),
    ("equipamentos_agricolas", 100_000, 1_409_647),
    ("veiculos", 5_000, 123_837),
    ("moveis_utensilios", 10_000, 29_100),
    ("equipamentos_escritorio", 10_000, 35_871),
    ("outros", 10_000, 18_512),
    ("imobilizado_andamento", 4_000, 330_010),
]
assert sum(n for _, n, _ in CLASSES) == 500_000
assert sum(v for _, _, v in CLASSES) == 7_111_885

FIELDS = ["registro_id", "classe", "fazenda_sintetica", "componente", "data_entrada",
          "custo_bruto_centavos", "depreciacao_acumulada_centavos", "valor_contabil_centavos",
          "valor_suporte_sintetico_centavos", "documento_sintetico_id", "status_sintetico"]

def allocate(total: int, n: int) -> list[int]:
    """Particiona centavos em valores positivos individuais, sem arredondar o total."""
    weights = [RNG.randint(250, 1750) for _ in range(n)]
    denom = sum(weights)
    vals = [max(1, total * w // denom) for w in weights]
    vals[-1] += total - sum(vals)
    assert min(vals) > 0 and sum(vals) == total
    return vals

base = caminho("base_imobilizado_sintetica_500000.csv", OUT)
oracle = caminho("excecoes_inseridas_gabarito.csv", OUT)
totals = defaultdict(int)
injected = defaultdict(int)
global_id = 0
with base.open("w", newline="", encoding="utf-8-sig") as f, oracle.open("w", newline="", encoding="utf-8-sig") as o:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    ow = csv.writer(o)
    w.writeheader()
    ow.writerow(["registro_id", "tipo_excecao", "valor_efeito_centavos", "observacao"])
    for cls, count, amount_thousands in CLASSES:
        amounts = allocate(amount_thousands * 100_000, count)
        for j, carrying in enumerate(amounts, 1):
            global_id += 1
            rid = f"SYN-IMOB-{global_id:06d}"
            farm = f"FAZENDA-SINT-{(global_id - 1) % 37 + 1:02d}"
            unit = f"{cls.upper()}-{farm}-{j:06d}"
            entered = date(2012, 1, 1) + timedelta(days=RNG.randrange(0, 5114))
            # Valor líquido coincide com o saldo publicado; o custo e a depreciação
            # são somente atributos de cadastro sintético, não saldos divulgados.
            dep = 0 if cls in ("terras_cultura", "imobilizado_andamento") else carrying * RNG.randrange(0, 80) // 100
            gross = carrying + dep
            support = carrying
            status = "ativo"
            if global_id % 479 == 0:
                support += max(100_000, carrying // 100)
                ow.writerow([rid, "divergencia_suporte", support - carrying, "suporte sintético > razão sintético"])
                injected["divergencia_suporte"] += 1
            if global_id % 997 == 0:
                entered = date(2026, 1, 1) + timedelta(days=global_id % 30)
                ow.writerow([rid, "entrada_apos_corte", 0, "data sintética após 31/12/2025"])
                injected["entrada_apos_corte"] += 1
            if cls == "terras_cultura" and j % 127 == 0:
                dep = max(100_000, carrying // 100)
                gross = carrying + dep
                ow.writerow([rid, "depreciacao_terras", dep, "terra sintética com depreciação indevida"])
                injected["depreciacao_terras"] += 1
            row = dict(registro_id=rid, classe=cls, fazenda_sintetica=farm,
                       componente=unit, data_entrada=entered.isoformat(),
                       custo_bruto_centavos=gross, depreciacao_acumulada_centavos=dep,
                       valor_contabil_centavos=carrying,
                       valor_suporte_sintetico_centavos=support,
                       documento_sintetico_id=f"DOC-SYN-{global_id:06d}", status_sintetico=status)
            w.writerow(row)
            totals[cls] += carrying

assert global_id == 500_000
assert sum(totals.values()) == 711_188_500_000

sha = hashlib.sha256(base.read_bytes()).hexdigest()
manifest = {
    "natureza": "DADOS SINTETICOS - nao sao registros da SLC Agricola",
    "semente": SEED, "linhas": global_id,
    "unidade_base": "centavos de real", "unidade_demonstracoes": "milhares de reais",
    "totais_por_classe_centavos": dict(totals),
    "total_base_centavos": sum(totals.values()),
    "total_publicado_centavos": 711_188_500_000,
    "diferenca_centavos": sum(totals.values()) - 711_188_500_000,
    "excecoes_inseridas": dict(injected), "sha256_base": sha,
}
(caminho("manifesto_base.json", OUT)).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(manifest, ensure_ascii=False, indent=2))
