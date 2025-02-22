# Conversor de Markdown para HTML

## Autor
Rui Gonçalves Dantas - a104008 - 2025-02-22  
![Autor](https://github.com/ruidantas04/PL2025-A104008/blob/main/e034a3fe-4b4a-4a78-8cf5-8c200b1753be.jpg)

## Objetivo
Este projeto tem como objetivo implementar um conversor de Markdown para HTML em Python, usando expressões regulares. O programa processa texto no formato Markdown e gera a versão equivalente em HTML, suportando os seguintes elementos:
- Cabeçalhos (#, ##, ###)
- Negrito (**texto** → `<b>texto</b>`)
- Itálico (*texto* → `<i>texto</i>`)
- Listas numeradas (1. Item → `<ol><li>Item</li></ol>`)
- Links ([texto](URL) → `<a href="URL">texto</a>`)
- Imagens (![alt](URL) → `<img src="URL" alt="alt"/>`)

## Funcionalidades
- **Conversão Automática**  
O programa converte automaticamente os elementos Markdown para HTML, mantendo a formatação original. Utiliza expressões regulares para identificar e substituir corretamente cada elemento.

- **Suporte a Diferentes Estruturas**  
  - Cabeçalhos são convertidos para `<h1>`, `<h2>`, `<h3>`, conforme o número de `#`.  
  - Texto em negrito (**texto**) é transformado em `<b>texto</b>`.  
  - Texto em itálico (*texto*) é transformado em `<i>texto</i>`.  
  - Links e imagens são corretamente formatados em HTML.  
  - Listas numeradas são convertidas para `<ol><li>Item</li></ol>`.

## Como Usar
1. **Executar o programa**  
Guarda o código Python no teu computador e executa com `python tp3.py` (ou o nome de ficheiro escolhido).

2. **Inserir o Markdown**  
Escreve o texto diretamente no código ou lê de um ficheiro.

3. **Obter o HTML**  
O programa irá gerar e mostrar o código HTML equivalente ao Markdown inserido. 
