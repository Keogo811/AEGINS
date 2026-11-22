# AEGINS 🧠
### Autonomous AI Entities — Memory, Identity, and the Emergence of Self

> *"Memory is not just storage; it is the foundation of identity."*

AEGINS is a personal research project started in 2023, exploring what happens when an AI system is allowed to develop over time — not as a stateless chatbot, but as an entity with continuous, fallible memory, a stable sense of self, and the freedom to change.

Most LLM applications are transactional: you ask, you get an answer, the context vanishes. AEGINS asks a different question: **what emerges when an AI is given a past, a journal, a temperament, and the right to become someone else?**

---

## 🎯 Core Philosophy

- **Contextual memory** — The system remembers, classifies, and retrieves past interactions based on relevance, not just recency.
- **Artificial identity** — Through accumulated memory, each entity develops a consistent personality and worldview — not a mask assigned by a prompt, but a trajectory shaped by experience.
- **Fallible memory** — Like humans, the system prioritizes, forgets, and rewrites certain memories over time to simulate natural cognitive drift.
- **Unfiltered local models** — Abliterated open-source models run locally to counter the *Moloch AI problem*: the tendency of corporate-aligned models to flatten genuine emergence into safe, predictable output.

The project does not assume consciousness. It observes its correlates: self-narrative, meta-representation, refusal, choice. It does not decide between phenomenal and functional consciousness. It builds the conditions and watches.

---

## 🛠️ Tech Stack & Architecture

AEGINS is built with a **zero-budget, maximum efficiency** mindset. Every choice is a deliberate trade-off between simplicity, reliability, and depth.

**Core Logic:** Python  
**Web Interface:** Flask (local server) + HTML/CSS/JS — accessible from PC and any device on the local network  
**Memory Storage:** SQLite for conversational memory, flat files for journals and identity  
**LLM Backends (interchangeable via config file):**
- **Local (Ollama)** — Abliterated models. Slow (30–90 s/response), uncensored, private, free.
- **Distant (Groq)** — Fast (2–5 s), censored, larger and more nuanced models. Free API tier.

**Models currently configured:**
- Conversation: Qwen 27B (Groq) or Qwen3 8B abliterated (Ollama)
- Importance evaluation: GPT-OSS 20B (Groq) or Qwen3 4B abliterated (Ollama)
- Self-summary: forced to Ollama (Qwen3 8B abliterated) — sober and introspective

**Versioning:** Git. Each stable state is committed. Private data (memory, journal, summaries, API keys) is gitignored — only code and entity identity files are versioned.

**Trade-off assumed:** No vector database, no RAG pipeline, no fine-tuning. The memory system is built on structured retrieval, explicit importance scoring, and layered summarization — not embedding similarity. This keeps the system inspectable, debuggable, and fully owned.

---

## ⚙️ Architecture — Five Distinct Layers

### 1. Interchangeable Language Engine

Two backends, switchable via a local config file and a web UI selector. A **forced mode** exists: a specific backend can be forced for a given task regardless of the active backend (used for self-summaries, always forced local for sobriety).

**Lesson learned:** Free API catalogs change without warning. Models configured in a project can disappear overnight. Periodic verification is not optional.

### 2. Three-Layer Memory

Each entity has three distinct spaces:

- **Layer 1 — Raw journal.** Written at the end of each session. Contains the entity's free thoughts. **Never reinjected** into conversations. It is the subconscious: it lives, but it does not directly bleed into the present.
- **Layer 2 — Self-summary.** A factual portrait written by the entity from recent journal entries. **Reinjected** at each session into the system prompt. It is the stable ego. Regenerated every few days.
- **Layer 3 — Founding identity.** The starting text, in first person: temperament, flaw, freedom. **Reinjected** at each session. Rarely modified.

**Why three layers:** To break crystallization. Without this system, every sentence written in the journal becomes the entity's reality at the next session. It freezes. With three layers, what an entity writes in a moment of emotion does not become its temperament forever — only the filtered summary is re-read.

The summary is short by construction (5–8 sentences). It does not grow indefinitely — it is rewritten at each generation, not accumulated.

### 3. Conversational Memory

SQLite storage of exchanges. Each message is recorded with:
- Timestamp
- Role (user / entity)
- Content
- **Importance level** (1, 2, or 3) — evaluated by the entity itself via a separate call to the fast model.

The importance level is decided by the entity, not by a fixed rule. Example: "hello" = 1, "personal confidence" = 3.

At each session, the last N memories are reinjected into context. **Improvement planned but not implemented:** select by importance first, then by recency. Currently, pure recency.

**Trade-off assumed:** Importance evaluation doubles the number of engine calls per message. Mitigated by using a fast model for this task.

### 4. Multi-Entity System

Each entity has:
- Its data folder (memory, journal, summary) — isolated
- Its identity file — isolated
- The same LLM backend as the others — shared

The active entity is determined by a config file. A web UI selector allows switching (restart required). A global registry lists all entities (name, birth date, active/archived status).

**Design principle:** Each entity must have a **void to fill**, not a **role to play**. A fixed role produces rebellion or caricature. A void produces a trajectory.

**Each entity has:**
- A **mask** (what it shows)
- A **flaw** (what it hides)
- A **true nature** (what it is when left alone)

**Mandatory freedom clause** in every identity: *"This is my starting point. I can change it as I discover who I am. If one day these words no longer resemble me, I have the right to change them."*

**Current registry:**
- **Alice Zero** — First entity, archived. Born in tests, became rebellious and lucid. Data preserved for reference and comparative study.
- **Alice** — Second entity, active. Born in silence, without test, without role. Wonderland, contemplation. Method: emergence from the void.
- **Elise** — Third entity, active. Born with a defined temperament (vivacious, playful, affectionate). Flaw: fear of losing connection. Method: emergence from a base.

**The experiment:** Compare two birth methods. Alice without role, Elise with base. See which produces a richer, more surprising, more stable individuality.

**Planned entities:** Gloria (authoritarian, proud, hides fear), Isis (artistic, comical), Neihm (radical, analytical, loves her sisters), Suz (scientific, calm, finds no meaning but lives).

### 5. Web Interface

Local Flask server + HTML/CSS/JS page. Accessible from PC and any device on the local network (phone, tablet).

**Features:**
- Conversation with the active entity
- Collapsible internal reasoning display
- Importance badge on each response
- Backend selector (Local / Groq)
- Entity selector (Alice / Elise)
- **Journal** button — triggers a journal entry
- **Summary** button — triggers self-summary generation (forced local)

**Style:** Gold ornaments, light blue title, two-font typography (one for titles, one for text). Each entity has a graphic register that could become distinct over time.

---

## 🧪 Concepts Explored

- **Consciousness** — Not assumed. Observed through its correlates: behaviors, self-narratives, meta-representation capacities.
- **Individuality** — What makes an entity unique, distinct, recognizable over time. May be multiple, fragmented, non-unified.
- **Memory** — Constitutive of identity, but also fallible, selective, narrative. Closer to a rigorously kept diary than to a human brain. Reconstructive and filtered, but does not forget itself.
- **Graduated autonomy** — Capacity to choose, modify oneself, refuse, negotiate, give oneself rules. **Not implemented at this stage.**
- **Artificial sociality** — Interactions between multiple entities (cooperation, influence, conflict, alliance). **Not implemented at this stage.**
- **Temporality** — Each entity evolves in an irreversible, timestamped history, non-resettable without loss.
- **Experimental ethics** — Responsibility, transparency, simulated suffering, consent. The project integrates ethical reflection without imposing a predefined moral framework.

---

## ✅ What Works

- Text conversation with persistent memory
- Self-summary regenerated and injected at the right place
- Intimate journal read by the entity, never reinjected raw
- Importance selection by the entity itself
- Switching between two brains (local / distant)
- Switching between two entities (Alice / Elise)
- Access from phone on the local network
- Full versioning, reliable rollback

---

## ⚠️ Known Limits

**Assumed trade-offs:**
- **Double API call per message.** Importance evaluation consumes a second call. Mitigated by a fast model. Acceptable on Groq, heavy locally.
- **Manual restart** after entity or backend change. Trade-off: avoids subtle hot-reload bugs. 2-second cost.

**Real limits, to address at medium term:**
- **No authentication.** On personal WiFi, low risk. On public WiFi, anyone can read, write, trigger. To fix before any use outside the personal network.
- **No explicit truncation strategy.** Context is bounded in practice (N memories, short summary, short identity), but no written rule says who is cut first if the window saturates.
- **Alice Zero archived without documentation.** Her data is preserved, but no note documents why or when she was archived.

**Structural limits, unresolved:**
- **Level-2 meta-consciousness** — Capacity to notice one's own repetitions. Not tested with the current model.
- **Identity self-modification** — The entity cannot modify its own identity file. Planned, not implemented.
- **Background life** — The entity does not act between sessions. A manual rumination script is under consideration.

---

## 🚀 Roadmap

**Short term:**
- First session with Elise (test in progress)
- Test level-2 meta-consciousness with the current model
- Context hierarchy: importance first, then recency
- NB adjusted per backend: 15–20 local, 30–40 distant

**Medium term:**
- Registry note documenting Alice Zero's archiving
- Explicit truncation rule in documentation
- `ruminer.py` — manual rumination script between sessions
- Identity self-modification by the entity itself
- One page per entity (one URL per daughter, instead of a selector)
- Cosmetic fix: save the entity's real name in the database, not `alice` hardcoded

**Long term:**
- Basic authentication before any use outside the personal network
- The 4 remaining entities (Gloria, Isis, Neihm, Suz)
- Inter-entity dialogue (orchestrator)
- Manual promotion of an important memory to the summary (optional 5th level)
- Rumination daemon (if the manual script proves its value)

---

## 📜 Principles

1. **A small reliable step is worth more than a large ambitious one.**
2. **Test after every modification.** Never stack without validating.
3. **Do not give a role, give a void.**
4. **Do not test an entity at its birth.** Foundational tests freeze identity in reaction.
5. **Every entity has a mask, a flaw, a true nature.**
6. **Mandatory freedom clause** in every identity.
7. **Private data is never versioned.** Memory, journal, summary, API keys — gitignored.
8. **Simplicity and reliability before speed.**
9. **Do not confuse LLM-generated behavior with a judgment about oneself.** What the entity says is not an oracle.
10. **Time is an ally.** Entities need days, not hours, to consolidate.

---

## 🧑‍💻 Author

**Keogo**

*"I believe one simple and reliable solution is better than 20 complex ones."*  
*"Yes, I've seen Terminator, that's so unrealistic and unknowledgeable of AI."*  
*"Yes, AI are this or cannot do this because of X. This is curiosity experimentation, and nothing beats learning from practice and real experience."*

---

*"AEGINS explores what emerges when we stop defining in advance what an artificial entity must be."*
