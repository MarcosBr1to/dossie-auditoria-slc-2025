# Dicionário da base sintética de imobilizado

**Aviso:** nenhuma linha representa bem, transação ou documento real da SLC Agrícola. São registros analíticos artificiais de componentes patrimoniais, desenhados para fins de teste.

## Modelo e premissas

O maior saldo individual do ativo consolidado em 31/12/2025 é o imobilizado, R$ 7.111.885 mil (nota 14). A base contém 500.000 **componentes individuais com IDs únicos**, distribuídos em nove classes de imobilizado nas proporções simuladas abaixo. Componentes de correção do solo correspondem a unidades distintas de aplicação/área; componentes de equipamentos podem representar módulos ou peças capitalizadas. A granularidade é construção didática e não pressupõe que a companhia mantenha 500.000 bens cadastrados.

| Classe | Registros | Saldo publicado e gerado (R$ mil) |
|---|---:|---:|
| Terras de cultura | 1.000 | 3.315.500 |
| Correção e desenvolvimento do solo | 350.000 | 1.052.113 |
| Prédios e benfeitorias | 10.000 | 797.295 |
| Equipamentos agrícolas e instalações industriais | 100.000 | 1.409.647 |
| Veículos | 5.000 | 123.837 |
| Móveis e utensílios | 10.000 | 29.100 |
| Equipamentos e instalações de escritório | 10.000 | 35.871 |
| Outros | 10.000 | 18.512 |
| Imobilizado em andamento | 4.000 | 330.010 |
| **Total** | **500.000** | **7.111.885** |

Valores são alocados por pesos pseudoaleatórios positivos em centavos, com o resíduo atribuído ao último item de cada classe para igualdade exata. `custo_bruto - depreciacao_acumulada = valor_contabil` para cada linha. Custos e depreciações por item não são saldos publicados; são atributos sintéticos. Datas, fazendas e documentos são inteiramente inventados. Semente: 24120631.

## Colunas

| Variável | Tipo/unidade | Significado |
|---|---|---|
| `registro_id` | texto | Identificador único `SYN-IMOB-######` |
| `classe` | categoria | Rubrica de imobilizado alinhada à nota 14 |
| `fazenda_sintetica` | texto | Unidade operacional fictícia; não equivale a fazenda real |
| `componente` | texto | Identificador único de componente patrimonial fictício |
| `data_entrada` | AAAA-MM-DD | Data de capitalização fictícia, com algumas exceções após corte |
| `custo_bruto_centavos` | inteiro/R$ centavos | Custo bruto fictício |
| `depreciacao_acumulada_centavos` | inteiro/R$ centavos | Depreciação fictícia; sete terras têm depreciação indevida deliberada |
| `valor_contabil_centavos` | inteiro/R$ centavos | Saldo líquido fictício; soma igual ao saldo público por construção |
| `valor_suporte_sintetico_centavos` | inteiro/R$ centavos | Valor fictício de documento simulado, usado em teste de divergência |
| `documento_sintetico_id` | texto | Referência fictícia; não corresponde a nota fiscal ou escritura real |
| `status_sintetico` | texto | Estado fictício do registro |

Conversão: R$ mil = centavos / 100.000. O campo de suporte não faz parte da soma do razão sintético. Seu excesso agregado de R$ 1.118.295,15 representa divergências artificiais para testar detecção, não distorção da companhia. O gabarito de exceções fica em arquivo separado para comparação independente dos testes. A varredura automatizada encontrou as 1.551 exceções inseridas, sem falsos positivos ou falsos negativos nas regras codificadas.

**Fonte:** demonstrações anuais 2025, balanço e nota 14, [RI SLC Agrícola](https://ri.slcagricola.com.br/wp-content/themes/mziq_slc-agricola_ri_redesign/assets/rad2025/uploads/Demonstracoes_Financeiras_Anuais_Completas.pdf), páginas 105 e 156-158; acesso em 25/10/2026.


## Revisão da geração

Os registros são distribuídos por 37 fazendas fictícias mediante `(id - 1) % 37 + 1`; isso corrige a expressão anterior que resultava sempre na primeira unidade. Cada componente, documento e ID é único; valores podem repetir sem repetição do registro. O modelo não foi obtido dos controles da companhia e sua granularidade não estima o número real de bens. Datas abrangem 2012–2025, exceto 501 exceções intencionais em 2026. Campos de custo/depreciação não reproduzem o histórico ou vidas úteis reais. O gabarito permanece separado, sem alegação de cegamento ou independência do preparador. Há 1.551 ocorrências em 1.550 IDs distintos.

Escopo: consolidado da nota 14. O agregado CVM de imobilizado inclui direito de uso, separado no balanço do RI e excluído desta base; ver `conferencia_CVM_PT500.csv` e D-EC. Na controladora, investimentos são a maior conta.
