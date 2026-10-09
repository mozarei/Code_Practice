# Independent drill hints (read only the case you are working on)
| Case | Level 1 | Level 2 |
|---|---|---|
| 01 | Inspect model input contracts. | How does the embedding interpret indices? |
| 02 | Inspect the two loss arguments. | Is an extra target dimension present? |
| 03 | Inspect loss.requires_grad and grad_fn. | Was the loss disconnected before backward? |
| 04 | Separate trainability from optimizer inclusion. | Inspect backbone.requires_grad. |
| 05 | Gradients exist; inspect update ownership. | Compare optimizer parameter IDs with model parameter IDs. |
| 06 | Inspect gradients immediately before step. | Did anything clear them after backward? |
