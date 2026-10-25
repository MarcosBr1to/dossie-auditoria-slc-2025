# Acessar e atualizar o repositório

Repositório privado: [MarcosBr1to/dossie-auditoria-slc-2025](https://github.com/MarcosBr1to/dossie-auditoria-slc-2025).

## Navegar e baixar

Comece pelo [README principal](../README.md). O documento final fica em [dossie/](../dossie/); os cálculos e programas em [papeis_trabalho/](../papeis_trabalho/); as bases em [dados/](../dados/).

Para baixar tudo, use **Code → Download ZIP** no GitHub. Para manter uma cópia com histórico, use Git:

```powershell
git clone https://github.com/MarcosBr1to/dossie-auditoria-slc-2025.git
cd dossie-auditoria-slc-2025
```

O acesso ao repositório privado exige uma conta autorizada. A autenticação ocorre pelo mecanismo do Git/GitHub; não inclua credenciais nos arquivos.

## Reproduzir

Abra um terminal na raiz do clone, onde estão `README.md` e `requirements.txt`. Execute:

```powershell
python -m pip install -r requirements.txt
python codigo/generate_base.py
python codigo/analyze_base.py
python codigo/split_base.py
python codigo/audit_support.py
python codigo/build_dossier.py
python codigo/validar_entrega.py
```

Cada script grava os arquivos nas pastas correspondentes. Os nomes e os caminhos são centralizados em [codigo/caminhos.py](../codigo/caminhos.py). A validação atualiza o manifesto de integridade. A base integral é sintética e contém 500.000 registros; a prévia serve apenas para navegação, e as 20 partes juntas equivalem à base completa.

## Enviar alterações

Na raiz do clone, confira as alterações, valide e envie:

```powershell
git status --short
python codigo/validar_entrega.py
git add .
git diff --cached --stat
git commit -m "Atualiza dossiê e arquivos de apoio"
git push origin main
```

Se o Git solicitar identidade, configure `user.name` e `user.email` apenas nesse repositório com seus próprios dados. Depois do envio, confira o commit e as pastas no GitHub.

O CSV integral tem cerca de 70,7 MiB: use Git para enviá-lo. Consulte os [limites oficiais de arquivos](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). O ZIP local de transporte não integra o histórico; ele reúne os arquivos já organizados e não substitui a estrutura de pastas publicada.
