import sys
from typing import List
import syntax as ast
from vm_translator import PascalEWVMTranslator
from parser import PascalParser
from lexer import PascalLexer
import traceback

def translate_pascal_file(file_path: str, translator: PascalEWVMTranslator) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        lexer = PascalLexer()
        lexer.build()
        parser = PascalParser(lexer)

        ast_tree = parser.parse(code)
        if parser.error_count > 0:
            print(f"Error: Parsing failed for {file_path} with {parser.error_count} syntax errors")
            return []
        
        ewvm_code = translator.translate(ast_tree)
        return ewvm_code
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except ast.TranslationError as e:
        print(f"Translation error in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}")
        print("Stack trace:")
        traceback.print_exc()
        return []

def main():
    translator = PascalEWVMTranslator()
    file_paths = sys.argv[1:]
    
    if not file_paths:
        print("Usage: python test_vm.py <file1.pas> [<file2.pas> ...]")
        print("Please provide at least one Pascal file to process")
        return
    
    for file_path in file_paths:
        print(f"\nProcessing {file_path}:")
        print("-" * 50)
        ewvm_code = translate_pascal_file(file_path, translator)
        if ewvm_code:
            print("Generated EWVM code:")
            for line in ewvm_code:
                print(line)
        print("-" * 50)

if __name__ == '__main__':
    main()