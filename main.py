#coding: utf-8
import heapq
import sys
TAM_X = 6
TAM_Y = 6

#busca as coordenadas do tabuleiro que não são acessiveis
def busca_bloqueio(tabuleiro):
    bloqueio = []
    for i in range(TAM_X):
        for j in range(TAM_Y):
            if tabuleiro[i][j] == 1:
                bloqueio.append((j,i))
    return bloqueio
                
#retorna uma lista dos nós adjacentes a algum nó processado
def pega_adjacentes(lista, coord, tam_x, tam_y):
    adj = []
    if coord[0] < tam_x - 1:
        if (coord[0]+1, coord[1]) not in busca_bloqueio(tabuleiro):
            adj.append((coord[0]+1, coord[1]))
    if coord[1] > 0:
        if (coord[0], coord[1]-1) not in busca_bloqueio(tabuleiro):
            adj.append((coord[0],coord[1]-1))
    if coord[0] > 0:
        if (coord[0]-1, coord[1]) not in busca_bloqueio(tabuleiro):
            adj.append((coord[0]-1, coord[1]))
    if coord[1] < tam_y - 1:
        if (coord[0], coord[1]+1) not in busca_bloqueio(tabuleiro):
            adj.append((coord[0], coord[1]+1))
                        
    return adj

#utilidade para a dfs
def dfsu(tabuleiro, vertice, visitado):
    visitado.append(vertice)
    for adj in pega_adjacentes(tabuleiro,vertice,TAM_X,TAM_Y):
        if adj not in visitado:
            if tabuleiro[adj[0]][adj[1]] == 2:
                visitado.append((adj[0],adj[1]))
                break
            else:
                dfsu(tabuleiro, adj, visitado)

#busca em profundidade
def dfs(tabuleiro, inicio):
    visitado = []
    dfsu(tabuleiro,inicio,visitado)
    return visitado

class No(object):
    def __init__(self,coord,acessivel):
        self.acessivel = acessivel
        self.coord = coord
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class A_star(object):
    def __init__(self, tabuleiro):
        self.lista_aberta = []
        heapq.heapify(self.lista_aberta)
        self.lista_fechada = set()
        self.nos = []
        self.tam_x = TAM_X
        self.tam_y = TAM_Y
        self.tabuleiro = tabuleiro

    def cria_tabuleiro(self,inicio,fim):
        bloqueios = busca_bloqueio(self.tabuleiro)
        for i in range(self.tam_x):
            for j in range(self.tam_y):
                if (i,j) in bloqueios:
                    acessivel = False
                else:
                    acessivel = True
                self.nos.append(No((i,j), acessivel))
        self.inicio = self.get_no(inicio)
        self.fim = self.get_no(fim)

    #retorna o nó da coordenada pedida
    def get_no(self, coord):
        return self.nos[coord[0] * self.tam_y + coord[1]]
    
    #retorna o valor da função de heuristica
    def heuristica(self, no):
        return (abs(no.coord[0] - self.fim.coord[0]) + abs(no.coord[1] - self.fim.coord[1]))*10
    
    #retorna uma lista dos nos adjacentes ao no a ser processado
    def nos_adjacentes(self,no):
        adj = []
        if no.coord[0] < self.tam_x - 1:
            adj.append(self.get_no((no.coord[0]+1, no.coord[1])))
        if no.coord[0] > 0:
            adj.append(self.get_no((no.coord[0]-1, no.coord[1])))
        if no.coord[1] > 0:
            adj.append(self.get_no((no.coord[0], no.coord[1]-1)))
        if no.coord[1] < self.tam_y - 1:
            adj.append(self.get_no((no.coord[0], no.coord[1]+1)))
        return adj

    #armazena o caminho percorrido para chegar na solução
    def pega_caminho(self,caminho):
        no = self.fim
        while no.parent is not self.inicio:
            no = no.parent
            caminho.append(no.coord)
    
    #modifica os custos de cada coordenada durante a execução da busca
    def aplica_heuristica(self, adjacente, no):
        adjacente.g = no.g + 10
        adjacente.h = self.heuristica(adjacente)
        adjacente.parent = no
        adjacente.f = adjacente.g + adjacente.h
    
    #busca A*
    def a(self,caminho):
        heapq.heappush(self.lista_aberta, (self.inicio.f, self.inicio))
        while self.lista_aberta:
            f, no = heapq.heappop(self.lista_aberta)
            self.lista_fechada.add(no)
            if no is self.fim:
                self.pega_caminho(caminho)
                break
            adj = self.nos_adjacentes(no)
            for v in adj:
                if v.acessivel and v not in self.lista_fechada:
                    if (v.f, v) in self.lista_aberta:
                        if v.g > no.g + 10:
                            self.aplica_heuristica(v,no)
                    else:
                        self.aplica_heuristica(v,no)
                        heapq.heappush(self.lista_aberta, (v.f, v))

if __name__ == "__main__":

    '''
    0 = vazio
    1 = obstaculo
    2 = destino
    '''
    
    
    
    if len(sys.argv) == 1:
        print "executando com valores padrão"
        tabuleiro = [[0,0,0,0,0,1],
                     [1,1,1,1,0,1],
                     [0,0,0,0,0,1],
                     [0,1,1,1,0,1],
                     [0,1,0,1,0,1],
                     [0,1,0,0,0,2]]
    
        #DFS
        print '==================================='
        print "Resultado da busca por DFS: "
        c = dfs(tabuleiro, (0,0))
        for i in c:
            print str(i) + "->",
        print '\n'
        #A*
        print '==================================='
        print "Resultado da busca A*: "
        caminho = []
        p = A_star(tabuleiro)
        p.cria_tabuleiro((0,0),(5,5))
        p.a(caminho)
        caminho.reverse()
        caminho.insert(0,(0,0))
        caminho.append((5,5))
        for i in caminho:
            print str(i) + "->",
        print '\n'
        
    elif len(sys.argv) == 2:
        inicio = (0,0)
        with open(sys.argv[1]) as arq:
            tabuleiro = [[int(i) for i in line.strip()] for line in arq]
        for i in range(len(tabuleiro[0])):
            for j in range(len(tabuleiro[0])):
                if tabuleiro[i][j] == 2:
                    fim = (i,j)
        TAM_X = len(tabuleiro[0])
        TAM_Y = len(tabuleiro[0])
        #DFS
        print '==================================='
        print "Resultado da busca por DFS: "
        c = dfs(tabuleiro, inicio)
        for i in c:
            if tabuleiro[i[0]][i[1]] == 2:
                print str(i) + "->",
                break
            else:
                print str(i) + "->",
        print '\n'
        #A*
        print '==================================='
        print "Resultado da busca A*: "
        caminho = []
        p = A_star(tabuleiro)
        p.cria_tabuleiro(inicio,fim)
        p.a(caminho)
        caminho.reverse()
        caminho.insert(0,inicio)
        caminho.append(fim)
        for i in caminho:
            print str(i) + "->",
        print '\n'
    
    else:
        print "./main.py <arquivo.txt> : executa a busca sobre um tabuleiro do arquivo"
        print "./main.py : executa uma busca para um tabuleiro padrão"
