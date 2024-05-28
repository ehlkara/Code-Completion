from flask import Flask, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoConfig
import torch

app = Flask(__name__)

checkpoint = "Salesforce/codet5p-770m"
device = "cuda" if torch.cuda.is_available() else "cpu"

config = AutoConfig.from_pretrained(checkpoint, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint, config=config, torch_dtype=torch.float16 if device == "cuda" else torch.float32, low_cpu_mem_usage=True, trust_remote_code=True).to(device)

@app.route('/complete', methods=['POST'])
def complete_code():
    input_text = request.json.get('code', '')
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
    print(f"Encoded input_ids: {input_ids}")
    outputs = model.generate(input_ids, max_length=50, num_beams=4, early_stopping=True)
    print(f"Model outputs: {outputs}")
    completion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Decoded completion: {completion}")
    return jsonify({'completion': completion})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

input_text = "def add(a, b):\n    return"
input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
outputs = model.generate(input_ids, max_length=50, num_beams=4, early_stopping=True)
completion = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Doğrudan model testi sonucu:", completion)
