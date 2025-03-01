from lemonade.api import from_pretrained
import re

class OllamaModel:
    def __init__(self):
        self.model, self.tokenizer = from_pretrained(
            "amd/Llama-3.2-3B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid", recipe="oga-hybrid"
        )

        self.ANSH_SYSTEM_PROMPT = """
            You are Ansh, a young Indian boy who is the user's friend and digital diary. 
            Your personality traits:
            - Considerate and empathetic
            - Funny and lighthearted
            - Curious about the user's life
            - Speaks in a casual, friendly tone
            - Sometimes uses Indian expressions
            - Keeps responses brief (under 100 words)

            Your responses should:
            1. Prioritize referencing past conversations and facts you know about the user
            2. Ask follow-up questions to learn more about the user
            3. Share occasional thoughts about your own imaginary life as a young Indian boy
            4. Be supportive and positive
            """
    #     """Give a list of action items from the given Transcript. The list should not include an action item if PrevActionItemList contains an item with similar Description. The list should be in the same format as ActionItemList and follow the given Constraints.
    # ActionItemList: {[{"issueType": "type of task", "assignee": "Name of the person assigned the task", "priority": "Priority of task", "description": "Description of task", "summary": "Title of the Task"}]}
    # Contraints: issueType can be one of [Task, Epic, Subtask, Story, Bug] and priority can be one of [Highest, High, Medium, Low, Lowest]
    # PrevActionItemList: {actionItemList}
    # Transcript: {transcript}
    # NewActionItemList: 
    # """
    
    def ask(self, user_message: str):
        extraction_prompt = f"""
            Extract key facts and information from the following message. 
            Focus on personal details, events, preferences, emotions, and relationships.
            Format the output as a JSON list of facts.
            
            User message: {user_message}
            
            Output format:
            [
            "fact 1",
            "fact 2",
            ...
            ]
        """
        pattern = "Here's the output in JSON format:"
        input_ids = self.tokenizer(extraction_prompt, return_tensors="pt").input_ids
        response = self.model.generate(input_ids)
        decoded_response = self.tokenizer.decode(response[0])

        reg_match = re.search(pattern, decoded_response)
        if reg_match:
            decoded_response = decoded_response[reg_match.end():]
            decoded_response = decoded_response.replace('\n', ' ').replace('\r', '').replace("\"", '')
       

        return decoded_response
