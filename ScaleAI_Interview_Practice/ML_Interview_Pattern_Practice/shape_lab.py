"""Readable, working real-BERT shape/state example; no intentional bugs."""
import argparse,json
from pathlib import Path
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer,AutoModelForSequenceClassification
ROOT=Path(__file__).resolve().parent
def show(name,tensor):
    print(f'{name:24} shape={str(tuple(tensor.shape)):15} dtype={str(tensor.dtype):13} requires_grad={tensor.requires_grad}')
def main():
    p=argparse.ArgumentParser();p.add_argument('--pdb',action='store_true');p.add_argument('--report',type=Path,default=ROOT/'output/shape_report.json');a=p.parse_args()
    torch.manual_seed(31);torch.set_num_threads(2)
    path=ROOT/'models/bert-tiny'
    tokenizer=AutoTokenizer.from_pretrained(path,local_files_only=True)
    model=AutoModelForSequenceClassification.from_pretrained(path,local_files_only=True).eval()
    # eval disables dropout here, but does NOT disable gradients or freeze weights.
    texts=['Hello world.','This example contains a few more words.']
    inputs=tokenizer(texts,padding=True,truncation=True,max_length=64,return_tensors='pt')
    labels=torch.tensor([0,1],dtype=torch.long)
    print('Original text count:',len(texts))
    print('Token counts before padding:',inputs['attention_mask'].sum(1).tolist())
    for name,tensor in inputs.items():show(name,tensor)
    print('First token sequence:',tokenizer.convert_ids_to_tokens(inputs['input_ids'][0].tolist()))
    lookup=model.bert.embeddings.word_embeddings(inputs['input_ids'])
    combined=model.bert.embeddings(input_ids=inputs['input_ids'],token_type_ids=inputs.get('token_type_ids'))
    show('word lookup',lookup);show('combined embeddings',combined)
    encoded=model.bert(**inputs,return_dict=True)
    show('last_hidden_state',encoded.last_hidden_state)
    pooled=encoded.pooler_output;show('pooler_output',pooled)
    dropped=model.dropout(pooled);show('dropout output',dropped)
    logits=model.classifier(dropped);show('classifier.weight',model.classifier.weight)
    show('classifier.bias',model.classifier.bias);show('logits',logits);show('labels',labels)
    loss=F.cross_entropy(logits,labels);show('loss',loss)
    probabilities=logits.softmax(-1);predictions=logits.argmax(-1)
    show('probabilities',probabilities);show('predicted classes',predictions)
    print('Cross-entropy above used RAW logits, not the displayed probabilities.')
    with torch.no_grad():assert torch.allclose(logits.detach(),model(**inputs).logits,rtol=1e-5,atol=1e-6)
    optimizer=torch.optim.AdamW(model.parameters(),lr=1e-4)
    optimizer.zero_grad(set_to_none=True)
    before=model.classifier.weight.detach().clone()
    print('Before backward: classifier.grad =',model.classifier.weight.grad)
    if a.pdb:breakpoint()  # inputs, encoded, pooled, logits, labels, loss, model exist here.
    loss.backward();show('classifier.weight.grad',model.classifier.weight.grad)
    print('After backward, weight unchanged:',torch.equal(before,model.classifier.weight.detach()))
    optimizer.step()
    print('After step, max weight change:',(model.classifier.weight.detach()-before).abs().max().item())
    # B=1: retain the batch dimension in labels. A scalar loss is intentional.
    one=tokenizer([texts[0]],return_tensors='pt')
    one_logits=model(**one).logits;one_labels=labels[:1]
    show('B=1 logits',one_logits);show('B=1 labels',one_labels)
    show('B=1 loss',F.cross_entropy(one_logits,one_labels))
    column=one_labels.unsqueeze(-1)
    print('[1,1].squeeze() ->',tuple(column.squeeze().shape))
    print('[1,1].squeeze(-1) ->',tuple(column.squeeze(-1).shape))
    detached=model.classifier.weight.detach()
    independent=model.classifier.weight.detach().clone()
    print('detach shares storage:',detached.data_ptr()==model.classifier.weight.data_ptr())
    print('detach+clone shares storage:',independent.data_ptr()==model.classifier.weight.data_ptr())
    report={'B':len(texts),'L':inputs['input_ids'].shape[1],'H':model.config.hidden_size,'C':model.config.num_labels,
            'V':model.config.vocab_size,'token_counts':inputs['attention_mask'].sum(1).tolist(),
            'shapes':{'input_ids':list(inputs['input_ids'].shape),'last_hidden_state':list(encoded.last_hidden_state.shape),
                      'pooler_output':list(pooled.shape),'classifier_weight':list(model.classifier.weight.shape),
                      'logits':list(logits.shape),'labels':list(labels.shape),'loss':list(loss.shape)}}
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n')
    print('SHAPE_LAB_COMPLETE')
if __name__=='__main__':main()
