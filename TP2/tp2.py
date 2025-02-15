from collections import defaultdict


def limpar_csv_sem_csv(caminho_arquivo):
    dados = []
    linha_atual = ""
    dentro_de_aspas = False

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        next(f)
        for linha in f:
            linha = linha.strip()

            if dentro_de_aspas:
                linha_atual += " " + linha
                if linha.count('"') % 2 != 0:
                    dentro_de_aspas = False
                    dados.append(separar_campos(linha_atual))
                    linha_atual = ""
                continue

            if linha.count('"') % 2 != 0:
                dentro_de_aspas = True
                linha_atual = linha
                continue

            if linha:
                dados.append(separar_campos(linha))

    return dados


def separar_campos(linha):
    campos = []
    campo_atual = ""
    dentro_de_aspas = False

    for char in linha:
        if char == '"':
            dentro_de_aspas = not dentro_de_aspas
        elif char == ";" and not dentro_de_aspas:
            campos.append(campo_atual.strip())
            campo_atual = ""
        else:
            campo_atual += char

    campos.append(campo_atual.strip())
    return campos


def listar_compositores_ordenados(dados):
    compositores = set()

    for linha in dados:
        if len(linha) > 4:
            compositor = linha[4].strip()
            if compositor:
                compositores.add(compositor)

    return sorted(compositores)


def distribuicao_por_periodo(dados):
    distribuicao = defaultdict(int)

    for linha in dados:
        if len(linha) > 3:
            periodo = linha[3].strip()
            if periodo:
                distribuicao[periodo] += 1

    return dict(sorted(distribuicao.items()))


def dicionario_periodo_titulos(dados):
    periodos = defaultdict(list)

    for linha in dados:
        if len(linha) > 3:
            titulo = linha[0].strip()
            periodo = linha[3].strip()

            if titulo and periodo:
                periodos[periodo].append(titulo)

    for periodo in periodos:
        periodos[periodo].sort()

    return dict(periodos)


def main():
    caminho_arquivo = "obras.csv"
    dados_limpos = limpar_csv_sem_csv(caminho_arquivo)

    while True:
        print("\n=== MENU ===")
        print("1 - Listar compositores ordenados alfabeticamente")
        print("2 - Distribuição das obras por período")
        print("3 - Dicionário de títulos por período")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            compositores_ordenados = listar_compositores_ordenados(dados_limpos)
            print("\nLista de compositores ordenados alfabeticamente:")
            for compositor in compositores_ordenados:
                print(compositor)

        elif opcao == "2":
            distribuicao = distribuicao_por_periodo(dados_limpos)
            print("\nDistribuição das obras por período:")
            for periodo, quantidade in distribuicao.items():
                print(f"{periodo}: {quantidade} obras")

        elif opcao == "3":
            dicionario_titulos = dicionario_periodo_titulos(dados_limpos)
            print("\nDicionário de títulos por período:")
            for periodo, titulos in dicionario_titulos.items():
                print(f"{periodo}:")
                for titulo in titulos:
                    print(f"  - {titulo}")

        elif opcao == "4":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
