# **Máquina de Venda Automática**  

## **Autor**  
Rui Gonçalves Dantas - a104008 - 2025-03-18  
![Autor](https://github.com/ruidantas04/PL2025-A104008/blob/main/e034a3fe-4b4a-4a78-8cf5-8c200b1753be.jpg)

## **Descrição**
Este projeto implementa um analisador sintático para processar expressões matemáticas simples. O objetivo principal é permitir que o programa calcule a solução de expressões que envolvem os operadores adição (+), subtração (-) e multiplicação (*), respeitando a precedência dos operadores.
O projeto utiliza a biblioteca PLY (Python Lex-Yacc) para construir o lexer e o parser, proporcionando uma abordagem funcional para o processamento de expressões aritméticas simples.

## **Implementação** 
O projeto é dividido em três módulos principais:

1. analex.py: Contém o lexer, responsável por converter a entrada em tokens reconhecíveis, como números e operadores.
2. anasin.py: Contém o parser, que utiliza os tokens do lexer para avaliar e calcular a expressão matemática.
3. program.py: Arquivo principal onde o programa lê a entrada do usuário e utiliza o parser para calcular o resultado.

## **Estrutura de Código**
### analex.py - Lexer (Analisador Léxico)
O lexer é responsável por dividir a entrada em tokens. Ele reconhece os seguintes tipos de tokens:

NUM: Números inteiros.
PLUS: Operador de adição (+).
MINUS: Operador de subtração (-).
MULT: Operador de multiplicação (*).
As expressões regulares no arquivo analex.py são responsáveis por identificar esses tokens e convertê-los em uma forma manipulável pelo parser.

### anasin.py - Parser (Analisador Sintático)
O parser utiliza os tokens do lexer para analisar a expressão matemática. O programa segue as seguintes regras de precedência:

Multiplicação (*) tem a maior precedência e é calculada primeiro.
Adição (+) e Subtração (-) têm a mesma precedência e são avaliadas da esquerda para a direita.
A função principal do parser é chamada rec_Parser, que inicia o processo de análise, chamando funções recursivas para cada parte da expressão.

### program.py - Execução do Programa
Este arquivo é responsável por:

1. Solicitar uma expressão ao utilizador.
2. Passar a entrada para o lexer e parser.
3. Exibir o resultado da expressão calculada.
### Funções Principais no Parser (anasin.py)

1. rec_Fator(): Processa números (tokens de tipo NUM).
2. rec_Termo(): Processa termos, incluindo multiplicações.
3. rec_Expressao(): Processa a expressão inteira, lidando com adições e subtrações.
4. rec_Parser(data): A função principal que inicializa o lexer e chama o parser para analisar a expressão.
