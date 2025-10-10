compilador mini java

## desc

Projeto desenvolvido para a disciplina **Compiladores 2** (UFMT).  
Implementa um compilador completo para uma linguagem MiniJava, com:
- análise léxica
- análise sintática
- análise semântica
- geração de código objeto
- máquina virtual (MaqHipo)

## requisistos
python 3.x

## como executar

### opcao 1: exec compilacao + execuccao (recomendo)
```bash 
python executar.py exemplo.mj
```

### opcao 3
# 1 => 
python main.py -> gera o arquivo codigo-gerado.txt

# 2=> 
python vm.py

Estrutura do projeto:

lexico.py : analisador lexico
parser.oy : analisar sintatico
vm.py : maquina virtual(interpretador)
executar.py : scprit para executar ambas partes
exemplo.mj: exemplo de codigo mini java

------------------------
