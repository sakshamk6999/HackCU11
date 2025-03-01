import ollama


class OllamaModel:
    def __init__(self):
        self.model = 'llama3.2:1b'
        self.stream = False
    
    def ask(self, prompt: str):
        response = ollama.chat(
            model=self.model, 
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']

# response = ollama.chat(model='llama3.2:1b', messages=[{'role': 'user', 'content': 'Tell me a short story.'}])
# print(response['message']['content'])

# Streaming example
# stream = ollama.chat(model='llama3.2:1b', messages=[{'role': 'user', 'content': 'Write a poem about the sea.'}], stream=True)
# for part in stream:
#     print(part['message']['content'], end='', flush=True)
# print()

# # Generate example
# response = ollama.generate(model='llama3', prompt='Explain the theory of relativity in simple terms.')
# print(response)

