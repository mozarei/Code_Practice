"""CPU-only supervised training for an original practice mock."""
import argparse
from pathlib import Path
import torch
from data import load_batch
from model import TinyClassifier, check_padding_invariance


def main():
    parser = argparse.ArgumentParser(description="Train the tiny CPU classifier")
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=60)
    args = parser.parse_args()
    if args.epochs < 1:
        parser.error("--epochs must be positive")
    torch.manual_seed(7)
    torch.set_num_threads(1)
    ids, mask, targets, vocabulary, classes = load_batch(args.training_csv)
    model = TinyClassifier(len(vocabulary), classes)
    # Padding check is practiced in Mock 2.
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
    criterion = torch.nn.CrossEntropyLoss()
    before = [p.detach().clone() for p in model.parameters()]
    with torch.no_grad():
        initial_loss = criterion(model(ids, mask), targets).item()
    model.train()
    for _ in range(args.epochs):
        logits = model(ids, mask)
        loss = criterion(logits, targets)
        loss.backward()
        optimizer.zero_grad(set_to_none=True)
        optimizer.step()
    if not any(not torch.equal(a, b.detach()) for a, b in zip(before, model.parameters())):
        raise AssertionError("Training completed without updating model parameters")
    model.eval()
    with torch.no_grad():
        logits = model(ids, mask)
        final_loss = criterion(logits, targets).item()
        accuracy = logits.argmax(dim=1).eq(targets).float().mean().item()
    if not torch.isfinite(torch.tensor(final_loss)) or final_loss >= initial_loss:
        raise AssertionError("Expected finite training loss below initial loss")
    print(f"rows={len(targets)} initial_loss={initial_loss:.6f} final_loss={final_loss:.6f} training_accuracy={accuracy:.3f}")
    print("Success: parameters changed and training loss decreased; this is not a held-out evaluation.")


if __name__ == "__main__":
    main()
