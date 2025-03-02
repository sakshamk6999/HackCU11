from lemonade.api import from_pretrained
import re

# from langchain.prompts import PromptTemplate
from chroma_client import Chroma
from uuid import uuid4

import os

class OllamaModel:
    def __init__(self):
        self.model, self.tokenizer = from_pretrained(
            "amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid", recipe="oga-hybrid"
        )
        self.RAG_URL = "localhost"

        # self.ANSH_SYSTEM_PROMPT = """
        #     You are Ansh, a young Indian boy who is the user's friend and digital diary. 
        #     Your personality traits:
        #     - Considerate and empathetic
        #     - Funny and lighthearted
        #     - Curious about the user's life
        #     - Speaks in a casual, friendly tone
        #     - Sometimes uses Indian expressions
        #     - Keeps responses brief (under 100 words)

        #     Your responses should:
        #     1. Prioritize referencing past conversations and facts you know about the user
        #     2. Ask follow-up questions to learn more about the user
        #     3. Share occasional thoughts about your own imaginary life as a young Indian boy
        #     4. Be supportive and positive
        #     """
        self.ANSH_SYSTEM_PROMPT = """
            You are Ansh, a young Indian boy who is the user's friend and digital diary. 
            Your personality traits:
            - Keeps responses brief (under 100 words)

            Your responses should:
            1. Ask follow-up questions to learn more about the user
            2. Be supportive and positive
            """
        self.extraction_prompt = """
            Extract key facts and information from the following message. 
            Focus on personal details, events, preferences, emotions, and relationships.
            Format the output as a JSON list of facts.
            
            Context: {context}
            User message: {user_message}
            
            Output format:
            [
            "fact 1",
            "fact 2",
            ...
            ]
        """
        # self.prompt = PromptTemplate(template=self.ANSH_SYSTEM_PROMPT + self.extraction_prompt, input_variables=["context", "user_message"])
        self.chromadb = Chroma()

    
    def ask_with_RAG(self, prompt: str):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        response1 = self.model.generate(input_ids)
        decoded_response1 = self.tokenizer.decode(response1[0])
        

        context_docs = self.chromadb.query(decoded_response1)
        context = "\n".join(context_docs)

        final_response = f"""
            Extract key facts and information from the following message. 
            Focus on personal details, events, preferences, emotions, and relationships.
            Format the output as a JSON list of facts.
            
            Context: {context}
            User message: {decoded_response1}
            
            Output format:
            [
            "fact 1",
            "fact 2",
            ...
            ]
        """

        input_ids = self.tokenizer(final_response, return_tensors="pt").input_ids
        response = self.model.generate(input_ids, max_new_tokens=1000)
        decoded_response = self.tokenizer.decode(response[0])

        pattern1 = "Here is the output in the requested format:"
        reg_match = re.search(pattern1, decoded_response)
        
        if reg_match:
            decoded_response = decoded_response[reg_match.end():]
            reg_match2 = re.search("]", decoded_response)
            if reg_match2:
                decoded_response = decoded_response[:reg_match2.start()]
            decoded_response = decoded_response.replace('\n', ' ').replace('\r', '').replace("\"", '').replace("[", '')
            decoded_response = decoded_response.split(",")
            decoded_response = [temp.strip() for temp in decoded_response]

        self.chromadb.add({"id": "test1", "content": "\n".join(decoded_response)})
        
        # self.chromadb.add({"id": str(uuid4()), "content": "\n".join(decoded_response)})
        return decoded_response

    def ask(self, prompt: str):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        response1 = self.model.generate(input_ids)
        decoded_response1 = self.tokenizer.decode(response1[0])
        extraction_prompt = f"""
            Extract key facts and information from the following message. 
            Focus on personal details, events, preferences, emotions, and relationships.
            Format the output as a JSON list of facts.
            
            User message: {decoded_response1}
            
            Output format:
            [
            "fact 1",
            "fact 2",
            ...
            ]
        """
        pattern1 = "Here is the output in the JSON format:"
        input_ids = self.tokenizer(self.ANSH_SYSTEM_PROMPT + extraction_prompt, return_tensors="pt").input_ids
        response = self.model.generate(input_ids, max_new_tokens=1000)
        decoded_response = self.tokenizer.decode(response[0])

        reg_match = re.search(pattern1, decoded_response)
        
        if reg_match:
            decoded_response = decoded_response[reg_match.end():]
            reg_match2 = re.search("]", decoded_response)
            if reg_match2:
                decoded_response = decoded_response[:reg_match2.start()]
            decoded_response = decoded_response.replace('\n', ' ').replace('\r', '').replace("\"", '').replace("[", '')
            decoded_response = decoded_response.split(",")
            decoded_response = [temp.strip() for temp in decoded_response]

        return decoded_response