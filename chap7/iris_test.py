import csv
from typing import List, Dict
from chap7.util import normalize_by_feature_scaling
from chap7.network import Network
from random import shuffle
from enum import Enum


class IrisSpecies(Enum):
    SETOSA = "Iris-setosa"
    VERSICOLOR = "Iris-versicolor"
    VIRGINICA = "Iris-virginica"


species_weights: Dict[str, List[float]] = {
    IrisSpecies.SETOSA: [1.0, 0.0, 0.0],
    IrisSpecies.VERSICOLOR: [0.0, 1.0, 0.0],
    IrisSpecies.VIRGINICA: [0.0, 0.0, 1.0],
}


def iris_interpret_output(output: List[float]) -> str:
    if max(output) == output[0]:
        return IrisSpecies.SETOSA.value
    elif max(output) == output[1]:
        return IrisSpecies.VERSICOLOR.value
    else:
        return IrisSpecies.VIRGINICA.value


if __name__ == "__main__":
    # 前処理
    iris_params: List[List[float]] = []
    iris_classifications: List[List[float]] = []
    iris_species: List[str] = []
    with open("iris.csv", mode="r", newline="") as f:
        irises: List[List[str]] = list(csv.reader(f))
        shuffle(irises)
        for iris in irises:
            iris_params.append([float(n) for n in iris[0:4]])
            iris_classifications.append(species_weights[IrisSpecies(iris[4])])
            iris_species.append(iris[4])
    normalize_by_feature_scaling(iris_params)

    # ニューラルネットワーク
    iris_network: Network = Network([4, 6, 6, 6, 3], 0.4)

    # 訓練
    iris_trainers: List[List[float]] = iris_params[0:140]
    iris_trainers_corrects: List[List[float]] = iris_classifications[0:140]
    for _ in range(100):
        iris_network.train(iris_trainers, iris_trainers_corrects)

    # テスト
    iris_testers = iris_params[140:]
    iris_testers_corrects = iris_species[140:]
    iris_results = iris_network.validate(
        iris_testers, iris_testers_corrects, iris_interpret_output
    )
    print(f"{iris_results[0]} correct of {iris_results[1]} = {iris_results[2] * 100}%")
