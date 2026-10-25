"""Gera memórias editáveis exclusivamente de divulgações públicas e premissas didáticas."""
from pathlib import Path
from decimal import Decimal
import csv,json
from suplemento_auditoria import program_rows,risk_rows
O=Path(__file__).resolve().parent
def write(name,headers,rows):
    with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)
def read(name):
    with (O/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
data=read('dados_CVM_SLC_2025.csv')
def cvm(code,kind='BPA',year='2025-12-31'):
    rows=[r for r in data if r['arquivo']==f'dfp_cia_aberta_{kind}_con_2025.csv' and r.get('DT_FIM_EXERC')==year and r.get('VERSAO')=='1' and r.get('CD_CONTA')==code and r.get('ORDEM_EXERC')=='ÚLTIMO']
    assert len(rows)==1,(code,len(rows))
    assert rows[0]['ESCALA_MOEDA']=='MIL' and rows[0]['MOEDA']=='REAL'
    return Decimal(rows[0]['VL_CONTA'])
checks=[('ativo_total','1',cvm('1'),21341432,'F01 p.105'),
 ('imobilizado_nota14','1.02.03.01 + 1.02.03.03',cvm('1.02.03.01')+cvm('1.02.03.03'),7111885,'F01 pp.105,156-158; exclui direito de uso'),
 ('estoques','1.01.04',cvm('1.01.04'),3722611,'F01 p.105'),
 ('biologicos','1.01.05',cvm('1.01.05'),2350421,'F01 p.105'),
 ('caixa','1.01.01',cvm('1.01.01'),2647586,'F01 p.105'),
 ('receita_liquida','3.01.01',cvm('3.01.01','DRE'),8553147,'F01 p.107; agregado 3.01 inclui variacao de valor justo/VRL de 1206067')]
write('conferencia_CVM_PT500.csv',['rubrica','codigo_CVM','CVM_R_mil','RI_R_mil','diferenca_R_mil','fonte'],
      [[label,code,str(value),real,str(value-real),source] for label,code,value,real,source in checks])
assert all(value==real for label,code,value,real,source in checks)
roll=5417528+342035+1730224-17941+3610-15526-348045
cash=1979575+1808281-1810196+669926
crop=1700088+93331+5266078+1107474-5946484
prov=13741+2118+64592-2045+2909-556
revenue=8810111+344800-601764
assets=25130398+4628111-8417077
recs=[['Imobilizado',roll,7111885,roll-7111885,'F01 pp.105,156-158'],
      ['Caixa/DFC',cash,2647586,cash-2647586,'F01 pp.105,111-112'],
      ['Culturas biológicas',crop,2220487,crop-2220487,'F01 p.131'],
      ['Provisão litígios',prov,80759,prov-80759,'F01 pp.175-176'],
      ['Receita segmentos',revenue,8553147,revenue-8553147,'F01 pp.107,222'],
      ['Ativo segmentos',assets,21341432,assets-21341432,'F01 pp.105,222'],
      ['CVM imobilizado agregado',7111885+2763422,int(cvm('1.02.03')),7111885+2763422-int(cvm('1.02.03')),'F02 códigos 1.02.03.01/02/03'],
      ['CVM receita agregada',8553147+1206067,int(cvm('3.01','DRE')),8553147+1206067-int(cvm('3.01','DRE')),'F02 códigos 3.01.01/02; F01 p.107']]
assert all(r[3]==0 for r in recs)
write('conciliacoes_publicas_PT520.csv',['procedimento','esperado_R_mil','publicado_R_mil','diferenca_R_mil','fonte'],recs)
area=Decimal(109768); prod=Decimal('68.59'); price=Decimal('97.68'); base=area*prod*price/1000
scens=[('Base pública',1,1),('Preço -5%',0.95,1),('Preço +5%',1.05,1),('Produtividade -10%',1,0.9),('Preço -5% e produtividade -10%',0.95,0.9),('Preço +5% e produtividade +10%',1.05,1.1)]
rows=[]
for name,p,y in scens:
    result=base*Decimal(str(p))*Decimal(str(y))
    rows.append([name,area,prod,price,p,y,f'{result:.2f}',f'{result-base:.2f}','SIMULADO: receita bruta potencial; nao e valor justo','F01 p.132'])
write('sensibilidade_PT540.csv',['cenario','area_ha_interpretada','produtividade_sc_ha','preco_R_sc','fator_preco','fator_produtividade','receita_potencial_R_mil','delta_R_mil','natureza','fonte'],rows)
write('programas_auditoria.csv',['ciclo','risco_afirmacao','natureza_procedimento','epoca','extensao','evidencia_resultado_limite','classificacao'],program_rows())
write('matriz_riscos_respostas.csv',['risco','afirmacoes_avaliacao','resposta_referencia'],risk_rows())
calc={'natureza':'CALCULOS SOBRE SALDOS PUBLICOS; cenarios explicitamente sinteticos',
      'fontes':'F01 pp.105-112,167-171; F02 DFP2025 consolidado versao1',
      'liquidez_corrente':9845683/5465900,'capital_giro_R_mil':9845683-5465900,
      'cobertura_sem_estoques_biologicos':(9845683-3722611-2350421)/5465900,
      'caixa_passivo_circulante':2647586/5465900,'caixa_emprestimos_circulantes':2647586/1591681,
      'imobilizado_percentual_ativo':7111885/21341432*100,
      'MG_0_5pct_receita_R_mil':8553147*.005,'referencia_5pct_LAIR_R_mil':713681*.05,
      'referencia_0_25pct_ativo_R_mil':21341432*.0025,'execucao_biologicos_R_mil':23504.21*.7,
      'diferenca_divida_gerencial_contabil_R_mil':7809254-7728284,
      'composicao_CVM_imobilizado':'6781875 operacao + 330010 andamento + 2763422 direito uso = 9875307; base nota14 = 7111885',
      'receita_bruta_potencial_soja_R_mil':str(base),'formula_soja':'109768 * 68.59 * 97.68 / 1000; cenarios multiplicam preco e produtividade; nao e valor justo'}
(O/'calculos_complementares.json').write_text(json.dumps(calc,ensure_ascii=False,indent=2),encoding='utf-8')
write('controle_circularizacao_PT505.csv',['id','terceiro','saldo_contabil','canal_validado','primeiro_envio','segundo_envio','resposta','divergencia','evidencia_alternativa','conclusao'],[])
parties=[['SLC-MIT','controlada',15669,'controladora','crédito'],['Pioneira','controlada',2755,'controladora','crédito'],['Preciosa','controlada',948,'controladora','crédito'],['Centro-Oeste','controlada',43405,'controladora','crédito'],['Perdizes','controlada',7280,'controladora','crédito'],['Sierentz','controlada',16457,'controladora','crédito'],['SLC Participações','controladora da emissora',216,'individual e consolidado','crédito'],['SLC Máquinas','parte relacionada',16380,'consolidado','passivo de arrendamento'],['Outros saldos nota16','partes relacionadas',139,'consolidado','passivo não arrendamento']]
assert sum(r[2] for r in parties[:7])==86730
write('partes_relacionadas_PT550.csv',['entidade','vinculo','saldo_R_mil','escopo','natureza'],parties)
entities=[['SLC Agrícola S.A.','emissora','Controladora e consolidação'],['SLC Investimentos','100% antes incorporação','Incorporada pela LandCo em 02/06/2025']]
for n in ['Parnaíba','Planorte','Pamplona','Planalto','Palmares','Parnaguá','Paiaguás','Paysandu','SLC Perdizes','Centro-Oeste','SLC Ventures','SLC-MIT','SLC LandCo','Pamplona Minas Gerais']:
    entities.append([n,'100%','Controlada; consolidação integral'])
entities += [['Preciosa','55%','Controle das atividades relevantes; integral'],['Pioneira','50%','Controle das atividades relevantes; integral'],['Paineira','6,45% direta','Controlada com vínculo indireto; não inferir só pelo direto'],['Sierentz','22,29% direta','77,71% via Centro-Oeste; grupo 100%'],['Piratini','50%','Controle contratual / FIP; integral'],['SLC Jaborandi','50%','Controle contratual / FIP; integral'],['Paladino','50%','Controle contratual / FIP; integral'],['Paladino Participações','50%','Controle contratual / FIP; integral'],['SLC São Desidério','indireta','100% de Paladino Participações'],['Hangar Capri','33,33%','Controle compartilhado; equivalência']]
write('componentes_PT600.csv',['entidade','participacao_direta','tratamento'],entities)
# Atualizar triagem analítica por ambos os critérios, sem reduzir à variação relativa.
rows=read('analise_horizontal_PT520.csv')
for r in rows:
    r['limite_absoluto_R_mil']='42765.735'
    r['investigar']=str(abs(float(r['variacao_R_mil']))>42765.735 or abs(float(r['variacao_percentual']))>15)
write('analise_horizontal_PT520.csv',list(rows[0]),[list(r.values()) for r in rows])
print('Conferência CVM: 6/6; conciliações: 8/8; programas: 12; componentes:',len(entities))
