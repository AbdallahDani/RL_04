from typing import Tuple, List
from math import log

rates = [
    [1, 0.23, 0.25, 16.43, 18.21, 4.94],
    [4.34, 1, 1.11, 71.40, 79.09, 21.44],
    [3.93, 0.90, 1, 64.52, 71.48, 19.37],
    [0.061, 0.014, 0.015, 1, 1.11, 0.30],
    [0.055, 0.013, 0.014, 0.90, 1, 0.27],
    [0.20, 0.047, 0.052, 3.33, 3.69, 1],
]

currencies = ('PLN', 'EUR', 'USD', 'RUB', 'INR', 'MXN')


def negate_logarithm_convertor(graph: Tuple[Tuple[float]]) -> List[List[float]]:
    ''' log de chaque taux dans le graphique et annulez-le'''
    result = [[-log(edge) for edge in row] for row in graph]
    return result


def arbitrage(currency_tuple: tuple, rates_matrix: Tuple[Tuple[float, ...]]):
    ''' Calcule les situations d'arbitrage et imprime le détail de ces calculs'''

    trans_graph = negate_logarithm_convertor(rates_matrix)

    # Choisissez n'importe quel sommet source - nous pouvons exécuter Bellman-Ford à partir de n'importe quel sommet et obtenir le bon résultat

    source = 0
    n = len(trans_graph)
    min_dist = [float('inf')] * n

    pre = [-1] * n

    min_dist[source] = source

    # 'Relax edges |V-1| times'
    for _ in range(n - 1):
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                    pre[dest_curr] = source_curr

    # si nous pouvons encore relâcher les bords, alors nous avons un cycle négatif
    for source_curr in range(n):
        for dest_curr in range(n):
            if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                # cycle négatif existe, et utilisez la chaîne prédécesseur pour imprimer le cycle
                print_cycle = [dest_curr, source_curr]
                # Commencez par la source et revenez en arrière jusqu'à ce que vous voyiez à nouveau le sommet source ou tout sommet qui existe déjà dans le tableau print_cycle
                while pre[source_curr] not in print_cycle:
                    print_cycle.append(pre[source_curr])
                    source_curr = pre[source_curr]
                print_cycle.append(pre[source_curr])
                print("Arbitrage Opportunity: \n")
                print(" --> ".join([currencies[p] for p in print_cycle[::-1]]))


if __name__ == "__main__":
    arbitrage(currencies, rates)

# Complexité temporelle : O(N^3)
# Complexité spatiale : O(N^2)