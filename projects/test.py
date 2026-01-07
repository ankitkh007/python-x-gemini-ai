from core.gemini_client import client

prompt = input("Enter any promt: ")
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

print("Gemini response: ")
print("----------------------------------------")
print(response.text)
