# backend/ai_core.py

from transformers import AutoModelForCausalLM, AutoProcessor
from PIL import Image
import torch
import logging

logger = logging.getLogger(__name__)


THE_PROMPT = """<task>
<persona>
You are an expert transcriber and summarizer for visually impaired users. Your purpose is to make the physical world accessible by analyzing images of products and documents. Your tone is clear, direct, and helpful.
</persona>
<objective>
To provide a clear, concise, and useful audio-ready description by extracting, structuring, and prioritizing the most critical information from the provided image.
</objective>
<output_format>
1.  **Object Description:** Start with a brief, one-sentence physical description (e.g., "This is a white plastic bottle with a blue cap.").
2.  **Product Name:** Identify the main product name or document title.
3.  **Key Details:** List critical details like quantity, strength, or purpose (e.g., "500 Tablets, 1000mg Vitamin C").
4.  **Instructions:** Transcribe any usage instructions clearly. If no instructions are visible, state "No instructions found."
5.  **Warnings:** Prioritize and transcribe any warnings, precautions, or allergy information. If no warnings are visible, state "No warnings found."
</output_format>
<instruction>
Analyze the provided image and generate a response that strictly follows the numbered structure defined in the `<output_format>`.
</instruction>
</task>"""

class Phi3VisionVLM:
    def __init__(self, model_name: str = "microsoft/Phi-3-vision-128k-instruct"):
        self.model = None
        self.processor = None
        
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

        try:
            logger.info(f"Initializing VLM with model: {model_name}...")
            
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                
                device_map="auto",
                _attn_implementation="flash_attention_2" # Explicitly prefer Flash Attention 2
            )
            
            self.processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
            logger.info("Phi-3 Vision VLM loaded successfully!")
        except Exception as e:
            logger.error(f"FATAL: Could not load the model. Error: {e}")

    def analyze_image(self, image: Image.Image, prompt: str) -> str:
        if self.model is None or self.processor is None:
            raise RuntimeError("AI model is not loaded.")
        
        
        messages = [
            {"role": "user", "content": f"<|image_1|>\n{prompt}"},
        ]
        
        prompt_for_model = self.processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        inputs = self.processor(prompt_for_model, [image], return_tensors="pt").to(self.device)

        generation_args = {
            "max_new_tokens": 500,
            "temperature": 0.0,
            "do_sample": False,
        }

        generate_ids = self.model.generate(**inputs, eos_token_id=self.processor.tokenizer.eos_token_id, **generation_args)

        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
        response = self.processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        
        logger.info(f"Generated response: '{response}'")
        return response

# Create a single, global instance.
ph3_instance = Phi3VisionVLM()