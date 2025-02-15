# Titulo
TP2 - Análise de um dataset de obras musicais
# Autor
Rui Gonçalves Dantas - a104008 - 2025-02-15

![Autor](https://github.com/ruidantas04/PL2025-A104008/blob/main/e034a3fe-4b4a-4a78-8cf5-8c200b1753be.jpg)
## Objetivo

Este programa tem como objetivo realizar a análise de dados extraídos de um ficheiro CSV com informações sobre obras musicais. Ele permite a extração e organização de informações como compositores, períodos e títulos das obras. O programa oferece um menu interactivo para que o utilizador possa escolher diferentes tipos de consulta, incluindo:

1. Listar compositores ordenados alfabeticamente.
2. Exibir a distribuição das obras por período.
3. Mostrar um dicionário de títulos de obras classificados por período.

O programa processa os dados de um ficheiro CSV e realiza as consultas conforme solicitado pelo utilizador, sem a necessidade de módulos externos.

## Funcionalidades

- **Limpeza e processamento do CSV**: O programa lê o ficheiro CSV e limpa as entradas, considerando aspas e separadores correctamente, especialmente para campos com descrições longas que se estendem por várias linhas.
  
- **Listagem de compositores**: O programa extrai os compositores das obras, remove duplicados e retorna uma lista ordenada alfabeticamente.

- **Distribuição das obras por período**: Conta quantas obras estão associadas a cada período e exibe essa distribuição.

- **Dicionário de títulos por período**: Organiza as obras por período, com os seus títulos listados de forma alfabética.

## Como Usar

1. **Prepare o ficheiro CSV**:
   - O ficheiro CSV deve seguir um formato adequado com as colunas: título da obra, compositor e período.
   - O programa espera que as obras sejam separadas por ponto e vírgula (;) e que as informações sobre compositor e período sejam extraídas das colunas correspondentes.
   
2. **Executar o programa**:
   - Para executar o programa, basta correr o código Python. O programa lerá o ficheiro CSV especificado na variável `caminho_arquivo`.
   - O ficheiro de entrada deve estar no mesmo diretório do código ou ser especificado com o caminho completo.
   
3. **Menu Interactivo**:
   - O programa exibe um menu com as seguintes opções:
     1. Listar compositores ordenados alfabeticamente.
     2. Distribuição das obras por período.
     3. Dicionário de títulos por período.
     4. Sair.
   - O utilizador pode seleccionar uma opção digitando o número correspondente.
