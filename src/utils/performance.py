import time
import matplotlib.pyplot as plt

from utils.io_utils import genereaza_matrice_aleatorie
from utils.backtracking import rezolva_tsp_backtracking
from utils.nearest_neighbor import rezolva_tsp_nn_multistart
from utils.nn_aima import rezolva_tsp_nn_aima_multistart


def ruleaza_experiment(dimensiuni, seed=42, timp_bt=2.0):
    """Ruleaza experimente pe mai multe dimensiuni de problema.

    Args:
        dimensiuni (list[int]): Lista dimensiunilor N.
        seed (int): Seed de baza.
        timp_bt (float): Limita de timp pentru BT.

    Returns:
        dict: Rezultate agregate pentru grafice.
    """
    rezultate = {
        "N": [],
        "BT": [],
        "NN": [],
        "NN_AIMA": [],
        "COST_BT": [],
        "COST_NN": [],
        "COST_NN_AIMA": [],
    }

    for idx, n in enumerate(dimensiuni):
        matrice = genereaza_matrice_aleatorie(n, seed=seed + idx)

        t0 = time.perf_counter()
        _, cost_bt, _, _ = rezolva_tsp_backtracking(
            n, matrice, mod="timp", timp_max=timp_bt
        )
        timp_bt_real = time.perf_counter() - t0

        t1 = time.perf_counter()
        _, cost_nn, _ = rezolva_tsp_nn_multistart(n, matrice)
        timp_nn = time.perf_counter() - t1

        t2 = time.perf_counter()
        _, cost_aima, _ = rezolva_tsp_nn_aima_multistart(n, matrice)
        timp_aima = time.perf_counter() - t2

        rezultate["N"].append(n)
        rezultate["BT"].append(timp_bt_real)
        rezultate["NN"].append(timp_nn)
        rezultate["NN_AIMA"].append(timp_aima)
        rezultate["COST_BT"].append(cost_bt)
        rezultate["COST_NN"].append(cost_nn)
        rezultate["COST_NN_AIMA"].append(cost_aima)

    return rezultate


def genereaza_grafice(rezultate):
    """Genereaza graficele de performanta.

    Args:
        rezultate (dict): Dictionar intors de ruleaza_experiment().
    """
    n_values = rezultate["N"]

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, rezultate["BT"], marker="o", label="Backtracking")
    plt.plot(n_values, rezultate["NN"], marker="o", label="Nearest Neighbor")
    plt.plot(n_values, rezultate["NN_AIMA"], marker="o", label="NN AIMA")
    plt.xlabel("Numar de orase (N)")
    plt.ylabel("Timp executie (s)")
    plt.title("Comparatie timp executie")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, rezultate["COST_BT"], marker="o", label="Cost BT")
    plt.plot(n_values, rezultate["COST_NN"], marker="o", label="Cost NN")
    plt.plot(n_values, rezultate["COST_NN_AIMA"], marker="o", label="Cost NN AIMA")
    plt.xlabel("Numar de orase (N)")
    plt.ylabel("Cost traseu")
    plt.title("Comparatie costuri")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()