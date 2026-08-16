#!/usr/bin/ env python3
import importlib
from types import ModuleType


def checking_dep() -> tuple[bool, list[ModuleType]]:
    liste: dict = [("pandas", "Data manipulation ready"),
                   ("numpy", "Numerical computation ready"),
                   ("matplotlib", "Visualization ready")]
    ready: bool = True
    res: list[ModuleType] = []
    for key, value in liste:
        try:
            res.append(importlib.import_module(key))
            print(f"[OK] {key} ({key.__version__}) - {value}")
        except ModuleNotFoundError as error:
            if error.name == key:
                print(f" Missing dependency for {key} :")
            else:
                print(f"[ERROR] {key} - Broken (Missing: {error.name})")
            ready = False
        except BaseException as error:
            print(f"[ERROR] : {error}")
            ready = False
    return ready, res


def main():
    print()
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")
    valide, [pd, np, matplotlib] = checking_dep()

    if not valide:
        print("\n === instruction for installation of pip or Poetry === ")
        print("\n To install using PIP, run:")
        print(" pip install requirements.txt")
        print("\n To install using POETRY, run:")
        print(" poetry install")
    else:
        print("\nAnalyzing Matrix data...")
        print("Processing 1000 data points")
        import matplotlib.pyplot as pl
        import numpy
        import pandas

        matrix_content = numpy.random.rand(1000, 1)
        matrix_generate = pandas.DataFrame(matrix_content)
        pl.plot(matrix_generate)
        pl.savefig("matrix_analysis.png")
        print("Generating visualization...")
        print("\nAnalysis complete!")
        print("Results saved to: matrix_analysis.png")
