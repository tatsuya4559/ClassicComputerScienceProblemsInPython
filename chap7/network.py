from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from chap7.layer import Layer
from chap7.util import sigmoid, derivative_sigmoid

T = TypeVar("T")


class Network:
    def __init__(
        self,
        layer_structure: List[int],
        learning_rate: float,
        activation_function: Callable[[float], float] = sigmoid,
        derivative_activation_function: Callable[[float], float] = derivative_sigmoid,
    ) -> None:
        if len(layer_structure) < 3:
            raise ValueError("Error: Network should have 3 layers at least.")
        self.layers: List[Layer] = []
        input_layer: Layer = Layer(
            None,
            layer_structure[0],
            learning_rate,
            activation_function,
            derivative_activation_function,
        )
        self.layers.append(input_layer)
        for previous, num_neurons in enumerate(layer_structure[1:]):
            next_layer = Layer(
                self.layers[previous],
                num_neurons,
                learning_rate,
                activation_function,
                derivative_activation_function,
            )
            self.layers.append(next_layer)

    def outputs(self, input_: List[float]) -> List[float]:
        value = input_
        for layer in self.layers:
            value = layer.outputs(value)
        return value

    def backpropagate(self, expected: List[float]) -> None:
        # 出力層
        self.layers[-1].calculate_deltas_for_output_layer(expected)
        # 隠れ層
        for l in range(len(self.layers) - 2, 0, -1):
            self.layers[l].calculate_deltas_for_hidden_layer(self.layers[l + 1])

    def update_weights(self) -> None:
        for layer in self.layers[1:]:
            for neuron in layer.neurons:
                for i, w in enumerate(neuron.weights):
                    w = w + (
                        neuron.learning_rate
                        * layer.previous_layer.output_cache[i]
                        * neuron.delta
                    )

    def train(self, inputs: List[List[float]], expecteds: List[List[float]]) -> None:
        for input_, expected in zip(inputs, expecteds):
            self.outputs(input_)
            self.backpropagate(expected)
            self.update_weights()

    def validate(
        self,
        inputs: List[List[float]],
        expecteds: List[T],
        interpret_output: Callable[[List[float]], T],
    ) -> Tuple[int, int, float]:
        correct: int = 0
        for input_, expected in zip(inputs, expecteds):
            result: T = interpret_output(self.outputs(input_))
            if result == expected:
                correct += 1
        percentage: float = correct / len(inputs)
        return correct, len(inputs), percentage
