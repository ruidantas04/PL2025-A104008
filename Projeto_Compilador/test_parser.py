import os
from parser import PascalParser
from lexer import PascalLexer
from view import *

def process_test_file(test_number, lexer, results_dir):
    input_file = f'./Tests/Correct/test{test_number}.txt'
    output_file = f'{results_dir}/resultado{test_number}.txt'
    
    try:
        with open(input_file, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_file}' não foi encontrado.")
        return False

    try:
        parser = PascalParser(lexer)
        ast = parser.parse(code)
    except Exception as e:
        print(f"Erro ao processar {input_file}: {e}")
        return False

    os.makedirs(results_dir, exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(f"=== Resultado do Teste {test_number} ===\n")
        f.write(f"Arquivo de entrada: {input_file}\n")
        f.write(f"Erros de sintaxe encontrados: {parser.error_count}\n\n")
        
        if parser.error_count == 0:
            printer = ASTPrinter()
            f.write(printer.translate(ast))
        else:
            f.write("Não foi possível gerar a AST devido a erros de sintaxe.\n")
    
    return True

def main():
    test_files_range = range(1, 13)
    results_dir = 'Resultados_ast'
    
    lexer = PascalLexer()
    lexer.build()

    print(f"Processando {len(test_files_range)} arquivos de teste...")
    
    success_count = 0
    for test_num in test_files_range:
        print(f"\nProcessando test{test_num}.txt...")
        if process_test_file(test_num, lexer, results_dir):
            success_count += 1
            print(f"Resultado guardado em {results_dir}/resultado{test_num}.txt")
        else:
            print(f"Falha ao processar test{test_num}.txt")

    print(f"\nProcessamento concluído. {success_count}/{len(test_files_range)} testes processados com sucesso.")

if __name__ == "__main__":
    main()