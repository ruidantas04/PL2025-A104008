import sys

def somadoronoff(l, a, state):
    estado = state  
    res = a  
    i = 0

    while i < len(l):
        valor = 0

        if l[i] in "0123456789":
            if estado[0] == "ON":  
                while i < len(l) and l[i] in "0123456789":
                    valor = valor * 10 + int(l[i])
                    i += 1
                res += valor
            else:
                while i < len(l) and l[i] in "0123456789":
                    i += 1

        elif l[i:i + 2].lower() == "on":
            estado[0] = "ON" 
            i += 2

        elif l[i:i + 3].lower() == "off":
            estado[0] = "OFF"  
            i += 3

        elif l[i] == '=':
            print(res)  
            i += 1

        else:
            i += 1
    return res

estado_atual = ["ON"]
soma_total = 0

ficheiro = "C:\\Users\\Utilizador\\Desktop\\3ano2sem\\PL\\TPC1\\Teste.txt"

try:
    with open(ficheiro, "r", encoding="utf-8") as f:
        for linha in f:
            soma_total = somadoronoff(linha, soma_total, estado_atual)

except FileNotFoundError:
    print(f"Erro: O ficheiro '{ficheiro}' não foi encontrado.")
