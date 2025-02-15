from collections import defaultdict


def limpar_csv_sem_csv(caminho_arquivo):
    dados = []
    linha_atual = ""  # Para armazenar linhas de descrições longas
    dentro_de_aspas = False  # Para controlar se estamos dentro de uma descrição entre aspas

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        next(f)  # Pula a primeira linha (cabeçalhos)
        for linha in f:
            linha = linha.strip()  # Remove espaços extras ao redor

            if dentro_de_aspas:
                linha_atual += " " + linha  # Junta as linhas na mesma string
                if linha.count('"') % 2 != 0:  # Se encontramos um número ímpar de aspas, fechamos a descrição
                    dentro_de_aspas = False
                    dados.append(separar_campos(linha_atual))  # Processamos a linha completa agora
                    linha_atual = ""  # Resetamos a linha acumulada
                continue

            if linha.count('"') % 2 != 0:  # Se a linha tem aspas ímpares, significa que começou uma descrição longa
                dentro_de_aspas = True
                linha_atual = linha  # Começamos a acumular
                continue

            # Linha normal, processamos e adicionamos
            if linha:
                dados.append(separar_campos(linha))

    return dados


def separar_campos(linha):
    """Separa os campos respeitando aspas e ponto e vírgula."""
    campos = []
    campo_atual = ""
    dentro_de_aspas = False

    for char in linha:
        if char == '"':
            dentro_de_aspas = not dentro_de_aspas  # Alterna estado de dentro/fora de aspas
        elif char == ";" and not dentro_de_aspas:
            campos.append(campo_atual.strip())  # Adiciona campo completo
            campo_atual = ""
        else:
            campo_atual += char  # Adiciona caractere ao campo atual

    campos.append(campo_atual.strip())  # Adiciona o último campo
    return campos


def listar_compositores_ordenados(dados):
    """Extrai a lista de compositores, remove duplicatas e ordena alfabeticamente."""
    compositores = set()  # Usamos um set para evitar repetição

    for linha in dados:
        if len(linha) > 4:  # Supondo que o nome do compositor esteja na 5ª coluna (índice 4)
            compositor = linha[4].strip()
            if compositor:  # Apenas adiciona se não for uma string vazia
                compositores.add(compositor)

    return sorted(compositores)  # Retorna a lista ordenada


def distribuicao_por_periodo(dados):
    """Conta quantas obras estão catalogadas em cada período."""
    distribuicao = defaultdict(int)  # Usamos defaultdict para contar automaticamente

    for linha in dados:
        if len(linha) > 3:  # Supondo que o período esteja na 6ª coluna (índice 5)
            periodo = linha[3].strip()
            if periodo:  # Só adiciona se o período não for vazio
                distribuicao[periodo] += 1

    # Ordena a distribuição por nome de período
    return dict(sorted(distribuicao.items()))  # Retorna o dicionário ordenado pelo nome do período


def dicionario_periodo_titulos(dados):
    """Retorna um dicionário em que a cada período está associada uma lista alfabética dos títulos das obras."""
    periodos = defaultdict(list)  # Usamos defaultdict para listas

    for linha in dados:
        if len(linha) > 3:  # Supondo que o título da obra esteja na 2ª coluna (índice 1) e o período na 4ª (índice 3)
            titulo = linha[0].strip()
            periodo = linha[3].strip()

            if titulo and periodo:  # Só adiciona se o título e o período não forem vazios
                periodos[periodo].append(titulo)

    # Ordena as listas de títulos alfabética por período
    for periodo in periodos:
        periodos[periodo].sort()

    return dict(periodos)  # Retorna o dicionário ordenado por período


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
