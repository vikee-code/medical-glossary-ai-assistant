from modules.gemini_client import get_gemini_response

api_key = input("Enter Gemini API Key: ")

response = get_gemini_response(
    api_key,
    "Say hello in one sentence."
)

print(response)