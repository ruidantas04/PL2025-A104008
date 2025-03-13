# **Máquina de Venda Automática**  

## **Autor**  
Rui Gonçalves Dantas - a104008 - 2025-03-13  
![Autor](https://github.com/ruidantas04/PL2025-A104008/blob/main/e034a3fe-4b4a-4a78-8cf5-8c200b1753be.jpg)


## **Descrição**  
Este projeto consiste na implementação de um sistema para uma **máquina de venda automática**, utilizando a biblioteca **PLY (Python Lex-Yacc)** para o processamento de comandos. O objetivo é permitir a **listagem de produtos, inserção de moedas, seleção de produtos e devolução de troco**.

## **Funcionalidades**  
A máquina suporta os seguintes comandos:  
- **LISTAR:** Apresenta os produtos disponíveis e respetivos preços.  
- **MOEDA Xc/Ye:** Insere moedas no saldo (centimos ou euros).  
- **SELECIONAR CÓDIGO:** Permite escolher um produto pelo código.  
- **ADICIONAR CÓDIGO NOME QUANT PRECO:** Adiciona ou atualiza um produto.  
- **SAIR:** Devolve o troco e termina o programa.  

## **Estrutura do Stock**  
O stock dos produtos é armazenado num ficheiro JSON (`stock.json`) e tem o seguinte formato:  
```json  
[
    {"cod": "A23", "nome": "Agua 0.5L", "quant": 4, "preco": 0.7},
    {"cod": "B12", "nome": "Refrigerante 330ml", "quant": 4, "preco": 1.2}
]  
```

## **Exemplo de Uso**  
```python  
>> LISTAR  
maq:  
cod  | nome         | quantidade | preço  
--------------------------------------  
A23  Agua 0.5L       4         0.70e  
B12  Refrigerante 330ml  4         1.20e  

>> MOEDA 2e 50c  
maq: Saldo = 2e50c  

>> SELECIONAR A23  
maq: Pode retirar o produto dispensado "Agua 0.5L"  
maq: Saldo = 1e80c  

>> SAIR  
maq: Pode retirar o troco: 1x 50c, 1x 20c, 1x 10c  
maq: Até à próxima  
```

## **Implementação**  
O código em Python utiliza **análise léxica** para identificar comandos e argumentos.  
Cada comando tem uma função específica que processa a ação correspondente.  
O saldo e o stock são atualizados dinamicamente e armazenados no ficheiro JSON.  

## **Tratamento de Erros e Cenários Especiais**  
O programa considera diferentes cenários que podem ocorrer durante o seu funcionamento:
- **Produto inexistente:** Se um utilizador tentar selecionar um código que não existe, a máquina informa que o produto não foi encontrado.
- **Stock esgotado:** Se o produto estiver sem stock, a máquina avisa o utilizador e não efetua a venda.
- **Saldo insuficiente:** Caso o saldo não seja suficiente para comprar um produto, a máquina informa o utilizador e indica o valor necessário.
- **Devolução de troco:** O troco é devolvido automaticamente quando o utilizador sai, sendo calculado com moedas de 50c, 20c, 10c, 5c, 2c e 1c.
- **Persistência de dados:** O stock é guardado e atualizado num ficheiro JSON, permitindo que a máquina mantenha o estado entre utilizações.
  
## **Conclusão**  
Este projeto demonstra a implementação de um sistema funcional para uma máquina de venda automática, utilizando técnicas de processamento de linguagem natural para interpretar comandos escritos pelo utilizador e garantindo um tratamento eficiente de erros e exceções.
