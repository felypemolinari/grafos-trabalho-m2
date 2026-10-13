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

print("OK")
