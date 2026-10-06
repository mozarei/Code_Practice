from torch import nn
from transformers import AutoModelForSequenceClassification


class TicketClassifier(nn.Module):
    def __init__(self, checkpoint):
        super().__init__()
        self.backbone = AutoModelForSequenceClassification.from_pretrained(
            checkpoint, local_files_only=True,
        )

    def forward(self, **inputs):
        outputs = self.backbone(**inputs)
        return outputs
