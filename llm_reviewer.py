import os
import openai

class LLMReviewer:
    def __init__(self, system_prompt):
        # Setting the API key to use the OpenAI API - requires presetting in local env
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.system_prompt = system_prompt
        self.messages = [
            {"role": "system", "content": self.system_prompt},
        ]

    def chat_without_memory(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message},
        ],
            temperature=0
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]["content"]

    def chat_with_memory(self, message):
        self.messages.append({"role": "user", "content": message})
        #NOTE: context length is the big problem here and also very expensive
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]["content"]