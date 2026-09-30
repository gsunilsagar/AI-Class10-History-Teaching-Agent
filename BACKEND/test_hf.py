import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

token = os.getenv("HF_TOKEN")

print("Token found:", bool(token))

if token:
    print("Token prefix:", token[:5])
else:
    print("ERROR: HF_TOKEN not found")

client = InferenceClient(
    token=token
)

try:
    response = client.chat.completions.create(
        model="HuggingFaceH4/zephyr-7b-beta",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ],
        max_tokens=30
    )

    print("\nSUCCESS:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nERROR:")
    print(repr(e))