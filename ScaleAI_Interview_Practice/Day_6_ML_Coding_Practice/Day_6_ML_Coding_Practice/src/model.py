from contextlib import nullcontext
import torch
from torch import nn
from transformers import AutoModelForSequenceClassification
class TicketClassifier(nn.Module):
    def __init__(self,checkpoint):
        super().__init__()
        self.backbone=AutoModelForSequenceClassification.from_pretrained(checkpoint,local_files_only=True)
    def forward(self,input_ids,attention_mask=None,token_type_ids=None):
        with torch.no_grad():
            encoded=self.backbone.bert(input_ids=input_ids,attention_mask=attention_mask,
                                       token_type_ids=token_type_ids,return_dict=True)
        pooled=self.backbone.dropout(encoded.pooler_output)
        return self.backbone.classifier(pooled)
