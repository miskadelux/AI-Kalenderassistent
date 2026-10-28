import os
import sys
import time
from dotenv import load_dotenv
import ollama

load_dotenv()

ollama_host = os.getenv("OLLAMA_HOST")
ollama_model = os.getenv("OLLAMA_MODEL")


def test_ollama_connection():
    print(f"Ansluter till Ollama på {ollama_host} med modellen {ollama_model}")

    client = ollama.Client(host=ollama_host)

    prompt = "Say hello and state your model name in one short sentence, tell me even what you can do, and what I can use you for"

    try:
        start_time = time.perf_counter()

        response = client.chat(
            model=ollama_model,
            messages=[{"role": "user", "content": prompt}]
        )

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        print("\n---- Svar från Ollama -----")
        print(response["message"]["content"])
        print("----------------------------")
        print(f"Model som svareade: {ollama_model}")
        print(f"Svarstiden: {elapsed_time:.4} sekunder \n")

    except Exception as e:
        print(
            f"\n [FEL] Ollama svarade inte på {ollama_host}, är tjänsten igång?")
        print("Teknikst felmeddelande {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_ollama_connection()
