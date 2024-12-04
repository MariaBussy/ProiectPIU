from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the Qwen model and tokenizer
model_name = "Qwen/Qwen2.5-0.5B"  # Use Qwen2.5-0.5B model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_book_recommendations(prompt):
    # Tokenize input with attention mask
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

    # Generate output with temperature and do_sample set to True
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=200,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,  # Ensures proper handling of padding
        num_return_sequences=1  # Generate only one sequence
    )

    # Decode and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Example prompt for book recommendations
prompt = (
    "Suggest five books that are similar to 'A Song of Ice and Fire' by George R. R. Martin and 'Lord of the Rings' by J. R. R. Tolkien written by other authors."
    "Answer in a valid json as it follows: {book: name of the book, author: author name.}"
)

# Generate the book recommendations
recommendations = generate_book_recommendations(prompt)
print("Recommended books:\n", recommendations)
