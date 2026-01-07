from core.gemini_client import client

chat = client.chats.create(model="gemini-2.5-flash")

print("chat starts here.... type 'endchat' to terminate the session")
user_input = input("User: ")

while user_input != "endchat":
    response = chat.send_message(user_input)
    print("Chatbot: " + response.text)
    user_input = input("User: ")
