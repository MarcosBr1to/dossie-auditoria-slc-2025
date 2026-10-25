"""Diagramação editorial do dossiê didático de auditoria SLC Agrícola 2025.

Importado por build_dossier.py. Mantém os dados e textos do dossiê, mas dá
estrutura visual distinta ao julgamento, aos procedimentos e às limitações.
"""
from __future__ import annotations

import re
from html import escape
from pathlib import Path
from caminhos import ROOT, caminho

from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate,
                               PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

INK = colors.black
GREEN = colors.black
LIME = colors.black
PALE = colors.white
WARM = colors.white
LINE = colors.black
GRAY = colors.black
WHITE = colors.white
BLUEPALE = colors.white
BEIGE = colors.white
BODY_WIDTH = 17.4 * cm

PRESENTATION = (
    "Este dossiê reúne os papéis de trabalho de um estudo de auditoria das demonstrações contábeis da SLC Agrícola S.A. relativas ao exercício encerrado em 31 de dezembro de 2025, com os comparativos de 2024. Seu objetivo é aplicar julgamento profissional, avaliação de riscos, planejamento e análise de evidências à companhia, com base na Estrutura Conceitual e nas NBC TA de 200 a 600 aplicáveis ao exercício.",
    "O exame documental abrange demonstrações anuais, notas explicativas, relatório do auditor independente e publicações da CVM, B3 e área de relações com investidores. A pesquisa foi encerrada em 25 de outubro de 2026. Os procedimentos incluem análises de saldos, materialidade e riscos, além de testes didáticos sobre 500.000 registros sintéticos de imobilizado. Cada papel explicita as fontes, os procedimentos, os resultados e as limitações correspondentes.",
    "A documentação está organizada em quatro grupos: enquadramento e responsabilidades; planejamento e resposta aos riscos; evidência e testes; estimativas, eventos e auditoria de grupos. Os anexos reúnem minutas e instrumentos de apoio. O trabalho tem finalidade acadêmica: os procedimentos dependentes de acesso interno permanecem planejados, e as simulações não representam registros reais da companhia. As conclusões se limitam às evidências obtidas e não constituem opinião profissional independente."
)

FONT_REGULAR = Path("C:/Windows/Fonts/arial.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
if "Arial" not in pdfmetrics.getRegisteredFontNames() and FONT_REGULAR.exists():
    pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

if "Arial" not in pdfmetrics.getRegisteredFontNames():
    from reportlab.pdfbase.pdfmetrics import Font
    pdfmetrics.registerFont(Font("Arial", "Helvetica", "WinAnsiEncoding"))
    pdfmetrics.registerFont(Font("Arial-Bold", "Helvetica-Bold", "WinAnsiEncoding"))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

ST = {
    "cover_kicker": ParagraphStyle("cover_kicker", fontName="Arial-Bold", fontSize=10, leading=14,
                                    textColor=GREEN, spaceAfter=8),
    "cover_title": ParagraphStyle("cover_title", fontName="Arial-Bold", fontSize=27, leading=33,
                                   textColor=INK, spaceAfter=15),
    "cover_sub": ParagraphStyle("cover_sub", fontName="Arial", fontSize=13, leading=18,
                                 textColor=GRAY, spaceAfter=10),
    "chapter": ParagraphStyle("chapter", fontName="Arial-Bold", fontSize=16, leading=20,
                               textColor=GREEN, spaceBefore=5, spaceAfter=10, keepWithNext=True),
    "section": ParagraphStyle("section", fontName="Arial-Bold", fontSize=11.4, leading=15,
                               textColor=INK, spaceBefore=13, spaceAfter=7, keepWithNext=True),
    "pttitle": ParagraphStyle("pttitle", fontName="Arial-Bold", fontSize=11.4, leading=14,
                               textColor=INK),
    "ptnorm": ParagraphStyle("ptnorm", fontName="Arial", fontSize=7.3, leading=10,
                              textColor=GRAY),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=9.2, leading=13.2,
                            textColor=INK, spaceAfter=5),
    "bodytight": ParagraphStyle("bodytight", fontName="Arial", fontSize=8.7, leading=12.2,
                                 textColor=INK),
    "small": ParagraphStyle("small", fontName="Arial", fontSize=7.2, leading=10,
                             textColor=GRAY),
    "label": ParagraphStyle("label", fontName="Arial-Bold", fontSize=7.4, leading=9.5,
                             textColor=GREEN),
    "white": ParagraphStyle("white", fontName="Arial-Bold", fontSize=9.5, leading=13,
                             textColor=INK, alignment=TA_CENTER),
    "tablehead": ParagraphStyle("tablehead", fontName="Arial-Bold", fontSize=7.7, leading=10,
                                 textColor=INK),
    "tablenum": ParagraphStyle("tablenum", fontName="Arial", fontSize=8.1, leading=11,
                                textColor=INK, alignment=TA_RIGHT),
    "toc": ParagraphStyle("toc", fontName="Arial", fontSize=9, leading=14,
                           textColor=INK, leftIndent=10, firstLineIndent=-10, spaceBefore=5),
}

def P(s, style="body", *, markup=False):
    return Paragraph(s if markup else escape(str(s)), ST[style])

def box(content, bg=PALE, pad=9, border=LINE):
    t = Table([[content]], colWidths=[BODY_WIDTH], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 1.0, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return t

def datatable(headers, rows, widths, *, align_right=(), font="bodytight"):
    cells = [[P(x, "tablehead") for x in headers]]
    for row in rows:
        cells.append([P(x, "tablenum" if i in align_right else font) for i, x in enumerate(row)])
    t = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.4, GREEN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(cmds))
    return t

def labeltext(label, text):
    return [P(label.upper(), "label"), P(text, "bodytight")]

class ChapterHeading(Paragraph):
    def __init__(self, title, key):
        super().__init__(escape(title), ST["chapter"])
        self.toc_title = title
        self.toc_key = key

class DossierDoc(BaseDocTemplate):
    def __init__(self, path):
        super().__init__(str(path), pagesize=A4, leftMargin=1.8*cm, rightMargin=1.8*cm,
                         topMargin=1.75*cm, bottomMargin=1.7*cm,
                         title="Dossiê de auditoria didático — SLC Agrícola 2025",
                         author="Marcos Aurélio de Brito Cunha — Matrícula 241021631")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="normal")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=frame, onPage=self.cover_page),
            PageTemplate(id="body", frames=frame, onPage=self.body_page),
        ])

    def cover_page(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        center = (3*cm + (w-2*cm))/2
        canvas.setFillColor(colors.black)
        canvas.setFont("Arial-Bold", 12)
        canvas.drawCentredString(center, h-3*cm, "UNIVERSIDADE DE BRASÍLIA")
        canvas.setFont("Arial", 12)
        canvas.drawCentredString(center, h-5.2*cm, "MARCOS AURÉLIO DE BRITO CUNHA")
        canvas.drawCentredString(center, h-5.9*cm, "Matrícula: 241021631")
        canvas.setFont("Arial-Bold", 14)
        canvas.drawCentredString(center, h/2+1.1*cm, "DOSSIÊ DE AUDITORIA")
        canvas.drawCentredString(center, h/2+0.35*cm, "SLC AGRÍCOLA S.A.")
        canvas.setFont("Arial", 12)
        canvas.drawCentredString(center, h/2-0.55*cm, "Demonstrações contábeis do exercício de 2025")
        canvas.drawCentredString(center, h/2-2.5*cm, "Professor: Lucas Oliveira Gomes Ferreira")
        canvas.drawCentredString(center, 2.5*cm, "2026")
        canvas.restoreState()

    def body_page(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFont("Arial", 9)
        canvas.setFillColor(colors.black)
        canvas.drawRightString(w-2*cm, 1.0*cm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, ChapterHeading):
            self.canv.bookmarkPage(flowable.toc_key)
            self.canv.addOutlineEntry(flowable.toc_title, flowable.toc_key, level=0, closed=False)
            self.notify("TOCEntry", (0, flowable.toc_title, self.page, flowable.toc_key))

def procedure_rows(text):
    pattern = r"\[(PÚBLICA|PLANEJADO|SIMULADO)\]\s*(.*?)(?=\s*\[(?:PÚBLICA|PLANEJADO|SIMULADO)\]|$)"
    hits = re.findall(pattern, text, flags=re.DOTALL)
    if not hits:
        return [("DESCRIÇÃO", text)]
    return [(tag, value.strip()) for tag, value in hits]

def procedure_table(text):
    rows = []
    for status, value in procedure_rows(text):
        label = {"PÚBLICA": "EXECUTADO<br/>FONTE PÚBLICA",
                 "SIMULADO": "EXECUTADO<br/>SINTÉTICO",
                 "PLANEJADO": "PLANEJADO<br/>SEM ACESSO"}.get(status, status)
        rows.append([P(label, "label", markup=True), P(value, "bodytight")])
    t = Table(rows, colWidths=[2.55*cm, BODY_WIDTH-2.55*cm], hAlign="LEFT")
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
            ("BACKGROUND", (0, 0), (0, -1), PALE)]
    t.setStyle(TableStyle(cmds))
    return t

def pt_card(code, pt, version, date, extra=None):
    title, items, objective, risks, population, procedures, evidence, result = pt
    header = Table([
        [P(f"PT {code}", "white"), [P(title, "pttitle"), P(f"{version}  ·  {items}", "ptnorm")]],
    ], colWidths=[2.0*cm, BODY_WIDTH-2.0*cm], hAlign="LEFT")
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), WHITE),
        ("LINEBELOW", (0, 0), (-1, -1), 0.7, INK),
        ("BACKGROUND", (1, 0), (1, 0), PALE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    two = Table([[
        labeltext("Afirmações e risco", risks),
        labeltext("População e seleção", population),
    ]], colWidths=[BODY_WIDTH/2, BODY_WIDTH/2], hAlign="LEFT")
    two.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBEFORE", (1, 0), (1, 0), 0.55, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 12),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    content = [header, Spacer(1, 9), P("OBJETO / OBJETIVO", "label"), P(objective),
               Spacer(1, 3), two, Spacer(1, 8), P("PROCEDIMENTOS E ESTÁGIO", "label"),
               procedure_table(procedures), Spacer(1, 8)]
    if extra is not None:
        content += [extra, Spacer(1, 8)]
    content += [box([P("RESULTADOS, CONCLUSÃO E LIMITAÇÕES", "label"), P(result, "bodytight")], bg=WARM),
                Spacer(1, 7),
                P(f"<b>Evidências e referências</b>  {escape(evidence)}", "small", markup=True),
                P(f"<b>Preparação</b>  Marcos Aurélio de Brito Cunha · Matrícula 241021631 · {date}", "small", markup=True),
                P("<b>Revisão</b>  revisor ______  data ______  observações ____________________", "small", markup=True),
                Spacer(1, 17)]
    return [KeepTogether(content)]

def chapter_intro(title, codes):
    return [ChapterHeading(title, "chapter-"+str(codes[0])),
            P("Papéis de trabalho: " + " · ".join("PT "+c for c in codes), "small"),
            Spacer(1, 9)]

def cover_story(date):
    # Capa acadêmica: instituição, autor, matrícula, título, professor e ano.
    return [Spacer(1, cm), NextPageTemplate("body"), PageBreak()]

def executive_pages(results, sources):
    toc = TableOfContents()
    toc.levelStyles = [ST["toc"]]
    story = [P("Sumário", "chapter"), toc, PageBreak(), ChapterHeading("Apresentação", "guide"),
             *[P(paragraph) for paragraph in PRESENTATION],
             P("Organização documental: NBC TA 230, itens 8, A3 e A11 (F11); apresentação de objetivo, escopo e método adaptada do manual da CGU, seção 6.5.2 (F12).", "small"),
             Spacer(1, 7),
             P("Classificação dos procedimentos", "section")]
    status = [
        ("REALIZADO COM EVIDÊNCIA PÚBLICA", "Leitura e recálculo de documentos da CVM, B3, RI e relatório do auditor."),
        ("PLANEJADO POR FALTA DE ACESSO", "Procedimento definido, sem execução ou resultado atribuído à SLC."),
        ("SIMULADO PARA FINS DIDÁTICOS", "Teste executado apenas sobre dados artificiais, identificado pelo prefixo SYN."),
    ]
    rows = [[P(a, "label"), P(b, "bodytight")] for a,b in status]
    tt = Table(rows, colWidths=[5.0*cm, BODY_WIDTH-5.0*cm], hAlign="LEFT")
    tt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(0,-1),PALE),
                            ("LINEBELOW",(0,0),(-1,-1),0.4,LINE),("LEFTPADDING",(0,0),(-1,-1),8),
                            ("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),8),
                            ("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    story += [tt, Spacer(1, 10),
              P("A conciliação da base sintética com o saldo publicado é uma premissa de geração; não comprova existência, direitos ou valoração dos bens da companhia.", "small"),
              PageBreak(), ChapterHeading("Visão de planejamento", "planning-view"),
              P("Os números abaixo são saldos consolidados publicados, em R$ mil. O imobilizado é a maior conta individual do ativo. A expansão de terras e a aquisição da Sierentz orientam o trabalho sobre existência, direitos, mensuração e consolidação."),
              Spacer(1, 8)]
    financial = [
        ("Ativo total", "21.341.432", "17.574.342", "+21,44%"),
        ("Imobilizado", "7.111.885", "5.417.528", "+31,28%"),
        ("Estoques", "3.722.611", "3.780.562", "−1,53%"),
        ("Ativos biológicos", "2.350.421", "1.785.392", "+31,65%"),
        ("Caixa e equivalentes", "2.647.586", "1.979.575", "+33,75%"),
        ("Receita líquida", "8.553.147", "6.915.764", "+23,68%"),
    ]
    story += [datatable(["CONTA / RUBRICA", "2025", "2024", "VARIAÇÃO"], financial,
                        [7.1*cm, 3.5*cm, 3.5*cm, 3.3*cm], align_right=(1,2,3)),
              Spacer(1, 11),
              P("Juízos que definem a resposta", "section"),
              box([P("01  MAIOR EXPOSIÇÃO PATRIMONIAL", "label"),
                   P("Imobilizado de R$ 7,11 bilhões (33,3% do ativo). A nota 14 separa terras, correção do solo, benfeitorias, equipamentos e obras. O cadastro de 500.000 linhas modela essas classes; seus registros são inteiramente fictícios.")], bg=PALE),
              Spacer(1, 7),
              box([P("02  ESTIMATIVA COM JULGAMENTO ELEVADO", "label"),
                   P("Ativos biológicos de R$ 2,35 bilhões; preço, produtividade e custos futuros afetam o valor justo. O assunto aparece no relatório do auditor EY e recebe análise de sensibilidade no PT 540.")], bg=PALE),
              Spacer(1, 7),
              box([P("03  FRONTEIRA DE CONCLUSÃO", "label"),
                   P("DFs e notas permitem identificação de riscos e recálculos. Sem registros internos, contratos, laudos e confirmações, não há base para concluir sobre todas as afirmações ou emitir opinião independente.")], bg=WARM),
              P("Fontes principais: F01 (balanço, DRE, notas 8 e 14), F05 (administração) e F09 (espelho indexado). Exercícios 2025 e 2024; acesso em 25/10/2026.", "small")]
    return story

def extra_for(code, results):
    if code == "320":
        rows=[("Receita líquida 2025", "8.553.147,00", "Base divulgada"),
              ("Materialidade global", "42.765,74", "0,5% da receita"),
              ("Para execução", "29.936,01", "70% da global"),
              ("Limiar de acúmulo", "2.138,29", "5% da global"),
              ("Específica — biológicos", "23.504,21", "1% do saldo")]
        return datatable(["CÁLCULO", "R$ MIL", "CRITÉRIO DIDÁTICO"],rows,
                         [6.6*cm,3.1*cm,7.7*cm],align_right=(1,))
    if code == "520":
        rows=[(x["conta"].replace("_"," ").capitalize(),
               f'{x["2025_R_mil"]:,}'.replace(",","."),
               f'{x["2024_R_mil"]:,}'.replace(",","."),
               ("+" if x["variacao_percentual"]>0 else "")+f'{x["variacao_percentual"]:.2f}%'.replace(".",","))
              for x in results["analiticos"]]
        return datatable(["RUBRICA", "2025", "2024", "Δ %"],rows,
                         [7.0*cm,3.5*cm,3.5*cm,3.4*cm],align_right=(1,2,3))
    if code == "530":
        rows=[("População", "500.000", "Cadastro SYN"),
              ("Amostra aleatória", "1.200", "Sem reposição"),
              ("Seleção dirigida", "50", "Maiores valores"),
              ("Divergências na amostra", "2", "Suporte sintético"),
              ("Detecção na varredura", "1.551/1.551", "Gabarito artificial")]
        return datatable(["MEDIDA", "RESULTADO", "BASE"],rows,
                         [7.0*cm,3.4*cm,7.0*cm],align_right=(1,))
    if code == "540":
        rows=[("Cenário −5%", "2.232.899,95", "−117.521,05"),
              ("Saldo divulgado", "2.350.421,00", "—"),
              ("Cenário +5%", "2.467.942,05", "+117.521,05")]
        return datatable(["CENÁRIO MECÂNICO", "R$ MIL", "EFEITO R$ MIL"],rows,
                         [6.2*cm,5.5*cm,5.7*cm],align_right=(1,2))
    return None

def appendix_pages(date):
    story=[PageBreak(),ChapterHeading("Instrumentos e anexos", "appendices"),
           P("As minutas abaixo são instrumentos de planejamento. Campos de destinatário, assinatura, envio e resposta permanecem sem preenchimento porque nenhum procedimento interno ou comunicação externa foi realizado."),
           Spacer(1,8)]
    def block(title, purpose, text):
        return KeepTogether([P(title,"section"),
                             box([P(purpose.upper(),"label"), P(text,"bodytight")],bg=PALE),Spacer(1,8)])
    story += [block("A1  Carta de contratação · PT 210", "Minuta não enviada",
                    "Destinatária: administração da SLC Agrícola S.A. Objeto proposto: demonstrações individuais e consolidadas de 31/12/2025. Referencial: práticas brasileiras e IFRS declaradas. A administração responderia pela elaboração, pelos controles e pelo acesso irrestrito. A equipe buscaria segurança razoável conforme NBC TA e reportaria opinião, base, principais assuntos e responsabilidades. Aceite, honorários e cronograma dependem de contratação real."),
              block("A2  Comunicação à governança · PT 260", "Minuta não enviada",
                    "Destinatário proposto: Comitê de Auditoria. Alcance: demonstrações de 2025 e componentes relevantes. Riscos prioritários: biológicos, receitas, hedge, Sierentz e imobilizado. Materialidade didática global: R$ 42.765,74 mil. Solicitações futuras: livros, contratos, laudos, sistemas e projeções. Independência da equipe e dificuldades devem ser declaradas somente após verificação efetiva."),
              P("A3  Hipóteses de controle extraídas da simulação · PT 265", "section")]
    controls=[
        ("501 datas após corte", "Bloqueio de entrada por período", "Erro de corte", "Revisar parametrização e aprovações"),
        ("7 terras depreciadas", "Política de classe patrimonial", "Despesa indevida", "Impedir depreciação de terra"),
        ("1.043 divergências", "Conciliação documento × razão", "Valoração", "Trilha de conciliação mensal"),
    ]
    story += [datatable(["CONDIÇÃO SYN", "CRITÉRIO / CAUSA HIPOTÉTICA", "EFEITO", "RECOMENDAÇÃO"],
                        controls,[3.5*cm,5.1*cm,3.0*cm,5.8*cm]),
              P("Estas condições foram inseridas no cadastro sintético; não são deficiências constatadas na companhia.","small"),
              P("A4  Programas por ciclo · PT 300 / 330 / 501", "section")]
    programs=[
        ("Receitas", "Contratos, transferência de controle, corte de embarques, devoluções e lançamentos manuais."),
        ("Disponibilidades", "Conciliação de bancos, restrições, confirmações e movimentação pós-fechamento."),
        ("Estoques", "Contagem, corte, custeio, qualidade e valor realizável líquido."),
        ("Imobilizado", "Adições, títulos, existência, baixas, depreciação e impairment."),
        ("Passivos", "Completude pós-fechamento, contratos, juros, covenants e classificação."),
        ("Estimativas", "Preço, produtividade, custos futuros e retrospectiva dos modelos de valor justo."),
    ]
    story += [datatable(["CICLO", "PROGRAMA PLANEJADO"],programs,[3.3*cm,14.1*cm]),
              P("Os programas internos não foram executados; os procedimentos realizados aparecem nos PTs e arquivos analíticos.","small"),
              P("A5  Risco e resposta · PT 315 / 330", "section")]
    risks=[
        ("R1", "Biológicos — valor", "Modelo, preço, produtividade e custo", "PT 540"),
        ("R2", "Receita — corte", "Contratos e embarques; fraude presumida", "PT 240"),
        ("R3", "Hedge — valor", "Reprecificação e eficácia", "PT 330"),
        ("R4", "Sierentz — aquisição", "Contrato e alocação de preço", "PT 600"),
        ("R5", "Imobilizado — direitos", "Títulos, inventário e baixas", "PT 530"),
        ("R6", "Dívida — completude", "Confirmações e covenants", "PT 570"),
    ]
    story += [datatable(["ID", "AFIRMAÇÃO EM RISCO", "RESPOSTA INTERNA PLANEJADA", "PT"],risks,
                        [1.1*cm,4.7*cm,9.7*cm,1.9*cm]),
              P("A6  Mapa de exceções inseridas · PT 450", "section")]
    errors=[
        ("Suporte sintético", "1.043", "R$ 1.118.295,15 de diferença no campo de suporte"),
        ("Entrada após 31/12", "501", "Efeito contábil não inferido"),
        ("Depreciação de terra", "7", "Indício de política; sem ajuste real"),
    ]
    story += [datatable(["EXCEÇÃO ARTIFICIAL", "N", "EFEITO / LIMITE"],errors,
                        [5.4*cm,1.8*cm,10.2*cm],align_right=(1,)),
              P("A7  Confirmações externas · PT 505", "section"),
              box([P("MODELO BANCO", "label"),P("Solicita confirmação direta ao auditor de depósitos, aplicações, empréstimos, garantias e restrições em 31/12/2025. Controle de emissão, resposta, diferenças e procedimentos alternativos: em branco; nenhuma solicitação enviada.")],bg=PALE),
              Spacer(1,6),
              box([P("MODELO CLIENTE", "label"),P("Solicita confirmação do saldo e títulos em aberto em 31/12/2025, com resposta direta ao auditor. Segunda solicitação ou evidência alternativa só se houver trabalho real.")],bg=PALE),
              P("A8  Sensibilidade dos biológicos · PT 540", "section"),
              datatable(["CENÁRIO DIDÁTICO", "VALOR R$ MIL", "EFEITO R$ MIL"],
                        [("−5%", "2.232.899,95", "−117.521,05"),
                         ("Saldo publicado", "2.350.421,00", "—"),
                         ("+5%", "2.467.942,05", "+117.521,05")],
                        [6.0*cm,5.7*cm,5.7*cm],align_right=(1,2)),
              P("Cenário linear mecânico; não reproduz o modelo de valor justo da administração.","small"),
              block("A9  Representações formais · PT 580", "Minuta não assinada",
                    "A administração confirmaria sua responsabilidade pelas demonstrações e pelos controles; completude dos registros; divulgação de fraude, litígios, partes relacionadas, estimativas, eventos subsequentes e planos de continuidade. A carta dependeria de validação e assinatura dos responsáveis na data do relatório. Não substitui outras evidências.")]
    return story

def final_pages(sources, date):
    story=[PageBreak(),ChapterHeading("Conclusão e fontes", "closing"),
           box([P("CONCLUSÃO INTEGRADA", "label"),
                P("A leitura das demonstrações, notas, relatório EY, publicações de RI/CVM/B3 e normas do CFC sustenta riscos em ativos biológicos, receita, hedge, aquisição da Sierentz, imobilizado e dívida. Foram executados recálculos públicos e testes em 500.000 registros integralmente sintéticos. A soma da base é idêntica ao saldo divulgado por construção; as 1.551 exceções inseridas foram detectadas. Sem razão contábil, contratos, laudos, inspeções, confirmações e acesso a sistemas, a evidência é insuficiente para uma opinião própria sobre as demonstrações da SLC Agrícola.")],bg=WARM,pad=12),
           Spacer(1,12),
           P("Limites e rastreabilidade", "section"),
           P("Os papéis estão identificados por PT; documentos públicos por F; dados artificiais por SYN. Cada PT registra norma, afirmação, seleção, procedimento, evidência, resultado, limitação, preparador e campo de revisão não preenchido. A lista completa de URLs, páginas, exercícios e data de acesso também está em fontes.csv."),
           P("Registro das fontes públicas", "section"),
           P(f"Data de acesso de todas as fontes: {date}. F11 e F12 fundamentam a organização documental e a apresentação do estudo.", "small")]
    for sid,emissor,doc,url,page,year in sources:
        txt=f"<b>{escape(sid)} · {escape(emissor)}</b>  {escape(doc)}<br/>{escape(year)} · {escape(page)}<br/><link href='{escape(url,quote=True)}' color='#000000'>{escape(url)}</link>"
        story += [box(P(txt,"small",markup=True),bg=WHITE,pad=0),Spacer(1,0.3)]
    return story

def build_pdf(pt, order, versions, sources, out, date, results):
    out = Path(out)
    story = cover_story(date)
    story += executive_pages(results, sources)
    groups = [
        ("01  Enquadramento e responsabilidades", ["EC","200","210","220","230","240","250","260","265"]),
        ("02  Planejamento e resposta ao risco", ["300","315","320","330","402"]),
        ("03  Evidência, testes e análise", ["450","500","501","505","510","520","530"]),
        ("04  Estimativas, eventos e grupo", ["540","550","560","570","580","600"]),
    ]
    seen=[]
    for title,codes in groups:
        story += [PageBreak()] + chapter_intro(title,codes)
        for code in codes:
            story.extend(pt_card(code,pt[code],versions[code],date,extra_for(code,results)))
            seen.append(code)
    assert seen==order
    from suplemento_auditoria import support_story
    story += support_story(P, datatable, ChapterHeading, PageBreak, Spacer, cm, out)
    story += final_pages(sources,date)
    DossierDoc(caminho("dossie_auditoria_SLC_2025.pdf", out)).multiBuild(story)
