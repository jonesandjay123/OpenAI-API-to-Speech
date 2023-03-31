import os
import openai

with open("api_key.txt", "r") as f:
    openai.api_key = f.read().strip()
lst = openai.Model.list()
print(lst)

