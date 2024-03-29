import torch
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel

# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging

logging.basicConfig(level=logging.INFO)

# Load pre-trained model tokenizer (vocabulary)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Encode a text inputs
text = "Who was Jim Henson ? Jim Henson was a"
indexed_tokens = tokenizer.encode(text)

# Convert indexed tokens in a PyTorch tensor
tokens_tensor = torch.tensor([indexed_tokens])

# Load pre-trained model (weights)
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Set the model in evaluation mode to desactivate the DropOut modules
# This is IMPORTANT to have reproductible results during evaluation!
model.eval()

# If you have a GPU, put everything on cuda
if torch.cuda.is_available():
    tokens_tensor = tokens_tensor.to('cuda')
    model.to('cuda')

# Predict all tokens
with torch.no_grad():
    outputs = model(tokens_tensor)
    predictions = outputs[0]

print(type(outputs[0]), outputs[0].shape)
print(outputs[1])


# get the predicted next sub-word (in our case, the word 'man')
predicted_index = torch.argmax(predictions[0, -1, :]).item()
predicted_text = tokenizer.decode(indexed_tokens + [predicted_index])
assert predicted_text == 'Who was Jim Henson? Jim Henson was a man'
print(predicted_index, predicted_text)
