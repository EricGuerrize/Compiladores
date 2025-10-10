compilador mini java
## desc

compilador para a linguagem minijava, inclui: analisador lexico, sintatico, semantico 

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
mini-java-gramatica-v2.txt: gramatica de lingaugem