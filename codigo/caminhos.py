"""Caminhos únicos dos artefatos, relativos à raiz do repositório.

Os nomes preservados no dossiê podem ser localizados por este catálogo.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARQUIVOS = {'INSTRUCOES_GITHUB.md': 'documentacao/INSTRUCOES_GITHUB.md',
 'REVISAO_CONFORMIDADE.md': 'validacao/REVISAO_CONFORMIDADE.md',
 'amostra_PT530.csv': 'papeis_trabalho/amostra_PT530.csv',
 'analise_horizontal_PT520.csv': 'papeis_trabalho/analise_horizontal_PT520.csv',
 'analyze_base.py': 'codigo/analyze_base.py',
 'audit_support.py': 'codigo/audit_support.py',
 'base_imobilizado_sintetica_500000.csv': 'dados/sinteticos/base_imobilizado_sintetica_500000.csv',
 'base_partes': 'dados/sinteticos/base_partes',
 'base_sintetica_previa_5000.csv': 'dados/sinteticos/base_sintetica_previa_5000.csv',
 'build_dossier.py': 'codigo/build_dossier.py',
 'calculos_complementares.json': 'papeis_trabalho/calculos_complementares.json',
 'componentes_PT600.csv': 'papeis_trabalho/componentes_PT600.csv',
 'conciliacao_imobilizado.csv': 'papeis_trabalho/conciliacao_imobilizado.csv',
 'conciliacoes_publicas_PT520.csv': 'papeis_trabalho/conciliacoes_publicas_PT520.csv',
 'conferencia_CVM_PT500.csv': 'papeis_trabalho/conferencia_CVM_PT500.csv',
 'controle_circularizacao_PT505.csv': 'papeis_trabalho/controle_circularizacao_PT505.csv',
 'dados_CVM_SLC_2025.csv': 'dados/publicos/dados_CVM_SLC_2025.csv',
 'dicionario_base.md': 'dados/sinteticos/dicionario_base.md',
 'dossie_auditoria_SLC_2025.pdf': 'dossie/dossie_auditoria_SLC_2025.pdf',
 'dossie_editavel.md': 'dossie/dossie_editavel.md',
 'excecoes_detectadas.csv': 'papeis_trabalho/excecoes_detectadas.csv',
 'excecoes_inseridas_gabarito.csv': 'dados/sinteticos/excecoes_inseridas_gabarito.csv',
 'fontes.csv': 'fontes/fontes.csv',
 'generate_base.py': 'codigo/generate_base.py',
 'manifesto_arquivos.json': 'validacao/manifesto_arquivos.json',
 'manifesto_base.json': 'dados/sinteticos/manifesto_base.json',
 'mapa_distorcoes_PT450.csv': 'papeis_trabalho/mapa_distorcoes_PT450.csv',
 'materialidade_editavel.json': 'papeis_trabalho/materialidade_editavel.json',
 'matriz_cobertura.csv': 'papeis_trabalho/matriz_cobertura.csv',
 'matriz_riscos_respostas.csv': 'papeis_trabalho/matriz_riscos_respostas.csv',
 'partes_relacionadas_PT550.csv': 'papeis_trabalho/partes_relacionadas_PT550.csv',
 'pdf_layout.py': 'codigo/pdf_layout.py',
 'programas_auditoria.csv': 'papeis_trabalho/programas_auditoria.csv',
 'registro_normas.json': 'fontes/registro_normas.json',
 'resultados_testes.json': 'papeis_trabalho/resultados_testes.json',
 'sensibilidade_PT540.csv': 'papeis_trabalho/sensibilidade_PT540.csv',
 'split_base.py': 'codigo/split_base.py',
 'suplemento_auditoria.py': 'codigo/suplemento_auditoria.py',
 'validacao_entrega.json': 'validacao/validacao_entrega.json',
 'validar_entrega.py': 'codigo/validar_entrega.py'}

def caminho(nome, raiz=None):
    """Resolve um artefato conhecido sem depender do diretório do terminal."""
    raiz = ROOT if raiz is None else Path(raiz)
    if nome.startswith('base_partes/'):
        relativo = 'dados/sinteticos/' + nome
    else:
        relativo = ARQUIVOS[nome]
    destino = raiz / relativo
    destino.parent.mkdir(parents=True, exist_ok=True)
    return destino
