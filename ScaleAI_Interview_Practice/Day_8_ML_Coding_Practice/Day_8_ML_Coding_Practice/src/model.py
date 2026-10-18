from torch import nn
from transformers import AutoModelForSequenceClassification
class ReviewClassifier(nn.Module):
    def __init__(self,checkpoint):
        super().__init__()
        self.backbone=AutoModelForSequenceClassification.from_pretrained(
            checkpoint,local_files_only=True
            )
    
    def forward(self,input_ids,attention_mask=None,token_type_ids=None):
        encoded=self.backbone.bert(input_ids=input_ids,attention_mask=attention_mask,
                                   token_type_ids=token_type_ids,return_dict=True)
        # breakpoint()
        # features=encoded.last_hidden_state.mean(dim=-1)
        features = encoded.pooler_output
        return self.backbone.classifier(self.backbone.dropout(features))
