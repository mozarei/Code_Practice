"""A tiny text classifier using hand-written features and logistic regression."""
import math


def features(text):
    markers = ("ignore", "secret", "credential", "bypass", "exfiltrate", "override")
    words = text.lower().split()
    hits = sum(any(marker in word for marker in markers) for word in words)
    return [1.0, min(len(text) / 200.0, 1.0), hits / 4.0]


def initialize_weights(n_features):
    return [0.0] * n_features


def sigmoid(value):
    if value >= 0:
        return 1.0 / (1.0 + math.exp(-value))
    exp_value = math.exp(value)
    return exp_value / (1.0 + exp_value)


def predict(vector, weights):
    if len(vector) != len(weights):
        raise ValueError(f"Feature/parameter contract: {len(vector)} features, {len(weights)} weights")
    return sigmoid(sum(value * weight for value, weight in zip(vector, weights)))


def loss(data, weights):
    total = 0.0
    for vector, label in data:
        probability = min(max(predict(vector, weights), 1e-12), 1.0 - 1e-12)
        total -= label * math.log(probability) + (1 - label) * math.log(1 - probability)
    return total / len(data)


def gradient(data, weights):
    result = [0.0] * len(weights)
    for vector, label in data:
        error = predict(vector, weights) - label
        for i, value in enumerate(vector):
            result[i] += error * value / len(data)
    return result
