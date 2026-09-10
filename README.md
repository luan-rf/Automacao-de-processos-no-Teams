# Automação de Cancelamento de Solicitações no Microsoft Teams

Automação desenvolvida em **Python** para localizar chamados em uma tela de aprovações do Microsoft Teams e cancelar solicitações que ainda estejam com status **"Solicitado"**.

O projeto utiliza automação de interface gráfica (RPA) com reconhecimento de imagens na tela e uma planilha Excel como fonte de entrada e controle do processamento.

## 🎯 Objetivo

Reduzir o trabalho manual no tratamento de solicitações de cancelamento, permitindo processar uma lista de chamados de forma sequencial e registrar o resultado de cada processamento na própria planilha.

O fluxo automatizado:

1. Abre o Microsoft Teams.
2. Acessa a tela de aprovações.
3. Acessa a seção de itens enviados.
4. Lê os números dos chamados a partir de uma planilha Excel.
5. Localiza cada chamado utilizando o filtro da interface.
6. Identifica chamados não encontrados.
7. Localiza solicitações com status **"Solicitado"**.
8. Abre a solicitação e executa **"Cancelar pedido"**.
9. Confirma visualmente a alteração para **"Cancelado"**.
10. Atualiza o status do processamento na planilha.
11. Salva o progresso após cada chamado.

O salvamento individual permite preservar os resultados já processados caso a execução seja interrompida.

---

## 🛠️ Tecnologias utilizadas

- **Python**
- **Pandas** — leitura e manipulação da planilha
- **PyAutoGUI** — automação da interface gráfica
- **OpenPyXL** — suporte à manipulação de arquivos Excel
- **Pyperclip** — inserção de texto via área de transferência
- **Microsoft Teams Desktop**
- **Jupyter Notebook** — utilizado durante o desenvolvimento

---

## 📁 Estrutura do projeto

```text
automacao-cancelamento-teams/
│
├── data/
│   └── chamados_cancelados.xlsx
│
├── images/
│   ├── aprovacoes_teams.png
│   ├── botao_enviados.png
│   ├── botao_filtrar.png
│   ├── btn_cancelar_pedido.png
│   ├── nao_encontrado.png
│   ├── status_cancelado.png
│   └── status_solicitado.png
│
├── main.py
├── pegar_posicao.py
├── requirements.txt
├── .gitignore
└── README.md
```


---

## 📊 Entrada de dados

A automação utiliza uma planilha Excel contendo, no mínimo, a coluna:

```text
Numero_Chamado
```

Durante o processamento, a aplicação cria automaticamente a coluna:

```text
Status_Processamento
```

### Exemplo

| Numero_Chamado | Status_Processamento |
|---|---|
| CHAMADO001 | Cancelado |
| CHAMADO002 | Já cancelado |
| CHAMADO003 | Não encontrado |
| CHAMADO004 | |

### Status possíveis

| Status | Significado |
|---|---|
| `Cancelado` | Foi encontrada uma solicitação com status "Solicitado" e o cancelamento foi realizado |
| `Já cancelado` | O chamado foi localizado, mas não havia solicitações com status "Solicitado" para cancelar |
| `Não encontrado` | O chamado não foi localizado na interface do Teams |
| vazio | Chamado ainda não processado |

---

## ⚙️ Funcionamento

A automação utiliza reconhecimento de imagens através do `PyAutoGUI` para localizar elementos da interface do Microsoft Teams.

### Localização de elementos

A função `aguarda_imagem()` aguarda até que um determinado elemento visual esteja disponível na tela.

É utilizada em situações em que a aplicação precisa aguardar o carregamento da interface antes de continuar.

### Verificação com tempo limite

A função `imagem_visivel()` verifica se determinado elemento aparece na tela dentro de um período definido.

Isso permite tratar situações como:

- chamado não encontrado;
- botão ainda não disponível;
- elemento que pode ou não aparecer.

### Processamento dos chamados

Para cada chamado:

1. O filtro anterior é limpo.
2. O número do chamado é informado.
3. A pesquisa é executada.
4. O sistema verifica se o chamado foi encontrado.
5. Caso existam solicitações com status `Solicitado`, elas são processadas.
6. O pedido é cancelado.
7. O status `Cancelado` é confirmado visualmente.
8. O resultado é registrado na planilha.

### Controle de progresso

Após cada chamado processado, a planilha é salva.

```python
tabela.to_excel(caminho_planilha, index=False)
```

Esse comportamento permite preservar o progresso da execução.

---

## 🚀 Como executar

### 1. Pré-requisitos

- Windows
- Python 3.x
- Microsoft Teams Desktop
- Acesso à conta utilizada no processo
- Planilha Excel preparada
- Imagens de referência compatíveis com a interface atual do Teams

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente virtual:

```bash
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Preparar a planilha

Coloque a planilha de entrada em:

```text
data/chamados_cancelados.xlsx
```

A planilha deve possuir a coluna:

```text
Numero_Chamado
```

### 5. Executar

```bash
python main.py
```

---

## 🖥️ Automação de interface

O projeto utiliza reconhecimento visual para interagir com a interface do Teams.

As imagens utilizadas como referência são:

```text
images/aprovacoes_teams.png
images/botao_enviados.png
images/botao_filtrar.png
images/btn_cancelar_pedido.png
images/nao_encontrado.png
images/status_cancelado.png
images/status_solicitado.png
```

A automação depende da compatibilidade dessas imagens com a interface apresentada durante a execução.

Alterações no layout do Teams podem exigir a atualização das imagens de referência.

---

## ⚠️ Limitações

Por utilizar automação de interface gráfica, o funcionamento pode ser afetado por:

- alteração da resolução da tela;
- alteração da escala do Windows;
- mudança de posição dos elementos;
- atualização da interface do Microsoft Teams;
- alteração do tema da aplicação;
- carregamento mais lento da interface;
- mudanças nas imagens utilizadas como referência.

Além disso, alguns pontos da automação dependem de coordenadas de tela previamente definidas.

---



## 💡 Aplicação prática

O projeto demonstra a aplicação de Python na automação de um processo operacional de TI, combinando:

- **RPA**
- **Automação de interface gráfica**
- **Manipulação de dados**
- **Excel**
- **Python**
- **Controle de processamento**
- **Reconhecimento visual**
- **Automação de atividades repetitivas**

A solução foi estruturada para reduzir uma atividade manual e repetitiva, mantendo o registro do resultado de cada chamado processado.

---