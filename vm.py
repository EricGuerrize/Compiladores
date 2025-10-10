"""
Maquina Virtual - MaqHipo
Interpretador para executar codigo objeto gerado pelo compilador
"""

class MaquinaVirtual:
    def __init__(self):
        # area de codigo - armazena as instrucoes
        self.C = []
        
        # area de dados - pilha para valores
        self.D = []
        self.s = -1  # topo da pilha
        
        # registrador de programa
        self.i = 0   # proxima instrucao
        
        # mapa de rotulos
        self.rotulos = {}
        
        # flag pra parar execucao
        self.executando = True
    
    def carregar_codigo(self, arquivo):
        """Lê o arquivo de código objeto e carrega na área C"""
        print(f"\nCarregando codigo objeto de '{arquivo}'...")
        
        with open(arquivo, 'r') as f:
            linhas = f.readlines()
        
        # Primeira passagem: identifica rótulos
        posicao = 0
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            
            # Verifica se é um rótulo (formato: R0:, R1:, etc.)
            if linha.startswith('R') and ':' in linha:
                rotulo = linha.rstrip(':')
                self.rotulos[rotulo] = posicao
                print(f"  Rotulo '{rotulo}' na posicao {posicao}")
            else:
                self.C.append(linha)
                posicao += 1
        
        print(f"{len(self.C)} instrucoes carregadas")
        print(f"{len(self.rotulos)} rotulos identificados")
    
    def executar(self):
        """Executa o programa carregado"""
        print("\nIniciando execucao...\n")
        
        while self.executando and self.i < len(self.C):
            instrucao = self.C[self.i]
            print(f"[{self.i:03d}] {instrucao:20s} | Pilha: {self.D[:self.s+1] if self.s >= 0 else '[]'}")
            
            self.executar_instrucao(instrucao)
            
            # Se não houve desvio, avança para próxima instrução
            if self.executando:
                self.i += 1
        
        print("\nExecucao finalizada!")
        print(f"Estado final da pilha: {self.D[:self.s+1] if self.s >= 0 else '[]'}")
    
    def executar_instrucao(self, instrucao):
        """Decodifica e executa uma instrução"""
        partes = instrucao.split()
        cmd = partes[0]
        
        # Instruções de controle
        if cmd == 'INPP':
            self.instr_INPP()
        elif cmd == 'PARA':
            self.instr_PARA()
        
        # Instruções de memória
        elif cmd == 'ALME':
            self.instr_ALME(int(partes[1]))
        elif cmd == 'CRVL':
            self.instr_CRVL(int(partes[1]))
        elif cmd == 'CRCT':
            self.instr_CRCT(float(partes[1]))
        elif cmd == 'ARMZ':
            self.instr_ARMZ(int(partes[1]))
        
        # I/O
        elif cmd == 'LEIT':
            self.instr_LEIT()
        elif cmd == 'IMPR':
            self.instr_IMPR()
        
        # Operações aritméticas
        elif cmd == 'SOMA':
            self.instr_SOMA()
        elif cmd == 'SUBT':
            self.instr_SUBT()
        elif cmd == 'MULT':
            self.instr_MULT()
        elif cmd == 'DIVI':
            self.instr_DIVI()
        
        # Comparações
        elif cmd == 'CPMA':
            self.instr_CPMA()
        elif cmd == 'CPME':
            self.instr_CPME()
        elif cmd == 'CPIG':
            self.instr_CPIG()
        elif cmd == 'CDES':
            self.instr_CDES()
        elif cmd == 'CMAG':
            self.instr_CMAG()
        elif cmd == 'CMEG':
            self.instr_CMEG()
        
        # Desvios
        elif cmd == 'DSVF':
            self.instr_DSVF(partes[1])
        elif cmd == 'DSVI':
            self.instr_DSVI(partes[1])
        
        else:
            raise Exception(f"Instrução desconhecida: {cmd}")
    
    # ============= IMPLEMENTAÇÃO DAS INSTRUÇÕES =============
    
    def instr_INPP(self):
        """Inicia o programa"""
        self.s = -1
        self.D = []
    
    def instr_PARA(self):
        """Para a execução"""
        self.executando = False
    
    def instr_ALME(self, m):
        """Aloca m posições na pilha"""
        for _ in range(m):
            self.s += 1
            self.D.append(0.0)
    
    def instr_CRVL(self, n):
        """Carrega valor do endereço n no topo da pilha"""
        self.s += 1
        if self.s >= len(self.D):
            self.D.append(0.0)
        self.D[self.s] = self.D[n]
    
    def instr_CRCT(self, k):
        """Carrega constante k no topo da pilha"""
        self.s += 1
        if self.s >= len(self.D):
            self.D.append(0.0)
        self.D[self.s] = k
    
    def instr_ARMZ(self, n):
        """Armazena topo da pilha no endereço n"""
        self.D[n] = self.D[self.s]
        self.s -= 1
    
    def instr_LEIT(self):
        """Lê valor da entrada"""
        valor = float(input("Digite um valor: "))
        self.s += 1
        if self.s >= len(self.D):
            self.D.append(0.0)
        self.D[self.s] = valor
    
    def instr_IMPR(self):
        """Imprime valor do topo da pilha"""
        print(f"Saida: {self.D[self.s]}")
        self.s -= 1
    
    def instr_SOMA(self):
        """Soma os dois valores do topo"""
        resultado = self.D[self.s-1] + self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_SUBT(self):
        """Subtrai os dois valores do topo"""
        resultado = self.D[self.s-1] - self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_MULT(self):
        """Multiplica os dois valores do topo"""
        resultado = self.D[self.s-1] * self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_DIVI(self):
        """Divide os dois valores do topo"""
        resultado = self.D[self.s-1] / self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CPMA(self):
        """Compara se s-1 > s"""
        resultado = 1.0 if self.D[self.s-1] > self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CPME(self):
        """Compara se s-1 < s"""
        resultado = 1.0 if self.D[self.s-1] < self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CPIG(self):
        """Compara se s-1 == s"""
        resultado = 1.0 if self.D[self.s-1] == self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CDES(self):
        """Compara se s-1 != s"""
        resultado = 1.0 if self.D[self.s-1] != self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CMAG(self):
        """Compara se s-1 >= s"""
        resultado = 1.0 if self.D[self.s-1] >= self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CMEG(self):
        """Compara se s-1 <= s"""
        resultado = 1.0 if self.D[self.s-1] <= self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_DSVF(self, rotulo):
        """Desvia se topo da pilha for 0 (falso)"""
        if self.D[self.s] == 0.0:
            self.i = self.rotulos[rotulo] - 1  # -1 porque vai incrementar depois
        self.s -= 1
    
    def instr_DSVI(self, rotulo):
        """Desvia incondicionalmente"""
        self.i = self.rotulos[rotulo] - 1  # -1 porque vai incrementar depois


# ============= PROGRAMA PRINCIPAL =============

if __name__ == "__main__":
    import sys
    
    # Define o arquivo de entrada
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "codigo-gerado.txt"
    
    try:
        # Cria a máquina virtual
        vm = MaquinaVirtual()
        
        # Carrega o código
        vm.carregar_codigo(arquivo)
        
        # Executa
        vm.executar()
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{arquivo}' nao encontrado!")
        print("Execute primeiro o compilador: python main.py")
    except Exception as e:
        print(f"ERRO durante execucao: {e}")
        import traceback
        traceback.print_exc()