from __future__ import annotations
from typing import List, Callable, Optional
from random import random
from chap7.neuron import Neuron
from chap7.util import dot_product


class Layer:
    def __init__(
        self,
        previous_layer: Optional[Layer],
        num_neurons: int,
        learning_rate: float,
        activation_function: Callable[[float], float],
        derivative_activation_function: Callable[[float], float],
    ) -> None:
        self.previous_layer: Optional[Layer] = previous_layer
        random_weights: List[float] = [
            random() for _ in previous_layer.neurons
        ] if previous_layer else []
        self.neurons: List[Neuron] = [
            Neuron(
                random_weights,
                learning_rate,
                activation_function,
                derivative_activation_function,
            )
            for _ in range(num_neurons)
        ]
        self.output_cache: List[float] = [0.0 for _ in range(num_neurons)]

    def outputs(self, inputs: List[float]) -> List[float]:
        if not self.previous_layer:
            self.output_cache = inputs
        else:
            self.output_cache = [n.output(inputs) for n in self.neurons]
        return self.output_cache

    def calculate_deltas_for_output_layer(self, expected: List[float]) -> None:
        for index, neuron in enumerate(self.neurons):
            neuron.delta = neuron.derivative_activation_function(
                neuron.output_cache
            ) * (expected[index] - self.output_cache[index])

    def calculate_deltas_for_hidden_layer(self, next_layer: Layer) -> None:
        for index, neuron in enumerate(self.neurons):
            next_weights: List[float] = [n.weights[index] for n in next_layer.neurons]
            next_deltas: List[float] = [n.delta for n in next_layer.neurons]
            neuron.delta = neuron.derivative_activation_function(
                neuron.output_cache
            ) * dot_product(next_weights, next_deltas)
