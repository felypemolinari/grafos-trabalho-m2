from grafo import GrafoLista, GrafoMatriz, busca_em_largura, busca_em_profundidade, dijkstra

for classe in (GrafoLista, GrafoMatriz):
    g = classe.ler_arquivo("grafo.txt")
    assert busca_em_largura(g, 0) == [0, 1, 2, 3, 4, 5], classe
    assert busca_em_profundidade(g, 0) == [0, 1, 3, 2, 4, 5], classe
    dist, cam = dijkstra(g, 0)
    assert dist == {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3}, classe
    assert cam[5] == [0, 1, 3, 5], classe

    g = classe.ler_arquivo("grafo_ponderado.txt")
    dist, cam = dijkstra(g, 0)
    assert dist == {0: 0, 1: 3, 2: 1, 3: 4, 4: 7}, classe
    assert cam[4] == [0, 2, 1, 3, 4], classe
    assert dijkstra(g, 4)[0][0] == float("inf"), classe

gl, gm = GrafoLista.ler_arquivo("grafo_ponderado.txt"), GrafoMatriz.ler_arquivo("grafo_ponderado.txt")
for v in gl.vertices:
    assert gl.vizinhos(v) == gm.vizinhos(v)
    assert dijkstra(gl, v) == dijkstra(gm, v)

for classe in (GrafoLista, GrafoMatriz):
    g = classe.ler_arquivo("grafo.txt")
    assert g.contem_aresta(0, 1) and g.contem_aresta(1, 0), classe
    assert not g.contem_aresta(0, 3), classe
    assert not g.contem_aresta(0, 99), classe

    g = classe.ler_arquivo("grafo_ponderado.txt")
    assert g.contem_aresta(2, 1), classe
    assert not g.contem_aresta(1, 2), classe
    assert not g.contem_aresta(4, 0), classe

for arquivo in ("grafo.txt", "grafo_ponderado.txt"):
    gl, gm = GrafoLista.ler_arquivo(arquivo), GrafoMatriz.ler_arquivo(arquivo)
    for u in gl.vertices:
        for v in gl.vertices:
            assert gl.contem_aresta(u, v) == gm.contem_aresta(u, v), (arquivo, u, v)

import random
from coloracao import ALGORITMOS, coloracao_valida, forca_bruta


def montar(n, arestas):
    g = GrafoLista(n)
    for u, v in arestas:
        g.adicionar_aresta(u, v)
    return g


def num_cores(cores):
    return len(set(cores.values()))


casos = [
    (GrafoLista.ler_arquivo("grafo.txt"), 2),
    (montar(3, [(0, 1), (1, 2), (2, 0)]), 3),
    (montar(5, [(i, (i + 1) % 5) for i in range(5)]), 3),
    (montar(4, [(u, v) for u in range(4) for v in range(u + 1, 4)]), 4),
    (montar(4, []), 1),
]
for g, esperado in casos:
    assert num_cores(forca_bruta(g)) == esperado, esperado
    for nome, algoritmo in ALGORITMOS.items():
        assert coloracao_valida(g, algoritmo(g)), nome

random.seed(42)
for _ in range(30):
    n = random.randint(2, 8)
    g = montar(n, [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.4])
    otimo = num_cores(forca_bruta(g))
    for nome, algoritmo in ALGORITMOS.items():
        cores = algoritmo(g)
        assert coloracao_valida(g, cores), nome
        assert num_cores(cores) >= otimo, nome

g = montar(3000, [(random.randrange(3000), random.randrange(3000)) for _ in range(20000)])
for nome in ("Sem criterio de ordem", "Welsh Powell", "DSATUR"):
    assert coloracao_valida(g, ALGORITMOS[nome](g)), nome

from itertools import combinations
from agm import kruskal, prim, soma


def montar_ponderado(n, arestas):
    g = GrafoLista(n, ponderado=True)
    for u, v, p in arestas:
        g.adicionar_aresta(u, v, p)
    return g


def agm_forca_bruta(g):
    arestas = [(u, v, p) for u in g.vertices for v, p in g.vizinhos(u) if u < v]
    melhor = float("inf")
    for escolha in combinations(arestas, g.num_vertices - 1):
        if len(kruskal(montar_ponderado(g.num_vertices, escolha))) == g.num_vertices - 1:
            melhor = min(melhor, soma(escolha))
    return melhor


for classe in (GrafoLista, GrafoMatriz):
    g = classe.ler_arquivo("grafos_teste/ponderado_9.txt")
    assert soma(prim(g)) == soma(kruskal(g)) == 37, classe
    assert len(prim(g)) == len(kruskal(g)) == 8, classe

desconexo = montar_ponderado(5, [(0, 1, 3), (1, 2, 1), (0, 2, 2), (3, 4, 5)])
assert soma(prim(desconexo)) == soma(kruskal(desconexo)) == 8
assert len(prim(desconexo)) == len(kruskal(desconexo)) == 3

for _ in range(30):
    n = random.randint(2, 7)
    arestas = [(i, random.randrange(i), random.randint(1, 9)) for i in range(1, n)]
    arestas += [(u, v, random.randint(1, 9)) for u in range(n) for v in range(u + 2, n) if random.random() < 0.4]
    g = montar_ponderado(n, arestas)
    esperado = agm_forca_bruta(g)
    assert soma(prim(g)) == soma(kruskal(g)) == esperado

g = GrafoLista.ler_arquivo("grafos_teste/ponderado_5000.txt")
assert soma(prim(g)) == soma(kruskal(g)) and len(prim(g)) == 4999

print("OK")
