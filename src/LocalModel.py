from src.BaseModel import BaseModel
#from transformers import T5Tokenizer, T5ForConditionalGeneration
import json
import logging

logger = logging.getLogger("LocalModel")


class LocalModel(BaseModel):
    def __init__(self, model):
        with open("data/config.json", 'r') as f:
            config = json.load(f)

        self.model_path = config["local_models"][model]
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)

    def generate_text(self, prompt: str) -> str:

        logger.debug("tokenize prompt")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids
        # attention_mask = inputs.attention_mask

        logger.info("Generate text")
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
