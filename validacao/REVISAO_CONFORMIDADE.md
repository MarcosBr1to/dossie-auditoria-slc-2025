# Revisão de conformidade — versão 2.0

Preparador: Marcos Aurélio de Brito Cunha | matrícula 241021631 | 25/10/2026.  
Natureza: revisão de consistência do material acadêmico pelo preparador.  
Revisão por terceiro: revisor ______; data ______; observações ______.

## Correções

- Sumário antes da apresentação; identificação solicitada, preto e branco, numeração inferior direita e sem cabeçalho repetido.
- Corrigida a fórmula das fazendas sintéticas; regenerados base, partes, prévia e hashes.
- Corrigida a variação do caixa para 33,75%, as páginas das fontes e as referências cruzadas.
- Compatibilizada a apresentação CVM/RI de imobilizado e receita. Escopo consolidado explicitado, distinguindo a controladora.
- Fundamentado o tamanho da amostra e limitado o alcance da projeção. Exportadas detecções por ID/tipo e mapa de diferenças; 1.551 ocorrências em 1.550 IDs.
- Acrescentadas memórias D-EC a D-600, minutas, programas, cronograma, matriz de riscos, cálculos, sensibilidade, grupo e relacionadas.
- Ampliada pesquisa de eventos com ITR 2T26. Separada dívida contábil de medida gerencial e de cálculo contratual de covenant.
- Normas individualizadas por versão, URL, itens, páginas, exercício, acesso e hash.

## Confronto com o roteiro

| Requisito | Evidência / situação |
|---|---|
| Companhia, nome e ticker | SLC Agrícola S.A./SLCE3; distinção de Centro-Oeste; PT 315/D-EC |
| DC anuais 2025 e comparativos | F01/F02; balanço, DRE, DFC, notas e relatório EY de 11/03/26 |
| CVM, B3, RI e fontes rastreáveis | `fontes.csv`; 14 fontes principais e registro das normas |
| EC e todas as NBC TA do roteiro | 27 linhas de `matriz_cobertura.csv`; versões e itens no PDF |
| Estrutura de cada PT | Código/título, norma/itens, objetivo/objeto, afirmações/riscos, população/seleção, procedimento, evidência, resultado/limite, preparador/data e revisão em branco |
| Classificação dos procedimentos | Evidência pública, planejado por falta de acesso ou simulado para fins didáticos |
| 500.000 registros analíticos | IDs/componentes/documentos únicos, nove classes e 37 fazendas fictícias; granularidade explicada |
| Conta e materialidade | Consolidado do RI/nota 14; ponte ao agregado CVM e diferença da controladora explicitadas |
| Método e dicionário | Gerador, `dicionario_base.md` e manifesto |
| Conciliação | Nove classes, diferença zero, por construção e sem autenticar bens |
| Amostra, testes, gabarito e resultados | PT 530/D-530; AAS 1.200 e 50 maiores; arquivos por ID/tipo e mapa PT 450 |
| Materialidade e analíticos | Cálculos, alternativas de base, expectativas e limites em JSON/CSV/scripts |
| Seis ciclos obrigatórios | 12 programas com natureza/época/extensão/classificação no CSV e PDF |
| Cartas e comunicações | D-210/260/505/580; minutas não enviadas/assinadas; controle vazio |
| Fraude, controles e respostas | D-240/265/315/330; hipóteses separadas de fatos e risco de burla |
| Saldos iniciais, litígios e segmentos | D-510/501; recálculos públicos e procedimentos internos planejados |
| Estimativas e sensibilidade | D-540; método, dados, incerteza e cenários de preço/produtividade, sem representar valor justo |
| Relacionadas, continuidade e grupo | D-550/570/600 e mapas; materialidade hipotética dos componentes e limitações |
| Eventos subsequentes | D-560; corte 25/10/26, ITR 1T26/2T26, distinção de condições existentes na data-base |
| PDF, editável e reprodução | PDF/Markdown, scripts, requisitos, README e validação |
| GitHub | Repositório privado MarcosBr1to/dossie-auditoria-slc-2025; arquivos e histórico de versões no Git |

## Limites

Não houve acesso a livros, sistemas, modelos completos, contratos, títulos, inventários físicos, respostas de bancos/advogados, entrevistas ou papéis do antecessor. Esses procedimentos estão planejados conforme o comando acadêmico. Nenhum tópico foi dispensado apenas com “não se aplica”. Na NBC TA 402, a aplicabilidade depende da relevância dos serviços ao sistema contábil; nenhum relatório de prestador foi obtido.

Materialidade, componentes e amostra são decisões didáticas. A fundamentação da detecção por atributos foi explicitada nesta revisão, preservando a amostra original, sem alegar plano anterior fictício. A varredura compara erros inseridos às regras programadas e não cobre todo erro possível. A pesquisa de eventos não certifica completude de publicações. Não foi emitida opinião independente.

## Verificação técnica

`validar_entrega.py` verifica as 500.000 linhas, unicidade, soma, hashes, igualdade das 20 partes ao original, 5.000 linhas de prévia, amostra de 1.249 IDs, 1.551 detecções, oito conciliações públicas, seis rubricas CVM/RI, 27 PTs/normas e ordem sumário/apresentação. Resultado em `validacao_entrega.json`. A inspeção visual complementa a verificação automática; nenhuma delas é revisão de terceiro.

Reprodução isolada executada em pasta separada: seis scripts concluídos e 14 arquivos centrais idênticos, incluindo base, amostra, gabarito, resultados e Markdown. Os localizadores normativos finais também foram reproduzidos e conferidos.
