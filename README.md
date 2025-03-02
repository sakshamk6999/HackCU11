# Ansh.ai

## 📚 About the Project

Journaling has always been a powerful tool for self-reflection, but we wanted to make it more natural, conversational, and accessible — like talking to a trusted friend. This inspired us to create **Ansh.ai**, a **real-time agentic AI friend** that listens to your thoughts, understands your emotions, and helps you process your day through meaningful conversation.  

The name **Ansh** stands for **Artificial Narrator for Self-reflection and Harmony**, but in Sanskrit, it also means **“a part of you.”** This dual meaning captures our goal — building an AI that feels personal, empathetic, and truly connected to the user’s inner world.

Ansh.ai acts as a **real-time conversational diary companion**.  
- You speak, Ansh listens.
- It reflects on your day with you, asking gentle questions and providing insights.
- It remembers past conversations, helping you connect patterns over time.
- Responses are presented not just as text, but through a **talking AI avatar** that feels more human and approachable.

Whether you’re venting after a long day, celebrating small wins, or reflecting on personal growth, Ansh is always there to listen and respond with thoughtful reflections.



## 💻 Tech Stack
|  Tech	|  Usage  |
| -------- | ------- |
|Python	| Backend logic & APIs |
| Flask | Web server |
| React |	Frontend UI |
| ChromaDB |	Vector Database |
| Langchain |	LLM integration |
| AMD Minisforum AI 370 | Hybrid NPU+GPU Compute|

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/sakshamk6999/HackCU11.git
cd HackCU11
```

Install backend dependencies
```bash
pip install -r backend/latest_requirements.txt
```

Install frontend dependencies
```bash
cd frontend
npm install
```

Run the project (backend):
```bash
python app.py &
python server.py
```

Run project (frontend):
```bash
cd frontend
npm run dev
```
## Video - https://youtu.be/1wwqeeN3aRM

## 🧑‍💻 Team Members
- Saksham Khatwani 
- Rahul Shetty
- Siddharth De
- Gyanig Kumar
- Uditanshu Tomar

## npu fix
If you are facing issues when running the backend app, try the following:

```bash
pip install -r small_requirements.txt --force-reinstall
```

## ❤️ Acknowledgments

Special thanks to the HackCU team for organizing this amazing hackathon!

Shoutout to Naveen from AMD for helping us work and develop with the AMD Miniforum AI 370.
