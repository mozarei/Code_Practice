"""CPU-only training. All printed losses are training losses."""
import argparse
import json
import math
from pathlib import Path
from data import load_data
from model import initialize_weights, loss, gradient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--learning-rate", type=float, default=0.3)
    args = parser.parse_args()
    if args.steps < 1 or not math.isfinite(args.learning_rate) or args.learning_rate <= 0:
        parser.error("Steps and learning rate must be positive and finite")
    data = load_data(args.csv)
    weights = initialize_weights(len(data[0][0]))
    before = weights.copy()
    initial = loss(data, weights)
    for step in range(args.steps):
        updates = gradient(data, weights)
        for i in range(len(weights)):
            weights[i] -= args.learning_rate * updates[i]
    final = loss(data, weights)
    if weights == before:
        raise AssertionError("No model parameters changed")
    if not math.isfinite(final) or final >= initial:
        raise AssertionError(f"Training loss did not decrease: {initial:.6f} -> {final:.6f}")
    result = {"rows": len(data), "initial_loss": initial,
              "final_loss": final, "weights_changed": weights != before}
    print("METRICS " + json.dumps(result, sort_keys=True))
    print("Success: training behavior verified; this is not a held-out evaluation.")


if __name__ == "__main__":
    main()
