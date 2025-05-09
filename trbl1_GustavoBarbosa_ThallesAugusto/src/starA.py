# Algoritmo A* para encontrar o caminho mais curto em um grafo
# Gustavo Barbosa Neves 
#  Thalles Augusto Monteiro Martins 

grafo_romenia = { 
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Rimnicu Vilcea": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}



heuristica_bucharest = { 
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}


def busca_a_estrela(grafo, heuristica, inicio, objetivo):
    from queue import PriorityQueue
    # Fila de prioridade para armazenar os nós a serem explorados
    fila = PriorityQueue()
    fila.put((0 + heuristica[inicio], 0, inicio))  # (f(n), g(n), nó)
    visitados = set()  # Conjunto para rastrear os nós visitados
    caminho = {}  # Dicionário para reconstruir o caminho
    custo_atual = {inicio: 0}  # Custo acumulado para cada nó
    cont = 0

    while not fila.empty():
        print('Fila: ',fila.queue)
        cont += 1
        _, g_atual, atual = fila.get()  # Pega o nó com menor f(n)
        print('Atual: ',atual, g_atual, _)
        if atual == objetivo:
            # Reconstrói o caminho a partir do objetivo
            caminho_final = []
            while atual:
                caminho_final.append(atual)
                atual = caminho.get(atual)
                #print('Caminho: ',caminho_final)
            return caminho_final[::-1]  # Retorna o caminho na ordem correta
        visitados.add(atual)
        print('Contador: ',cont)
        print('Visitados: ',visitados)
        # Explora os vizinhos do nó atual
        for vizinho, custo in grafo[atual].items():
            novo_custo = g_atual + custo  # Calcula g(n) para o vizinho
            if vizinho not in visitados or novo_custo < custo_atual.get(vizinho, float('inf')):
                custo_atual[vizinho] = novo_custo
                f_n = novo_custo + heuristica[vizinho]  # Calcula f(n) = g(n) + h(n)
                fila.put((f_n, novo_custo, vizinho))
                caminho[vizinho] = atual  # Armazena o nó anterior para reconstruir o caminho
    return None  # Retorna None se não encontrar o objetivo


# Exemplo de uso
inicio = "Arad"
objetivo = "Bucharest"
caminho = busca_a_estrela(grafo_romenia, heuristica_bucharest, inicio, objetivo)

if caminho:
    # Calcula o total de milhas percorridas
    total_milhas = 0
    for i in range(len(caminho) - 1):
        total_milhas += grafo_romenia[caminho[i]][caminho[i + 1]]
    print("Caminho encontrado:", " -> ".join(caminho))
    print("Total de milhas percorridas: ",  total_milhas)

else:
    print("Caminho não encontrado.")
