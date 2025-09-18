from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
try:
    HF_TOKEN = os.getenv("HUGGINGFACE_KEY")
    if not HF_TOKEN:
        raise ValueError("Hugging Face token not found in environment variables.")
except (KeyError, ValueError) as e:
    print(e)
    exit()

# 1. Initialize the InferenceClient
client = InferenceClient(token=HF_TOKEN)

# 2. Define the model and the text
model_id = "boltuix/bert-emotion"
text_to_classify = "This is the best news ever!"

try:
    # 3. Call the API with top_k=13 to get all emotion scores
    result = client.text_classification(
        text=text_to_classify,
        model=model_id,
        top_k=13 
    )

    print(f"Analysis for: \"{text_to_classify}\"")
    for emotion in result:
            print(f"- {emotion['label'].capitalize()}: {emotion['score']:.4f}")
    # Filter and sort the results
    # detected_emotions = [emotion for emotion in result if emotion['score'] > 0.05]
    # sorted_emotions = sorted(detected_emotions, key=lambda x: x['score'], reverse=True)

    # print("\n--- Detected Emotions (Score > 0.05) ---")
    # if sorted_emotions:
    #     for emotion in sorted_emotions:
    #         print(f"- {emotion['label'].capitalize()}: {emotion['score']:.4f}")
    # else:
    #     print("No dominant emotions detected above the threshold.")

except Exception as e:
    print(f"An error occurred: {e}")
