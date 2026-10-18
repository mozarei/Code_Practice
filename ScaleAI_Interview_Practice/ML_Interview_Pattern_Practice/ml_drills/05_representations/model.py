from torch import nn
from transformers import AutoModelForSequenceClassification
class Classifier(nn.Module):
    def __init__(self,checkpoint):
        super().__init__()
        self.backbone=AutoModelForSequenceClassification.from_pretrained(checkpoint,local_files_only=True)
    def forward(self,**inputs):
        encoded=self.backbone.bert(**inputs,return_dict=True)
        features=encoded.last_hidden_state.mean(dim=-1)
        return self.backbone.classifier(self.backbone.dropout(features))
