import heapq
import time
from itertools import product

from grafo import GrafoLista


class Cronometro:
    def __enter__(self):
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, *_):
        self.segundos = time.perf_counter() - self.inicio


def _adjacencias(grafo):
    return {v: {d for d, _ in grafo.vizinhos(v) if d != v} for v in grafo.vertices}


def _menor_cor_livre(cores_vizinhos):
    cor = 0
    while cor in cores_vizinhos:
        cor += 1
    return cor


def coloracao_valida(grafo, cores):
    adj = _adjacencias(grafo)
    return all(v in cores for v in grafo.vertices) and all(
        cores[v] != cores[u] for v in grafo.vertices for u in adj[v]
    )


def forca_bruta(grafo):
    vertices = grafo.vertices
    if not vertices:
        return {}
    indice = {v: i for i, v in enumerate(vertices)}
    arestas = {
        (indice[v], indice[u])
        for v, viz in _adjacencias(grafo).items()
        for u in viz
        if indice[v] < indice[u]
    }
    if not arestas:
        return {v: 0 for v in vertices}

    k = 2
    while True:
        for combinacao in product(range(k), repeat=len(vertices)):
            if all(combinacao[a] != combinacao[b] for a, b in arestas):
                return dict(zip(vertices, combinacao))
        k += 1


def sem_criterio(grafo):
    adj = _adjacencias(grafo)
    cores = {}
    for v in grafo.vertices:
        cores[v] = _menor_cor_livre({cores[u] for u in adj[v] if u in cores})
    return cores


def welsh_powell(grafo):
    adj = _adjacencias(grafo)
    ordem = sorted(grafo.vertices, key=lambda v: len(adj[v]), reverse=True)
    cores = {}
    cor = 0
    while len(cores) < len(ordem):
        usados_na_cor = set()
        for v in ordem:
            if v not in cores and not (adj[v] & usados_na_cor):
                cores[v] = cor
                usados_na_cor.add(v)
        cor += 1
    return cores


def dsatur(grafo):
    adj = _adjacencias(grafo)
    cores = {}
    cores_vizinhas = {v: set() for v in grafo.vertices}
    fila = [(0, -len(adj[v]), v) for v in grafo.vertices]
    heapq.heapify(fila)
    while fila:
        sat, _, v = heapq.heappop(fila)
        if v in cores or -sat != len(cores_vizinhas[v]):
            continue
        cor = _menor_cor_livre(cores_vizinhas[v])
        cores[v] = cor
        for u in adj[v]:
            if u not in cores and cor not in cores_vizinhas[u]:
                cores_vizinhas[u].add(cor)
                heapq.heappush(fila, (-len(cores_vizinhas[u]), -len(adj[u]), u))
    return cores


ALGORITMOS = {
    "Forca bruta": forca_bruta,
    "Sem criterio de ordem": sem_criterio,
    "Welsh Powell": welsh_powell,
    "DSATUR": dsatur,
}


def executar(grafo, algoritmo, nome):
    with Cronometro() as c:
        cores = algoritmo(grafo)
    num_cores = len(set(cores.values()))
    print(f"{nome}:")
    print(f"  Tempo de execucao: {c.segundos:.6f} s")
    print(f"  Numero de cores: {num_cores}")
    if grafo.num_vertices < 10:
        for v in grafo.vertices:
            print(f"    vertice {v}: cor {cores[v]}")
    if not coloracao_valida(grafo, cores):
        print("  ATENCAO: coloracao invalida!")
    return cores


if __name__ == "__main__":
    import sys

    arquivo = sys.argv[1] if len(sys.argv) > 1 else "grafo.txt"
    limite_forca_bruta = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    g = GrafoLista.ler_arquivo(arquivo)
    print(g.cabecalho())
    print()
    for nome, algoritmo in ALGORITMOS.items():
        if algoritmo is forca_bruta and g.num_vertices > limite_forca_bruta:
            print(f"{nome}: ignorado ({g.num_vertices} vertices > limite {limite_forca_bruta})")
            print()
            continue
        executar(g, algoritmo, nome)
        print()
