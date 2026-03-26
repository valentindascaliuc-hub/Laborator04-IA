import time


def rezolva_tsp_nn(n, matrice, start=0):
    """Rezolva TSP prin euristica nearest neighbor.

    Args:
        n (int): Numarul de orase.
        matrice (list[list[int]]): Matricea distantelor.
        start (int): Orasul de start.

    Returns:
        tuple: (traseu, cost)
    """
    vizitat = [False] * n
    vizitat[start] = True

    traseu = [start]
    cost = 0
    curent = start

    for _ in range(n - 1):
        vecin = None
        dist_min = float("inf")

        for j in range(n):
            if not vizitat[j] and matrice[curent][j] < dist_min:
                dist_min = matrice[curent][j]
                vecin = j

        traseu.append(vecin)
        vizitat[vecin] = True
        cost += dist_min
        curent = vecin

    traseu.append(start)
    cost += matrice[curent][start]

    return traseu, cost


def rezolva_tsp_nn_multistart(n, matrice):
    """Ruleaza NN din toate starturile si pastreaza cel mai bun rezultat.

    Args:
        n (int): Numarul de orase.
        matrice (list[list[int]]): Matricea distantelor.

    Returns:
        tuple: (best_traseu, best_cost, rezultate_starturi)
    """
    rezultate = []
    best_traseu = None
    best_cost = float("inf")

    for start in range(n):
        traseu, cost = rezolva_tsp_nn(n, matrice, start=start)
        rezultate.append((start, traseu, cost))

        if cost < best_cost:
            best_cost = cost
            best_traseu = traseu

    return best_traseu, best_cost, rezultate


def rezolva_tsp_nn_timp(n, matrice, timp_max):
    """Ruleaza NN repetat pana la expirarea timpului.

    Args:
        n (int): Numarul de orase.
        matrice (list[list[int]]): Matricea distantelor.
        timp_max (float): Timp maxim in secunde.

    Returns:
        tuple: (best_traseu, best_cost, nr_rulari, timp_executie)
    """
    start_time = time.perf_counter()

    best_traseu = None
    best_cost = float("inf")
    nr_rulari = 0
    idx_start = 0

    while True:
        acum = time.perf_counter()
        if acum - start_time >= timp_max:
            break

        traseu, cost = rezolva_tsp_nn(n, matrice, start=idx_start)
        nr_rulari += 1

        if cost < best_cost:
            best_cost = cost
            best_traseu = traseu

        idx_start = (idx_start + 1) % n

    timp_executie = time.perf_counter() - start_time
    return best_traseu, best_cost, nr_rulari, timp_executie