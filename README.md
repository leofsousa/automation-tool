# Automation Tool

Aplicativo desktop em Python para automacoes internas corporativas no Windows.

A primeira funcionalidade implementada e um renomeador de arquivos em massa com preview antes da confirmacao. A arquitetura ja foi organizada para crescer com novos modulos, incluindo um futuro formatador inteligente de Excel com suporte a `pandas`, `openpyxl` e integracao posterior com IA via API.

## Funcionalidades Atuais

- Selecionar uma pasta local.
- Listar arquivos encontrados.
- Aplicar regras de renomeacao.
- Exibir preview antes de renomear.
- Confirmar a operacao manualmente.
- Registrar logs/status da operacao.
- Preservar extensao original dos arquivos.
- Evitar sobrescrever arquivos existentes.

## Regra Inicial De Renomeacao

Exemplo:

```text
BATERIA 11 [17-05] DOM M T N CR.mp4
```

Resultado:

```text
BAT 11.mp4
```

Regras aplicadas:

- `BATERIA` vira `BAT`.
- Conteudos entre colchetes sao removidos.
- Textos extras apos o numero principal sao removidos.
- A extensao original do arquivo e preservada.
- Arquivos com conflitos de nome nao sao renomeados automaticamente.

## Estrutura Do Projeto

```text
automation_tool/
├── main.py
├── requirements.txt
├── README.md
├── ui/
│   ├── __init__.py
│   ├── home.py
│   ├── rename_page.py
│   └── excel_page.py
├── services/
│   ├── __init__.py
│   ├── rename_service.py
│   └── excel_service.py
├── utils/
│   ├── __init__.py
│   ├── patterns.py
│   ├── file_helpers.py
│   └── text_helpers.py
└── assets/
    └── .gitkeep
```

## Responsabilidade Das Pastas

### `ui/`

Contem as telas da aplicacao.

- `home.py`: janela principal e navegacao por abas.
- `rename_page.py`: interface do renomeador de arquivos.
- `excel_page.py`: tela reservada para o futuro formatador de Excel.

### `services/`

Contem as regras de negocio da aplicacao.

- `rename_service.py`: regras de preview e renomeacao de arquivos.
- `excel_service.py`: ponto inicial para a futura logica de processamento de Excel.

### `utils/`

Contem funcoes auxiliares reutilizaveis.

- `file_helpers.py`: funcoes para leitura e validacao de arquivos/pastas.
- `text_helpers.py`: funcoes de tratamento de texto.
- `patterns.py`: constantes e padroes reutilizaveis.

### `assets/`

Pasta reservada para icones, imagens e outros recursos visuais futuros.

## Requisitos

- Windows 10 ou superior.
- Python 3.12 ou superior.
- PowerShell.

Dependencias Python:

- `pandas`
- `openpyxl`
- `pyinstaller`

As dependencias estao listadas em:

```text
requirements.txt
```

## Como Preparar O Ambiente

Abra o PowerShell na pasta do projeto:

```powershell
cd C:\caminho\para\automation_tool
```

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

### Opcao 1: Ativar O Ambiente Virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execucao de scripts, execute:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Depois confirme com:

```text
S
```

Em seguida, ative novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Opcao 2: Sem Ativar O Ambiente Virtual

Se estiver em um computador corporativo com restricoes no PowerShell, use diretamente o Python do ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Como Executar A Aplicacao

Com o ambiente virtual ativado:

```powershell
python main.py
```

Sem ativar o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Como Usar O Renomeador

1. Abra a aplicacao.
2. Clique em `Selecionar pasta`.
3. Escolha a pasta que contem os arquivos.
4. Confira a coluna de preview com o novo nome.
5. Clique em `Renomear`.
6. Confirme a operacao.
7. Verifique os logs/status no painel inferior.

## Como Gerar O Executavel `.exe`

Com o ambiente virtual ativado:

```powershell
python -m PyInstaller --noconfirm --onefile --windowed --name AutomationTool main.py
```

Sem ativar o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --onefile --windowed --name AutomationTool main.py
```

O executavel sera gerado em:

```text
dist\AutomationTool.exe
```

Esse `.exe` pode ser executado em outro computador Windows sem instalar Python, desde que o executavel tenha sido gerado corretamente com PyInstaller.

## Arquivos Que Nao Devem Ir Para O GitHub

Recomenda-se criar um arquivo `.gitignore` com:

```gitignore
.venv/
venv/
env/

__pycache__/
*.py[cod]
*$py.class

build/
dist/
*.spec

*.log
*.tmp
*.bak

.vscode/
.idea/

.DS_Store
Thumbs.db
```

## Fluxo Recomendado Com GitHub

Inicializar o repositorio:

```powershell
git init
git add .
git commit -m "Initial desktop automation tool"
```

Conectar ao GitHub:

```powershell
git remote add origin https://github.com/SEU_USUARIO/automation_tool.git
git branch -M main
git push -u origin main
```

Criar uma nova funcionalidade:

```powershell
git checkout -b feature/excel-formatter
```

Salvar alteracoes:

```powershell
git add .
git commit -m "Add Excel formatter module"
git push -u origin feature/excel-formatter
```

## Releases

Para distribuir versoes fechadas do aplicativo:

1. Gere o `.exe` com PyInstaller.
2. Crie uma tag de versao:

```powershell
git tag v0.1.0
git push origin v0.1.0
```

3. No GitHub, acesse `Releases`.
4. Crie uma nova release usando a tag.
5. Anexe o arquivo:

```text
dist\AutomationTool.exe
```

Sugestao de versionamento:

```text
v0.1.0 - primeiro renomeador funcional
v0.2.0 - formatador de Excel
v0.3.0 - melhorias de interface
v1.0.0 - versao estavel para uso interno
```

## Proximos Passos

- Adicionar `.gitignore`.
- Criar testes automatizados para as regras de renomeacao.
- Implementar historico de operacoes.
- Implementar desfazer renomeacao.
- Iniciar o formatador inteligente de Excel.
- Preparar camada futura para integracao com IA via API.
