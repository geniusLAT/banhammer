import torch
from transformers import BertTokenizer, BertForSequenceClassification


tokenizer = BertTokenizer.from_pretrained('s-nlp/russian_toxicity_classifier')
model = BertForSequenceClassification.from_pretrained('s-nlp/russian_toxicity_classifier')


model.eval()

def get_toxicity_probability(text):

    inputs = tokenizer.encode(text, return_tensors='pt')
    
    with torch.no_grad():  
        outputs = model(inputs)
    
    logits = outputs.logits
    
    probabilities = torch.nn.functional.softmax(logits, dim=1)
    
    toxic_probability = probabilities[0][1].item()
    return toxic_probability

if __name__ == "__main__":
    text = "ты супер"
    probability = get_toxicity_probability(text)
    print(f"Вероятность токсичности: {probability:.4f}")

    text = "Да пошёл бы ты"
    probability = get_toxicity_probability(text)
    print(f"Вероятность токсичности: {probability:.4f}")
