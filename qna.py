# qa_model.py
from transformers import pipeline

# Load the model and tokenizer once
model_name = "deepset/bert-large-uncased-whole-word-masking-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def get_answer(question, context):
    QA_input = {
        'question': question,
        'context': context
    }
    result = nlp(QA_input)
    return result['answer']
