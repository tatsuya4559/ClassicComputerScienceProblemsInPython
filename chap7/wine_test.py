from chap7.util import normalize_by_feature_scaling
from chap7.network import Network
from random import shuffle
import csv


def wine_interpret_output(output):
    if max(output) == output[0]:
        return 1
    elif max(output) == output[1]:
        return 2
    else:
        return 3


if __name__ == "__main__":
    wine_params = []
    wine_classifications = []
    wine_species = []
    with open("wine.csv", mode="r", newline="") as f:
        wines = list(csv.reader(f, quoting=csv.QUOTE_NONNUMERIC))
        shuffle(wines)
        for wine in wines:
            params = [float(n) for n in wine[1:14]]
            wine_params.append(params)
            species = int(wine[0])
            if species == 1:
                wine_classifications.append([1.0, 0.0, 0.0])
            elif species == 2:
                wine_classifications.append([0.0, 1.0, 0.0])
            else:
                wine_classifications.append([0.0, 0.0, 1.0])
            wine_species.append(species)
    normalize_by_feature_scaling(wine_params)

    wine_network = Network([13, 7, 3], 0.9)

    wine_trainers = wine_params[0:150]
    wine_trainers_corrects = wine_classifications[0:150]
    for _ in range(100):
        wine_network.train(wine_trainers, wine_trainers_corrects)

    wine_testers = wine_params[150:]
    wine_testers_corrects = wine_species[150:]
    results = wine_network.validate(
        wine_testers, wine_testers_corrects, wine_interpret_output
    )
    print(f"{results[0]} corrects of {results[1]} = {results[2]*100}%")
