# Dossiê de auditoria didático: SLC Agrícola S.A. (2025)

**Preparador:** Marcos Aurélio de Brito Cunha  
**Matrícula:** 241021631  
**Data de preparação:** 25/10/2026  

**Natureza:** trabalho acadêmico baseado em fontes públicas e dados sintéticos. Não constitui auditoria independente nem opinião profissional sobre a companhia.

## Organização

| Arquivo | Conteúdo |
|---|---|
| `dossie_auditoria_SLC_2025.pdf` | Sumário, apresentação, 27 papéis de trabalho, anexos, conclusão e fontes; numeração inferior direita |
| `dossie_editavel.md` | Versão editável integral do dossiê |
| `base_imobilizado_sintetica_500000.csv` | 500.000 registros **sintéticos** de componentes do imobilizado |
| `base_sintetica_previa_5000.csv` | Prévia pequena para abrir no visualizador; 5.000 registros espaçados ao longo da base |
| `base_partes/` | 20 arquivos de 25.000 registros, juntos equivalentes à base completa; manifesto com hash de cada parte |
| `dicionario_base.md` | Dicionário, premissas e limitações da base |
| `generate_base.py` | Geração determinística da base e do gabarito de exceções |
| `analyze_base.py` | Conciliação, testes da população, amostra e indicadores |
| `split_base.py` | Geração das partes menores e da prévia para visualização |
| `build_dossier.py` | Geração dos PTs, matriz, fontes, versão editável e PDF |
| `pdf_layout.py` | Projeto gráfico do PDF: capa, guia, quadros dos PTs, anexos e fontes |
| `conciliacao_imobilizado.csv` | Conciliação por classe com a nota 14, em R$ mil |
| `amostra_PT530.csv` | Seleção reproduzível de 1.200 registros aleatórios e 50 maiores (1 sobreposição) |
| `excecoes_inseridas_gabarito.csv` | Gabarito separado das 1.551 exceções deliberadas |
| `resultados_testes.json` | Resultado dos testes e confronto com o gabarito |
| `materialidade_editavel.json` | Cálculos e premissas de materialidade |
| `analise_horizontal_PT520.csv` | Análise horizontal 2025/2024 |
| `matriz_cobertura.csv` | Norma, versão, itens e PT correspondente |
| `fontes.csv` | URLs, documento, páginas/seções, exercício e acesso |
| `manifesto_base.json` | Totais, semente e SHA-256 da base |
| `INSTRUCOES_GITHUB.md` | Passo a passo para publicar o conteúdo no GitHub |

## Fontes e conta escolhida

As demonstrações consolidadas de 2025 apresentam **imobilizado de R$ 7.111.885 mil**, maior conta individual do ativo, ante R$ 5.417.528 mil em 2024. A nota 14 discrimina terras, correção do solo, prédios, equipamentos, veículos e obras em andamento. [Demonstrações anuais completas da companhia](https://ri.slcagricola.com.br/wp-content/themes/mziq_slc-agricola_ri_redesign/assets/rad2025/uploads/Demonstracoes_Financeiras_Anuais_Completas.pdf), páginas 105 e 156-158, exercício 2025, acesso em 25/10/2026. A base sintética foi forçada a conciliar exatamente com cada subtotal divulgado. Essa conciliação **não** autentica bens ou registros reais.

A ação da emissora permanece **SLCE3**; a antiga Terra Santa citada no dossiê é controlada, hoje SLC Agrícola Centro-Oeste S.A., não uma mudança de nome/ticker da emissora. Ver `fontes.csv` para [CVM](https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp), [B3](https://www.b3.com.br/pt_br/busca/?query=SLCE3), [RI](https://ri.slcagricola.com.br/) e [CFC](https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/nbc-ta-de-auditoria-independente/).

## Reproduzir

Requer Python 3.10 ou superior; `reportlab` para regenerar o PDF e `pypdf` para validação (`python -m pip install -r requirements.txt`). Abra um terminal **dentro da pasta que contém este README** (a pasta local `outputs` ou a raiz do repositório após publicação):

```text
python generate_base.py
python analyze_base.py
python split_base.py
python audit_support.py
python build_dossier.py
python validar_entrega.py
```

O primeiro script é determinístico com semente 24120631 e regenera o CSV de 500.000 linhas, o gabarito e o manifesto. O segundo usa semente 53024120631 para a amostra, compara todas as detecções ao gabarito e interrompe se houver divergência. O terceiro comando gera a prévia e as 20 partes, com hash e totais em `base_partes/manifesto_partes.json`. O quarto gera as memórias complementares. O quinto gera o PDF com auxílio de `pdf_layout.py`, além do Markdown, `fontes.csv` e `matriz_cobertura.csv`. Os cálculos de materialidade e análise horizontal são JSON/CSV editáveis. Na primeira geração, compare o SHA-256 em `manifesto_base.json`; diferenças de codificação/versão do Python devem ser investigadas antes de tomar o hash como idêntico.

Se o visualizador não conseguir abrir o CSV integral de 74 MB, abra `base_sintetica_previa_5000.csv` ou um arquivo da pasta `base_partes/`. A prévia é **somente para navegação**, não é a amostra do PT 530. As 20 partes preservam as 500.000 linhas sem omissões; cada arquivo contém cabeçalho próprio. O CSV integral permanece como fonte canônica para todos os cálculos.

**Tamanho da base:** 74.098.222 bytes (cerca de 70,7 MiB). O GitHub aceita o envio por Git de arquivos até 100 MiB, com aviso acima de 50 MiB; o upload pelo navegador aceita no máximo 25 MiB. Por isso, siga `INSTRUCOES_GITHUB.md` e envie o CSV com `git push`. O ZIP de transporte está ignorado por `.gitignore` e não precisa integrar o repositório.

## Leitura dos resultados

Os testes de população identificaram 1.043 divergências com suporte **sintético**, 501 entradas após 31/12/2025 e 7 depreciações sintéticas de terras; todos correspondem ao gabarito. A seleção aleatória de 1.200 itens achou duas divergências de suporte. A extrapolação simples de R$ 833.333,33 é ilustração de amostragem, inadequada para conclusão sobre a SLC real. Procedimentos que exigem livros, contratos, inspeção, confirmações ou entrevistas estão expressamente marcados **PLANEJADO** no dossiê.

## Versões normativas

A matriz lista a NBC TA Estrutura Conceitual e cada NBC TA exigida de 200 a 600. Para a auditoria de 2025 e relatório de 11/03/2026, usaram-se as versões anteriores às revisões NBC TA 240 (R2) e 570 (R1), publicadas em 25/09/2026. Consulte o catálogo CFC indicado em `fontes.csv` e a versão específica antes de empregar qualquer PT em prática profissional.


## Revisão

O PDF inclui as memórias D-EC a D-600, com minutas completas, cronograma, controles, riscos, respostas, análises de estimativas e grupo. Cada memória integra o PT de mesmo número. Veja `REVISAO_CONFORMIDADE.md` para o confronto com o roteiro.

| Arquivo | Conteúdo |
|---|---|
| `suplemento_auditoria.py` | Texto estruturado das memórias e programas |
| `audit_support.py` | Gera os cálculos, programas e mapas complementares |
| `dados_CVM_SLC_2025.csv` | Extrato público da DFP, versão 1; dados reais divulgados, separados da base SYN |
| `conferencia_CVM_PT500.csv` | Seis rubricas conciliadas entre CVM e RI |
| `conciliacoes_publicas_PT520.csv` | Oito recálculos, incluindo pontes da taxonomia CVM |
| `calculos_complementares.json` | Materialidade, alternativas de base e indicadores |
| `sensibilidade_PT540.csv` | Cenários de preço/produtividade; receita potencial, não valor justo |
| `programas_auditoria.csv` / `matriz_riscos_respostas.csv` | Natureza, época, extensão, afirmações, riscos e respostas |
| `excecoes_detectadas.csv` / `mapa_distorcoes_PT450.csv` | Resultado por ID/tipo e mapa de diferenças |
| `componentes_PT600.csv` / `partes_relacionadas_PT550.csv` | Mapa público do grupo e saldos relacionados |
| `controle_circularizacao_PT505.csv` | Modelo vazio: nenhuma solicitação enviada |
| `registro_normas.json` | 27 documentos individuais CFC, versões, páginas, links, data e hashes |
| `validar_entrega.py` / `validacao_entrega.json` | Verificação técnica executável e resultado |
| `manifesto_arquivos.json` | SHA-256 dos arquivos, exceto ele próprio e ZIP |

**Escopo da maior conta:** o imobilizado é a maior rubrica individual no balanço consolidado do relatório anual do RI. Na controladora, investimentos são superiores; a escolha do consolidado foi explícita. Na DFP/CVM, o agregado `1.02.03` de R$ 9.875.307 mil também inclui direito de uso de R$ 2.763.422 mil. A base corresponde à nota 14: operação 6.781.875 + andamento 330.010 = 7.111.885 (R$ mil), sem duplicar arrendamentos. A receita operacional está em `3.01.01` (8.553.147); o agregado `3.01` (9.759.214) inclui valor justo/VRL de 1.206.067. As conciliações evidenciam essas diferenças de apresentação.

**Correção da base:** a distribuição em fazendas foi corrigida para 37 unidades fictícias; não se atribuem nomes ou registros reais da SLC. As sementes históricas 24120631 e 53024120631 foram preservadas; não são a matrícula atual. O hash anterior da base foi substituído pelo hash da versão corrigida. As 1.551 ocorrências atingem 1.550 IDs distintos (um ID tem duas). O plano de detecção da amostra foi fundamentado na revisão; não fornece limite monetário superior de erro.

Para abrir os CSVs em planilha, importe como **UTF-8, separador vírgula**. Os resultados são editáveis; para recalcular, altere as premissas no script correspondente e execute a sequência do README. O sexto comando valida unicidade, soma, partes, gabarito, amostra, conciliações, 27 PTs e ordem sumário/apresentação. A validação não substitui revisão profissional de terceiro.

Não é necessário baixar novamente as fontes para reproduzir os cálculos: o extrato CVM e os parâmetros públicos estão preservados. Fontes novas exigem revisão consciente, sem substituir silenciosamente o exercício de 2025. No Windows o PDF usa Arial; em outros sistemas há alternativa Helvetica. Paginação e hash do PDF podem variar por fontes/versões/metadados, sem mudar os dados.

Repositório **privado** de entrega: [MarcosBr1to/dossie-auditoria-slc-2025](https://github.com/MarcosBr1to/dossie-auditoria-slc-2025). O acesso exige autenticação e autorização do proprietário. A pesquisa posterior inclui ITR 1T26/2T26 até o corte de 25/10/2026, sem certificar exaustividade de todos os comunicados. Não há opinião profissional independente.
