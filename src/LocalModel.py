from src.BaseModel import BaseModel
from transformers import T5Tokenizer, T5ForConditionalGeneration


class LocalModel(BaseModel):
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("model/flan-t5-large")
        self.model = T5ForConditionalGeneration.from_pretrained("model/flan-t5-large")

    def generate_text(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids
        # attention_mask = inputs.attention_mask

        gen_tokens = self.model.generate(
            input_ids,
            do_sample=True,
            # attention_mask=attention_mask,
            temperature=0.3,
            max_length=500,
            min_length=50,
            top_k=100,
            top_p=0.8,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
        )

        generated_text = self.tokenizer.decode(gen_tokens[0], skip_special_tokens=True)
        return generated_text
