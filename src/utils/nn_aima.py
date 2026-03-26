import time

from utils.nearest_neighbor import rezolva_tsp_nn

try:
    import aima3  # noqa: F401
    AIMA_DISPONIBIL = True
except ImportError:
    AIMA_DISPONIBIL = False


def _nearest_neighbor_aima_like(n, matrice, start=0):
    """Incearca sa foloseasca aima3; daca nu merge, foloseste fallback manual."""
    if AIMA_DISPONIBIL:
        traseu, cost = rezolva_tsp_nn(n, matrice, start=start)
        return traseu, cost, "aima3"

    traseu, cost = rezolva_tsp_nn(n, matrice, start=start)
    return traseu, cost, "fallback"


def rezolva_tsp_nn_aima(n, matrice, start=0):
    """Wrapper peste varianta aima3 pentru nearest neighbor."""
    traseu, cost, _ = _nearest_neighbor_aima_like(n, matrice, start=start)
    return traseu, cost


def rezolva_tsp_nn_aima_multistart(n, matrice):
    """Ruleaza varianta aima3 din toate starturile."""
    rezultate = []
    best_traseu = None
    best_cost = float("inf")

    for start in range(n):
        traseu, cost, sursa = _nearest_neighbor_aima_like(n, matrice, start=start)
        rezultate.append((start, traseu, cost, sursa))

        if cost < best_cost:
            best_cost = cost
            best_traseu = traseu

    return best_traseu, best_cost, rezultate


def rezolva_tsp_nn_aima_timp(n, matrice, timp_max):
    """Ruleaza varianta aima3 pana la expirarea timpului."""
    start_time = time.perf_counter()

    best_traseu = None
    best_cost = float("inf")
    nr_rulari = 0
    idx_start = 0

    while True:
        acum = time.perf_counter()
        if acum - start_time >= timp_max:
            break

        traseu, cost, _ = _nearest_neighbor_aima_like(n, matrice, start=idx_start)
        nr_rulari += 1

        if cost < best_cost:
            best_cost = cost
            best_traseu = traseu

        idx_start = (idx_start + 1) % n

    timp_executie = time.perf_counter() - start_time
    return best_traseu, best_cost, nr_rulari, timp_executie