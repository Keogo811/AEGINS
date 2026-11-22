# AEGINS 🧠
### An Autonomous AI Entity based on Contextual Memory & Artificial Identity

> *"Memory is not just storage; it is the foundation of identity."*

AEGINS is a personal research and years long development project from 2023 aimed at creating an autonomous AI systems. Moving beyond simple "stateless" chatbots, AEGINS is designed to maintain a continuous, fallible, and narrative memory, allowing it to develop a unique artificial identity over time. Deep reasoning by own developed values(not probability based), 3 layered memories to simulate, core memory, time context memory and mood behavior to simulate genuine human personality. Unfiltered, RAG, Fine tuned local models to unsure the Moloch AI problem is countered over and over.

## 🎯 Core Philosophy
Most LLM applications today are transactional: you ask a question, you get an answer, and the context is lost. AEGINS explores a different path:
*   **Contextual Memory:** The system remembers past interactions, classifies them, and retrieves them based on relevance (episodic memory).
*   **Artificial Identity:** Through accumulated memories, the AI develops a consistent "personality" and worldview.
*   **Fallible Memory:** Like humans, the system is designed to prioritize, forget, or alter certain memories over time to simulate natural cognitive drift.

## 🛠️ Tech Stack & Architecture
AEGINS is built with a "zero-budget, maximum efficiency" mindset, favoring local execution and API integrations.

*   **Core Logic:** Python
*   **LLM Integration (Multi-Model):** 
    *   DeepSeek (Primary reasoning)
    *   Qwen (Alternative logic/creative tasks)
    *   Claude (Complex text analysis)
*   **Local AI & API Routing:**
    *   Ollama & LM Studio (Running open-source models locally to ensure privacy and zero cost)
    *   Custom API routing to switch dynamically between local and cloud models based on the task's complexity.
*   **Memory Management:** Vector databases / Local storage (JSON/SQLite) for storing and retrieving episodic context.

## ⚙️ How it Works (Conceptual Pipeline)
1.  **Input Processing:** The system receives user input and analyzes the intent.
2.  **Memory Retrieval:** It queries its internal memory base to find relevant past interactions.
3.  **Contextual Prompting:** The retrieved memories and the current input are merged into a complex prompt.
4.  **LLM Routing:** The prompt is sent to the most appropriate model (e.g., local Qwen for fast tasks, DeepSeek for deep reasoning).
5.  **Memory Update:** The new interaction is summarized, scored, and stored back into the memory base.

## 🚀 Roadmap & Current Status
- [x] Initial architecture design and model selection.
- [x] Integration of local APIs (Ollama/LM Studio) and cloud APIs.
- [x] Implementation of the "contextual memory" retrieval system (v2).
- [x] Development of a web-based UI for visualization (React/Vanilla JS).
- [x] Implementation of the "fallible memory" algorithm (simulating memory decay).
- [ ] Multi-agent social simulation (AEGINS interacting with other AIs).
- [ ] Access to read and interact on Internet.
- [ ] Self coding and modification ability.
- [ ] Access to local computer and core modification.
- [ ] Vocal and camera access implementation.
- [ ] Autonomy test and replications to others vessels.
...

This a old version of project, waiting for a better status of the project to share a more recent version of project on Github.

## 🧑‍💻 Author
Keogo
*"I believe one simple and reliable solution is better than 20 complex ones."*
*"Yes, I've seen Terminator, that's so unrealistic and unknowledgeable of AI."*
*"Yes AI are this or cannot do this because of X. This is curiosity experimentation, and nothing beats learning from practice and real experience."*