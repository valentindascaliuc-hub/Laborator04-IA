import random


def citeste_matrice(cale):
    """Citeste o matrice de distante din fisier text.

    Format acceptat:
        0 10 15
        10 0 20
        15 20 0

    Args:
        cale (str): Calea catre fisierul de intrare.

    Returns:
        list[list[int]]: Matricea de distante.

    Raises:
        FileNotFoundError: Daca fisierul nu exista.
        ValueError: Daca matricea este invalida.
    """
    with open(cale, "r", encoding="utf-8") as fisier:
        linii = [linie.strip() for linie in fisier if linie.strip()]

    matrice = [list(map(int, linie.split())) for linie in linii]

    if not matrice:
        raise ValueError("Fisierul este gol.")

    n = len(matrice)

    for linie in matrice:
        if len(linie) != n:
            raise ValueError("Matricea trebuie sa fie patratica.")

    for i in range(n):
        if matrice[i][i] != 0:
            raise ValueError("Elementele de pe diagonala principala trebuie sa fie 0.")
        for j in range(n):
            if matrice[i][j] < 0:
                raise ValueError("Distantele nu pot fi negative.")

    return matrice


def genereaza_matrice_aleatorie(n, seed=None, min_dist=1, max_dist=99):
    """Genereaza o matrice simetrica aleatorie de distante pentru TSP.

    Args:
        n (int): Numarul de orase.
        seed (int | None): Seed pentru reproductibilitate.
        min_dist (int): Distanta minima nenula.
        max_dist (int): Distanta maxima.

    Returns:
        list[list[int]]: Matrice simetrica n x n.

    Raises:
        ValueError: Daca n < 2.
    """
    if n < 2:
        raise ValueError("N trebuie sa fie cel putin 2.")

    rng = random.Random(seed)
    matrice = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            dist = rng.randint(min_dist, max_dist)
            matrice[i][j] = dist
            matrice[j][i] = dist

    return matrice


def scrie_matrice(cale, matrice):
    """Scrie o matrice in fisier text.

    Args:
        cale (str): Calea fisierului.
        matrice (list[list[int]]): Matricea de scris.
    """
    with open(cale, "w", encoding="utf-8") as fisier:
        for linie in matrice:
            fisier.write(" ".join(map(str, linie)) + "\n")


def calculeaza_cost_traseu(matrice, traseu):
    """Calculeaza costul unui traseu ciclic.

    Args:
        matrice (list[list[int]]): Matricea distantelor.
        traseu (list[int]): Traseul complet, inclusiv revenirea la start.

    Returns:
        int: Costul total al traseului.
    """
    cost = 0
    for i in range(len(traseu) - 1):
        cost += matrice[traseu[i]][traseu[i + 1]]
    return cost


def format_traseu(traseu):
    """Formateaza un traseu pentru afisare.

    Args:
        traseu (list[int]): Lista oraselor.

    Returns:
        str: Traseu formatat.
    """
    return " -> ".join(map(str, traseu))