# **Analisador Léxico**  

## **Autor**  
Rui Gonçalves Dantas - a104008 - 2025-03-06  
![Autor](https://github.com/ruidantas04/PL2025-A104008/blob/main/e034a3fe-4b4a-4a78-8cf5-8c200b1753be.jpg)


## **Descrição**  
Este projeto implementa um **lexer** para analisar consultas **SPARQL** usando a biblioteca **PLY (Python Lex-Yacc)**.  
O objetivo é identificar e categorizar os diferentes componentes de uma consulta, como **palavras-chave, identificadores, prefixos, operadores e literais**. 
Este projeto foi desenvolvido para a realização do TPC4 de Processamento de Linguagens.

## **Funcionalidades**  
O lexer suporta os seguintes tokens:  
- **Palavras-chave:** `select`, `where`, `LIMIT`, `a`  
- **Identificadores:** Variáveis iniciadas com `?`  
- **Prefixos e sufixos:** Reconhecimento de `prefixo:sufixo`  
- **Strings:** Texto entre aspas   
- **Números:** Inteiros  
- **Delimitadores:** `{ } .`  
- **Operadores:** `= > < !`  

## **Requisitos**  
- Python 3.x  
- Biblioteca `ply` (instale com `pip install ply`)  

## **Como Usar**  
1. Clone este repositório ou copie o código do lexer.  
2. Execute o script Python contendo o lexer.  
3. O lexer processará a entrada e imprimirá os tokens gerados.  

### **Exemplo de Uso**  
```python  
import lex
lexer.input("""
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
""")  
while (token := lexer.token()):  
    print(token)  
```
### **Explicação da Implementação**

O lexer foi desenvolvido utilizando a biblioteca PLY, que permite definir tokens com expressões regulares e funções associadas.

#### **Definição dos Tokens**

Foi criada uma lista de tokens, onde cada nome representa um tipo de elemento da linguagem.

Cada token é definido usando uma expressão regular, que descreve como ele deve ser reconhecido.

#### **Identificação de Tokens**

Para palavras-chave (select, where, LIMIT), são usadas funções t_KW_* que retornam os tokens correspondentes.

Para tokens simples, como operadores e delimitadores, são atribuídas expressões regulares diretamente.

O tratamento de prefixos e sufixos (exemplo: dbo:MusicalArtist) é feito separando a parte antes e depois dos :.

#### **Manejo de Erros**

Se um caractere não reconhecido for encontrado, ele é ignorado e um aviso é impresso.


