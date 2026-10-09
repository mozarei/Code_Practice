# Mock hints - final level before solution
Stage 1: Keep the tokenizer's standard input_ids key when forwarding to BERT.
Stage 2: The dataset already provides vector labels. Avoid unconditional squeeze().
Stage 3: Identify the context around the BERT encoder call. Does it disable gradients?
