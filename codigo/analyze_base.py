"""Reexecuta conciliação, testes de população e amostragem da base sintética.

Execução: python work/analyze_base.py (após generate_base.py).
"""
from __future__ import annotations

import csv
import json
import random
import math
from collections import Counter, defaultdict
from pathlib import Path
from caminhos import ROOT, caminho

HERE = ROOT
OUT = ROOT
BASE = caminho("base_imobilizado_sintetica_500000.csv", OUT)
RNG = random.Random(53024120631)

rows = []
with BASE.open(encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        for key in ("custo_bruto_centavos", "depreciacao_acumulada_centavos", "valor_contabil_centavos", "valor_suporte_sintetico_centavos"):
            r[key] = int(r[key])
        rows.append(r)
assert len(rows) == 500_000

def tests(r):
    hits = []
    if r["custo_bruto_centavos"] - r["depreciacao_acumulada_centavos"] != r["valor_contabil_centavos"]:
        hits.append("rollforward_invalido")
    if r["valor_suporte_sintetico_centavos"] != r["valor_contabil_centavos"]:
        hits.append("divergencia_suporte")
    if r["data_entrada"] > "2025-12-31":
        hits.append("entrada_apos_corte")
    if r["classe"] == "terras_cultura" and r["depreciacao_acumulada_centavos"]:
        hits.append("depreciacao_terras")
    return hits

pop_counts = Counter()
detected = []
for r in rows:
    for h in tests(r):
        pop_counts[h] += 1
        detected.append((r["registro_id"], h))

oracle = set()
with (caminho("excecoes_inseridas_gabarito.csv", OUT)).open(encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        oracle.add((r["registro_id"], r["tipo_excecao"]))
detected_set = set(detected)
assert detected_set == oracle, (len(detected_set - oracle), len(oracle - detected_set))
with (caminho('excecoes_detectadas.csv', OUT)).open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['registro_id','tipo_excecao','consta_gabarito','natureza'])
    w.writerows((rid,rule,(rid,rule) in oracle,'SINTETICO') for rid,rule in sorted(detected_set))

totals = defaultdict(int)
counts = Counter()
for r in rows:
    totals[r["classe"]] += r["valor_contabil_centavos"]
    counts[r["classe"]] += 1
with (caminho("conciliacao_imobilizado.csv", OUT)).open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["classe", "n_registros_sinteticos", "base_R_mil", "nota14_R_mil", "diferenca_R_mil"])
    expected = {"terras_cultura":3315500,"correcao_solo":1052113,"predios_benfeitorias":797295,
                "equipamentos_agricolas":1409647,"veiculos":123837,"moveis_utensilios":29100,
                "equipamentos_escritorio":35871,"outros":18512,"imobilizado_andamento":330010}
    for cls, exp in expected.items():
        actual = totals[cls] / 100_000
        w.writerow([cls, counts[cls], f"{actual:.2f}", exp, f"{actual-exp:.2f}"])
    w.writerow(["TOTAL",len(rows),f"{sum(totals.values())/100_000:.2f}",7111885,"0.00"])

# Amostra aleatória simples, sem reposição, reproduzível. Também separamos
# uma subamostra dirigida: os 50 maiores itens. Só a aleatória admite projeção.
random_idx = set(RNG.sample(range(len(rows)), 1200))
top50 = sorted(range(len(rows)), key=lambda i: rows[i]["valor_contabil_centavos"], reverse=True)[:50]
sample_idx = random_idx | set(top50)
sample = []
for i in sorted(sample_idx):
    r = rows[i]
    selection = "aleatoria+maior_valor" if i in random_idx and i in top50 else ("maior_valor" if i in top50 else "aleatoria")
    sample.append({"registro_id":r["registro_id"],"tipo_selecao":selection,
                   "classe":r["classe"], "valor_contabil_centavos":r["valor_contabil_centavos"],
                   "excecoes_identificadas":";".join(tests(r)),
                   "diferenca_suporte_centavos":r["valor_suporte_sintetico_centavos"]-r["valor_contabil_centavos"]})
with (caminho("amostra_PT530.csv", OUT)).open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(sample[0]))
    w.writeheader(); w.writerows(sample)

random_rows = [r for r in sample if "aleatoria" in r["tipo_selecao"]]
random_errors = [r for r in random_rows if r["diferenca_suporte_centavos"]]
# Projeção por diferença média por item, ilustrativa. Não é estimador monetário
# ótimo para população heterogênea; usar apenas como indicador de triagem.
projected = round(sum(r["diferenca_suporte_centavos"] for r in random_rows)/len(random_rows)*len(rows))

materiality = {
 "base_receita_liquida_2025_R_mil":8553147,
 "percentual_materialidade_global":0.005,
 "materialidade_global_R_mil":round(8553147*0.005,2),
 "materialidade_execucao_percentual_global":0.70,
 "materialidade_execucao_R_mil":round(8553147*0.005*0.70,2),
 "limiar_acumulacao_percentual_global":0.05,
 "limiar_acumulacao_R_mil":round(8553147*0.005*0.05,2),
 "materialidade_especifica_ativo_biologico_R_mil":23504.21,
 "racional":"Receita como base relativamente estável frente ao lucro volátil; percentuais são julgamento didático, não regra da NBC TA 320."
}
(caminho("materialidade_editavel.json", OUT)).write_text(json.dumps(materiality,ensure_ascii=False,indent=2),encoding="utf-8")
analytics = []
for name, v25, v24 in [
    ("ativo_total",21341432,17574342),("imobilizado",7111885,5417528),
    ("estoques",3722611,3780562),("ativos_biologicos",2350421,1785392),
    ("caixa_equivalentes",2647586,1979575),("receita_liquida",8553147,6915764)]:
    analytics.append({"conta":name,"2025_R_mil":v25,"2024_R_mil":v24,
                      "variacao_R_mil":v25-v24,"variacao_percentual":round((v25/v24-1)*100,2),
                      "limite_investigacao_percentual":15,"investigar":abs(v25/v24-1)>0.15})
with (caminho("analise_horizontal_PT520.csv", OUT)).open("w", encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(analytics[0]));w.writeheader();w.writerows(analytics)

results = {
 "natureza":"APENAS TESTES SOBRE DADOS SINTETICOS",
 "populacao":len(rows),"amostra_aleatoria":len(random_rows),"amostra_dirigida_50_maiores":50,
 "excecoes_populacao":dict(pop_counts),"gabarito_total":len(oracle),
 "verdadeiros_positivos":len(detected_set & oracle),"falsos_positivos":len(detected_set-oracle),
 "falsos_negativos":len(oracle-detected_set),
 "registros_distintos_com_excecao":len({rid for rid,rule in detected_set}),
 "fazendas_sinteticas_distintas":len({r['fazenda_sintetica'] for r in rows}),
 "desenho_amostral":{"objetivo":"detectar ao menos um desvio com prevalencia >=0,25%; nao determina precisao monetaria",
 "prevalencia_referencia":0.0025,"risco_nao_detectar":0.05,
 "n_minimo_aproximacao_binomial":math.ceil(math.log(0.05)/math.log(1-0.0025)),
 "n_adotado":1200,"probabilidade_deteccao_no_limiar":1-(1-0.0025)**1200,
 "justificativa_revisao":"Fundamentacao explicitada na revisao; amostra original preservada. Nao e plano previo executado na companhia."},
 "excecoes_suporte_amostra_aleatoria":len(random_errors),
 "diferenca_suporte_amostra_aleatoria_R":sum(r["diferenca_suporte_centavos"] for r in random_rows)/100,
 "projecao_simples_diferenca_media_R":projected/100,
 "diferenca_suporte_populacao_R":sum(r["valor_suporte_sintetico_centavos"]-r["valor_contabil_centavos"] for r in rows)/100,
 "ressalva":"A projeção é indicativa: cadastro heterogêneo e exceções artificiais. Não extrapolar à SLC real.",
 "materialidade":materiality,"analiticos":analytics
}
(caminho("resultados_testes.json", OUT)).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
with (caminho('mapa_distorcoes_PT450.csv', OUT)).open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['tipo','n','efeito_campo_R','tratamento','status','conclusao'])
    w.writerow(['divergencia_suporte',pop_counts['divergencia_suporte'],results['diferenca_suporte_populacao_R'],'suporte menos contabil; nao e ajuste comprovado','SIMULADO - nao corrigido na base','menor que limiar quantitativo; acumulado por finalidade didatica'])
    w.writerow(['entrada_apos_corte',pop_counts['entrada_apos_corte'],'nao determinado','saldo dos itens nao equivale automaticamente a distorcao','SIMULADO - nao corrigido na base','avaliacao qualitativa de corte; requer documento real'])
    w.writerow(['depreciacao_terras',pop_counts['depreciacao_terras'],sum(r['depreciacao_acumulada_centavos'] for r in rows if 'depreciacao_terras' in tests(r))/100,'efeito no campo depreciacao; bruto tambem alterado, liquido preservado','SIMULADO - nao corrigido na base','nao somar a diferenca de suporte como erro contabil'])
    w.writerow(['erros reais da SLC','desconhecido','desconhecido','sem livros e evidencia primaria','nao determinado','nenhum ajuste real proposto por este estudo'])
print(json.dumps({k:v for k,v in results.items() if k not in ("materialidade","analiticos")},ensure_ascii=False,indent=2))
