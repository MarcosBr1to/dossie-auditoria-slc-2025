"""Verificação reproduzível da entrega; não é revisão independente de auditoria."""
from pathlib import Path
import csv,json,hashlib
from pypdf import PdfReader
O=Path(__file__).resolve().parent
def read(name):
    with (O/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=O/'base_imobilizado_sintetica_500000.csv'
ids=set(); comps=set(); docs=set(); farms=set(); n=0;total=0
with base.open(encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        n+=1;ids.add(r['registro_id']);comps.add(r['componente']);docs.add(r['documento_sintetico_id']);farms.add(r['fazenda_sintetica'])
        assert r['registro_id'].startswith('SYN-')
        total+=int(r['valor_contabil_centavos'])
assert n==len(ids)==len(comps)==len(docs)==500000
assert len(farms)==37 and total==711188500000
manifest=json.loads((O/'manifesto_base.json').read_text(encoding='utf-8'))
assert sha(base)==manifest['sha256_base']
parts=json.loads((O/'base_partes/manifesto_partes.json').read_text(encoding='utf-8'))
with base.open(encoding='utf-8-sig',newline='') as f:
    master=csv.DictReader(f);count=0
    for part in parts['partes']:
        path=O/'base_partes'/part['arquivo'];assert sha(path)==part['sha256']
        for row in read('base_partes/'+part['arquivo']):
            assert row==next(master);count+=1
    assert next(master,None) is None and count==500000
oracle={(r['registro_id'],r['tipo_excecao']) for r in read('excecoes_inseridas_gabarito.csv')}
found={(r['registro_id'],r['tipo_excecao']) for r in read('excecoes_detectadas.csv')}
assert oracle==found and len(found)==1551
assert len({x[0] for x in found})==1550
samples=read('amostra_PT530.csv');assert len(samples)==1249
assert len([r for r in samples if 'aleatoria' in r['tipo_selecao']])==1200
assert len(read('base_sintetica_previa_5000.csv'))==5000
assert all(float(r['diferenca_R_mil'])==0 for r in read('conciliacao_imobilizado.csv'))
assert all(float(r['diferenca_R_mil'])==0 for r in read('conferencia_CVM_PT500.csv'))
assert all(float(r['diferenca_R_mil'])==0 for r in read('conciliacoes_publicas_PT520.csv'))
matrix=read('matriz_cobertura.csv');assert len(matrix)==27
assert len(json.loads((O/'registro_normas.json').read_text(encoding='utf-8')))==27
pdf=PdfReader(O/'dossie_auditoria_SLC_2025.pdf');txt=[p.extract_text() for p in pdf.pages]
assert 'Sumário' in txt[1] and 'Apresentação' in txt[2]
assert 'Marcos' not in txt[0] and 'MARCOS AURÉLIO DE BRITO CUNHA' in txt[0] and '241021631' in txt[0]
assert all('D-'+r['papel_trabalho'].split()[-1] in '\n'.join(txt) for r in matrix)
assert not read('controle_circularizacao_PT505.csv')
checks={'natureza':'Verificacao de consistencia pelo preparador; nao e revisao independente',
 'data':'25/10/2026','matricula':'241021631','resultado':'APROVADO nos testes automatizados descritos',
 'linhas':n,'ids_componentes_documentos_unicos':n,'fazendas_sinteticas':len(farms),'soma_centavos':total,
 'partes':len(parts['partes']),'linhas_partes_identicas':count,'linhas_previa':5000,
 'amostra_ids_unicos':len(samples),'excecoes':len(found),'registros_com_excecao':1550,
 'falsos_positivos':0,'falsos_negativos':0,'papeis_trabalho':len(matrix),'paginas_pdf':len(pdf.pages),
 'fontes_principais':len(read('fontes.csv')),'normas_documentos_individuais':27,
 'conferencias_CVM':6,'conciliacoes_publicas':8,
 'limites':'Sem testes internos, revisao por terceiro ou asseguracao. Publicacao remota verificada separadamente.'}
(O/'validacao_entrega.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
files={p.relative_to(O).as_posix():sha(p) for p in sorted(O.rglob('*')) if p.is_file() and not any(x in p.parts for x in ['__pycache__','.git']) and p.suffix not in ['.zip','.pyc'] and p.name!='manifesto_arquivos.json'}
(O/'manifesto_arquivos.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
