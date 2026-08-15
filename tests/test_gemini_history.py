


from google import genai

import inspect


clients = genai.Client(api_key="dummy")

print(inspect.signature(clients.chats.create))
print(inspect.getdoc(clients.chats.create))
      