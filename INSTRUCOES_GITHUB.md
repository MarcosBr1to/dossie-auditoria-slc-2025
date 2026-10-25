# Como publicar este dossiê no GitHub

Destino autorizado: **repositório privado** `dossie-auditoria-slc-2025`. Estas instruções permitem publicar ou atualizar o material. A existência dos arquivos locais não comprova publicação; confirme o resultado remotamente. O conteúdo da pasta que contém este arquivo é o conteúdo do futuro repositório. O ZIP `repositorio_SLC_2025_pronto.zip` serve apenas para transporte; não o envie como substituto dos arquivos internos.

## 1. Confira o material local

Na pasta `outputs`, confirme que há `README.md`, `dossie_auditoria_SLC_2025.pdf`, `base_imobilizado_sintetica_500000.csv`, os scripts `.py`, `requirements.txt` e as memórias complementares, a matriz, as fontes, a prévia e `base_partes/`. A base possui **500.000 registros sintéticos**, 74.098.222 bytes e SHA-256 registrado em `manifesto_base.json`. As 20 partes menores permitem visualizar toda a base por intervalos; a prévia de 5.000 linhas serve para inspeção rápida.

O README contém a matrícula **241021631**. Se escolher repositório público, esse identificador e todos os arquivos ficarão visíveis publicamente.

## 2. Crie um repositório vazio

1. Entre em [github.com/new](https://github.com/new).
2. Sugestão de nome: `dossie-auditoria-slc-2025`.
3. Escolha **Private**, conforme a preferência informada.
4. **Não** marque as opções para criar README, `.gitignore` ou licença: esses arquivos já estão na pasta local.
5. Clique em **Create repository** e copie o URL HTTPS mostrado na página, por exemplo `https://github.com/SEU_USUARIO/dossie-auditoria-slc-2025.git`.

## 3. Envie com Git, pelo PowerShell

Abra PowerShell **dentro da pasta que contém este arquivo**. Se estiver em outro local, use `Set-Location -LiteralPath 'CAMINHO_COMPLETO_DA_PASTA_OUTPUTS'` e substitua o caminho pelo caminho local real. Execute uma linha por vez:

```powershell
git --version
git init -b main
git status --short
git add .
git status --short
git commit -m "Dossiê didático SLC Agrícola 2025 - matrícula 241021631"
git remote add origin https://github.com/SEU_USUARIO/dossie-auditoria-slc-2025.git
git remote -v
git push -u origin main
```

Substitua `SEU_USUARIO` pelo seu usuário ou organização e, se escolheu outro nome, substitua também o nome do repositório. O arquivo ZIP não deverá aparecer em `git status --short`, pois `.gitignore` o exclui. O CSV de 74 MB **deverá** aparecer; o Git avisará que passa de 50 MiB, mas o limite de bloqueio do GitHub para Git comum é 100 MiB. Caso `git commit` peça identidade, configure **apenas este repositório** e repita o commit:

```powershell
git config user.name "SEU NOME"
git config user.email "SEU_EMAIL_DO_GITHUB"
git commit -m "Dossiê didático SLC Agrícola 2025 - matrícula 241021631"
```

Na primeira conexão HTTPS, o Git Credential Manager ou outro método configurado pode abrir o navegador para autenticação. **Não coloque senha ou token no URL remoto nem no README.** Se `origin` já existir, confira `git remote -v` antes de alterar qualquer endereço; não rode `git remote add` de novo.

## 4. Verifique a publicação

Abra a página do repositório. Confirme que o README aparece, que o PDF, os scripts, `matriz_cobertura.csv`, `fontes.csv`, `base_imobilizado_sintetica_500000.csv`, `base_sintetica_previa_5000.csv` e a pasta `base_partes/` estão listados, e que `repositorio_SLC_2025_pronto.zip` ficou fora do repositório. Copie o URL da página para sua entrega acadêmica. Para verificar a reprodução após clonar:

```powershell
python generate_base.py
python analyze_base.py
python split_base.py
python audit_support.py
python build_dossier.py
python validar_entrega.py
```

Rode os comandos na raiz do clone. Instale as dependências com `python -m pip install -r requirements.txt`. O quinto comando gera o PDF; o sexto verifica a entrega. O segundo compara as 1.551 detecções com o gabarito e falha se houver diferença. A base é gerada de forma determinística e deve voltar a somar R$ 7.111.885 mil.

## Por que usar Git em vez de upload pelo navegador?

O GitHub [limita arquivos enviados pelo navegador a 25 MiB, avisa em Git acima de 50 MiB e bloqueia acima de 100 MiB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). Este CSV tem cerca de 70,7 MiB, portanto cabe em Git comum, mas excede o limite do navegador. O procedimento de criação de repositório vazio e `git remote add`/`git push` segue a [documentação oficial de importação](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github). Para autenticação HTTPS, veja as [opções oficiais do Git Credential Manager](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git).
