import argparse
import os
import sys

from utils.backtracking import rezolva_tsp_backtracking
from utils.io_utils import citeste_matrice, format_traseu
from utils.nearest_neighbor import (
    rezolva_tsp_nn,
    rezolva_tsp_nn_multistart,
    rezolva_tsp_nn_timp,
)
from utils.nn_aima import (
    rezolva_tsp_nn_aima,
    rezolva_tsp_nn_aima_multistart,
    rezolva_tsp_nn_aima_timp,
)
from utils.performance import ruleaza_experiment, genereaza_grafice


def afiseaza_rezultat(titlu, n, traseu, cost, nr_solutii=None, timp_executie=None):
    """Afiseaza rezultatul final intr-un format clar.

    Args:
        titlu (str): Titlul sectiunii.
        n (int): Numarul de orase.
        traseu (list[int] | None): Traseul gasit.
        cost (int | float): Costul traseului.
        nr_solutii (int | None): Numarul de solutii gasite.
        timp_executie (float | None): Timp executie in secunde.
    """
    print(f"\n=== {titlu} ===")
    print(f"N: {n}")
    print(f"Traseu: {format_traseu(traseu) if traseu else 'N/A'}")
    print(f"Cost: {cost if cost != float('inf') else 'inf'}")

    if nr_solutii is not None:
        print(f"Numar solutii: {nr_solutii}")

    if timp_executie is not None:
        print(f"Timp executie: {timp_executie:.6f} sec")


def construieste_parser():
    """Construieste parserul de argumente.

    Returns:
        argparse.ArgumentParser: Parser configurat.
    """
    parser = argparse.ArgumentParser(
        description="Tema IA - TSP cu backtracking, NN si NN AIMA"
    )

    parser.add_argument(
        "fisier",
        nargs="?",
        help="Calea catre fisierul de intrare cu matricea distantelor."
    )

    parser.add_argument(
        "--algoritm",
        choices=["bt", "nn", "nn_aima"],
        default="bt",
        help="Algoritmul folosit."
    )

    parser.add_argument(
        "--mod",
        choices=["prima", "toate", "timp", "y_solutii"],
        default="toate",
        help="Modul de rulare."
    )

    parser.add_argument(
        "--timp",
        type=float,
        default=None,
        help="Limita de timp in secunde pentru modul 'timp'."
    )

    parser.add_argument(
        "--y",
        type=int,
        default=None,
        help="Numarul de solutii pentru modul 'y_solutii'."
    )

    parser.add_argument(
        "--grafice",
        action="store_true",
        help="Ruleaza experimente si afiseaza grafice de performanta."
    )

    return parser


def main():
    """Punctul de intrare in aplicatie."""
    parser = construieste_parser()
    args = parser.parse_args()

    if args.grafice:
        rezultate = ruleaza_experiment(dimensiuni=[4, 5, 6, 7, 8], timp_bt=1.0)
        genereaza_grafice(rezultate)
        return

    if not args.fisier:
        parser.error("Trebuie sa specifici fisierul de intrare sau sa folosesti --grafice.")

    if not os.path.exists(args.fisier):
        print(f"Fisier inexistent: {args.fisier}")
        sys.exit(1)

    matrice = citeste_matrice(args.fisier)
    n = len(matrice)

    if args.algoritm == "bt":
        traseu, cost, nr_solutii, timp_executie = rezolva_tsp_backtracking(
            n=n,
            matrice=matrice,
            mod=args.mod,
            timp_max=args.timp,
            y_max=args.y,
        )
        afiseaza_rezultat(
            titlu=f"Backtracking / mod={args.mod}",
            n=n,
            traseu=traseu,
            cost=cost,
            nr_solutii=nr_solutii,
            timp_executie=timp_executie,
        )

    elif args.algoritm == "nn":
        if args.mod == "prima":
            traseu, cost = rezolva_tsp_nn(n, matrice, start=0)
            afiseaza_rezultat(
                titlu="Nearest Neighbor (start=0)",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=1,
                timp_executie=None,
            )

        elif args.mod == "y_solutii":
            traseu, cost, rezultate = rezolva_tsp_nn_multistart(n, matrice)

            print("\n=== Nearest Neighbor Multistart ===")
            for start, traseu_start, cost_start in rezultate:
                print(f"Start {start}: {format_traseu(traseu_start)} (cost={cost_start})")

            afiseaza_rezultat(
                titlu="Nearest Neighbor - cel mai bun din toate starturile",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=len(rezultate),
                timp_executie=None,
            )

        elif args.mod == "timp":
            if args.timp is None:
                parser.error("Pentru --mod timp trebuie sa dai si --timp.")
            traseu, cost, nr_rulari, timp_executie = rezolva_tsp_nn_timp(n, matrice, args.timp)
            afiseaza_rezultat(
                titlu="Nearest Neighbor cu limita de timp",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=nr_rulari,
                timp_executie=timp_executie,
            )

        elif args.mod == "toate":
            traseu, cost, rezultate = rezolva_tsp_nn_multistart(n, matrice)
            afiseaza_rezultat(
                titlu="Nearest Neighbor 'toate' (asimilat multistart)",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=len(rezultate),
                timp_executie=None,
            )

    elif args.algoritm == "nn_aima":
        if args.mod == "prima":
            traseu, cost = rezolva_tsp_nn_aima(n, matrice, start=0)
            afiseaza_rezultat(
                titlu="Nearest Neighbor AIMA (start=0)",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=1,
                timp_executie=None,
            )

        elif args.mod == "y_solutii":
            traseu, cost, rezultate = rezolva_tsp_nn_aima_multistart(n, matrice)

            print("\n=== Nearest Neighbor AIMA Multistart ===")
            for start, traseu_start, cost_start, sursa in rezultate:
                print(
                    f"Start {start}: {format_traseu(traseu_start)} "
                    f"(cost={cost_start}, sursa={sursa})"
                )

            afiseaza_rezultat(
                titlu="Nearest Neighbor AIMA - cel mai bun din toate starturile",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=len(rezultate),
                timp_executie=None,
            )

        elif args.mod == "timp":
            if args.timp is None:
                parser.error("Pentru --mod timp trebuie sa dai si --timp.")
            traseu, cost, nr_rulari, timp_executie = rezolva_tsp_nn_aima_timp(
                n, matrice, args.timp
            )
            afiseaza_rezultat(
                titlu="Nearest Neighbor AIMA cu limita de timp",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=nr_rulari,
                timp_executie=timp_executie,
            )

        elif args.mod == "toate":
            traseu, cost, rezultate = rezolva_tsp_nn_aima_multistart(n, matrice)
            afiseaza_rezultat(
                titlu="Nearest Neighbor AIMA 'toate' (asimilat multistart)",
                n=n,
                traseu=traseu,
                cost=cost,
                nr_solutii=len(rezultate),
                timp_executie=None,
            )


if __name__ == "__main__":
    main()