# Maquina Virtual (MaqHipo)
# Interpretador simples para executar o código-objeto do compilador

VERBOSE = False  # mude para True se quiser ver o passo a passo

def dbg(msg):
    if VERBOSE:
        print(msg)

class MaquinaVirtual:
    
    # estado interno
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
        # carrega o código-objeto em C e coleta rótulos
        dbg(f"carregando código de '{arquivo}'...")
        
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
                dbg(f"rótulo '{rotulo}' na posição {posicao}")
            else:
                self.C.append(linha)
                posicao += 1
        
        print(f"{len(self.C)} instruções carregadas")
        dbg(f"{len(self.rotulos)} rótulos identificados")
    
    def executar(self):
        # roda as instruções carregadas
        dbg("iniciando execução...")
        
        while self.executando and self.i < len(self.C):
            instrucao = self.C[self.i]
            dbg(f"[{self.i:03d}] {instrucao:20s} | pilha: {self.D[:self.s+1] if self.s >= 0 else '[]'}")
            
            self.executar_instrucao(instrucao)
            
            # Se não houve desvio, avança para próxima instrução
            if self.executando:
                self.i += 1
        
        dbg("execução finalizada")
        dbg(f"pilha final: {self.D[:self.s+1] if self.s >= 0 else '[]'}")
    
    def executar_instrucao(self, instrucao):
        # decodifica e executa uma instrução
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
    
    #  implementacao das intsr
    
    def instr_INPP(self):
        # inicia o programa (zera pilha)
        self.s = -1
        self.D = []
    
    def instr_PARA(self):
        # para a execução
        self.executando = False
    
    def instr_ALME(self, m):
        # aloca m posições na pilha
        for _ in range(m):
            self.s += 1
            self.D.append(0.0)
    
    def instr_CRVL(self, n):
        # carrega valor do endereço n
        self.s += 1
        if self.s >= len(self.D):
            self.D.append(0.0)
        self.D[self.s] = self.D[n]
    
    def instr_CRCT(self, k):
        # carrega constante k
        self.s += 1
        if self.s >= len(self.D):
            self.D.append(0.0)
        self.D[self.s] = k
    
    def instr_ARMZ(self, n):
        # armazena topo no endereço n
        self.D[n] = self.D[self.s]
        self.s -= 1
    
    def instr_LEIT(self):
        # lê um valor do usuário
        valor = float(input("Digite um valor: "))
        self.s += 1
        if self.s >= len(self.D):
            self.D.append(0.0)
        self.D[self.s] = valor
    
    def instr_IMPR(self):
        # imprime o topo
        print(self.D[self.s])
        self.s -= 1
    
    def instr_SOMA(self):
        # soma D[s-1] + D[s]
        resultado = self.D[self.s-1] + self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_SUBT(self):
        # subtrai D[s-1] - D[s]
        resultado = self.D[self.s-1] - self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_MULT(self):
        # multiplica D[s-1] * D[s]
        resultado = self.D[self.s-1] * self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_DIVI(self):
        # divide D[s-1] / D[s]
        resultado = self.D[self.s-1] / self.D[self.s]
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CPMA(self):
        # compara D[s-1] > D[s]
        resultado = 1.0 if self.D[self.s-1] > self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CPME(self):
        # compara D[s-1] < D[s]
        resultado = 1.0 if self.D[self.s-1] < self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CPIG(self):
        # compara D[s-1] == D[s]
        resultado = 1.0 if self.D[self.s-1] == self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CDES(self):
        # compara D[s-1] != D[s]
        resultado = 1.0 if self.D[self.s-1] != self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CMAG(self):
        # compara D[s-1] >= D[s]
        resultado = 1.0 if self.D[self.s-1] >= self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_CMEG(self):
        # compara D[s-1] <= D[s]
        resultado = 1.0 if self.D[self.s-1] <= self.D[self.s] else 0.0
        self.s -= 1
        self.D[self.s] = resultado
    
    def instr_DSVF(self, rotulo):
        # desvia se topo == 0
        if self.D[self.s] == 0.0:
            self.i = self.rotulos[rotulo] - 1  # -1 porque vai incrementar depois
        self.s -= 1
    
    def instr_DSVI(self, rotulo):
        # desvia incondicionalmente
        self.i = self.rotulos[rotulo] - 1  # -1 porque vai incrementar depois


#  progrma  principalgit

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
        print(f"erro: arquivo '{arquivo}' não encontrado")
    except Exception as e:
        print(f"erro durante a execução: {e}")