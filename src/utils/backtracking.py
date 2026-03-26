import time


def rezolva_tsp_backtracking(n, matrice, mod="toate", timp_max=None, y_max=None):
    """Rezolva TSP prin backtracking cu moduri de oprire.

    Moduri:
        - prima
        - toate
        - timp
        - y_solutii

    Args:
        n (int): Numarul de orase.
        matrice (list[list[int]]): Matricea distantelor.
        mod (str): Modul de oprire.
        timp_max (float | None): Limita de timp in secunde pentru modul 'timp'.
        y_max (int | None): Numarul maxim de solutii pentru 'y_solutii'.

    Returns:
        tuple:
            (
                best_traseu,
                best_cost,
                nr_solutii,
                timp_executie
            )

    Raises:
        ValueError: Daca modul este invalid sau lipsesc argumente obligatorii.
    """
    if mod not in {"prima", "toate", "timp", "y_solutii"}:
        raise ValueError("Mod invalid. Foloseste: prima, toate, timp, y_solutii.")

    if mod == "timp" and (timp_max is None or timp_max <= 0):
        raise ValueError("Pentru modul 'timp' trebuie sa dai --timp > 0.")

    if mod == "y_solutii" and (y_max is None or y_max <= 0):
        raise ValueError("Pentru modul 'y_solutii' trebuie sa dai --y > 0.")

    start_time = time.perf_counter()

    vizitat = [False] * n
    vizitat[0] = True

    best_cost = float("inf")
    best_traseu = None
    nr_solutii = 0
    oprit = False

    def trebuie_oprit():
        if mod == "prima" and nr_solutii >= 1:
            return True
        if mod == "timp":
            return (time.perf_counter() - start_time) >= timp_max
        if mod == "y_solutii" and nr_solutii >= y_max:
            return True
        return False

    def backtrack(curent, path, cost_curent):
        nonlocal best_cost, best_traseu, nr_solutii, oprit

        if oprit:
            return

        if trebuie_oprit():
            oprit = True
            return

        if len(path) == n:
            cost_total = cost_curent + matrice[curent][0]
            traseu_final = path + [0]
            nr_solutii += 1

            if cost_total < best_cost:
                best_cost = cost_total
                best_traseu = traseu_final

            if trebuie_oprit():
                oprit = True
            return

        for urmator in range(n):
            if not vizitat[urmator] and urmator != curent:
                cost_nou = cost_curent + matrice[curent][urmator]

                if mod == "toate" and cost_nou >= best_cost:
                    continue

                vizitat[urmator] = True
                backtrack(urmator, path + [urmator], cost_nou)
                vizitat[urmator] = False

                if oprit:
                    return

    backtrack(0, [0], 0)

    timp_executie = time.perf_counter() - start_time

    return best_traseu, best_cost, nr_solutii, timp_executie