# script pra rodar compilador e vm em sequencia

import sys
import os

def executar_completo(arquivo_fonte):
    """compila e executa um arquivo mini java"""
    
    print("-"*10)
    print("COMPILADOR MINI JAVA")
    print("-"*10)
    
    # parte 1: compilacao
    print("\nPARTE 1: COMPILANDO")
    print("-"*10)
    
    try:
        from lexico import lexer
        from parser import init_parser
        
        # le arquivo
        if not os.path.exists(arquivo_fonte):
            print(f"ERRO: arquivo '{arquivo_fonte}' nao encontrado")
            return False
        
        with open(arquivo_fonte, "r") as f:
            codigo = f.read()
        
        print(f"Arquivo: {arquivo_fonte}")
        print(f"Tamanho: {len(codigo)} chars\n")
        
        # analise lexica
        print("Analise lexica")
        tokens = lexer(codigo)
        print(f"{len(tokens)} tokens\n")
        
        # sintaxe, semantica e geracao
        print("Analise sintatica e semantica")
        init_parser(tokens)
        
        print("\nCompilacao OK")
        
    except SyntaxError as e:
        print(f"\nERRO DE SINTAXE: {e}")
        return False
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # parte 2: execucao
    print("-"*15)
    print("PARTE 2: EXECUTANDO")
    print("-"*15)
    
    try:
        from vm import MaquinaVirtual
        
        # cria vm e executa
        vm = MaquinaVirtual()
        vm.carregar_codigo("codigo-gerado.txt")
        vm.executar()
        
        print("\nExecucao OK")
        
    except FileNotFoundError:
        print("ERRO: 'codigo-gerado.txt' nao encontrado")
        print("algo deu errado na compilacao")
        return False
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*30)
    print("Finalizado")
    print("="*30)
    return True


def main():
    # qual arquivo usar
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "exemplo.mj"
    
    sucesso = executar_completo(arquivo)
    
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()