# Mock hints - second level
Stage 1: A tensor may have the right values and dtype but the wrong argument name.
Stage 2: A dimension-removing operation can behave differently when B=1.
Stage 3: All parameters are in the optimizer. Check whether the encoder's
forward operations are actually recorded by autograd.
