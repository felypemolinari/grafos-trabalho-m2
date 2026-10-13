import heapq

from coloracao import Cronometro
from grafo import GrafoLista, GrafoMatriz


def _arestas(grafo):
    return [
        (peso, u, v)
        for u in grafo.vertices
        for v, peso in grafo.vizinhos(u)
        if u < v
    ]


def prim(grafo):
    chave = {v: float("inf") for v in grafo.vertices}
    pai = {v: None for v in grafo.vertices}
    na_arvore = set()
    arvore = []
    for raiz in grafo.vertices:
        if raiz in na_arvore:
            continue
        chave[raiz] = 0
        fila = [(0, raiz)]
        while fila:
            k, u = heapq.heappop(fila)
            if u in na_arvore or k > chave[u]:
                continue
            na_arvore.add(u)
            if pai[u] is not None:
                arvore.append((pai[u], u, k))
            for v, peso in grafo.vizinhos(u):
                if v not in na_arvore and peso < chave[v]:
                    chave[v] = peso
                    pai[v] = u
                    heapq.heappush(fila, (peso, v))
    return arvore


def kruskal(grafo):
    pai = {v: v for v in grafo.vertices}
    rank = {v: 0 for v in grafo.vertices}

    def encontrar(v):
        while pai[v] != v:
            pai[v] = pai[pai[v]]
            v = pai[v]
        return v

    def unir(a, b):
        if rank[a] < rank[b]:
            a, b = b, a
        pai[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1

    arvore = []
    for peso, u, v in sorted(_arestas(grafo)):
        ru, rv = encontrar(u), encontrar(v)
        if ru != rv:
            unir(ru, rv)
            arvore.append((u, v, peso))
            if len(arvore) == grafo.num_vertices - 1:
                break
    return arvore


ALGORITMOS = {
    "Prim": prim,
    "Kruskal": kruskal,
}


def soma(arvore):
    return sum(peso for _, _, peso in arvore)


def executar(grafo, algoritmo, nome):
    with Cronometro() as c:
        arvore = algoritmo(grafo)
    print(f"{nome}:")
    print(f"  Tempo de execucao: {c.segundos:.6f} s")
    print(f"  Soma das arestas: {soma(arvore)}")
    print(f"  Numero de arestas: {len(arvore)}")
    if len(arvore) < grafo.num_vertices - 1:
        print("  ATENCAO: grafo desconexo, resultado e uma floresta geradora minima")
    if grafo.num_vertices <= 20:
        for u, v, peso in arvore:
            print(f"    {u} - {v} (peso {peso})")
    return arvore


if __name__ == "__main__":
    import sys

    arquivo = sys.argv[1] if len(sys.argv) > 1 else "grafos_teste/ponderado_9.txt"
    classe = GrafoMatriz if len(sys.argv) > 2 and sys.argv[2] == "matriz" else GrafoLista
    g = classe.ler_arquivo(arquivo)
    print(g.cabecalho())
    print()
    if g.direcionado:
        sys.exit("Arvore geradora minima exige grafo nao direcionado")
    for nome, algoritmo in ALGORITMOS.items():
        executar(g, algoritmo, nome)
        print()
