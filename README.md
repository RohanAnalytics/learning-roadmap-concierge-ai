# 🎯 Learning Roadmap Concierge AI

A production-ready **Multi-Agent AI Learning Assistant** built with **Python**, **Google Gemini**, and **Streamlit** that generates personalized learning roadmaps, recommends learning resources, tracks learning progress, creates quizzes, and provides AI-powered learning analytics.

Designed using a modular multi-agent architecture where each agent specializes in a specific responsibility while collaborating to deliver an intelligent learning experience.

---

# 🚀 Features

- 🤖 Multi-Agent AI Architecture
- 🗺️ Personalized Learning Roadmaps
- 📚 AI-Powered Resource Recommendations
- 📈 Learning Progress Tracking
- 🧠 Quiz Generation
- 📊 AI Learning Analytics
- 👤 User Profile Management
- 💾 Persistent Progress Storage
- 🖥️ Interactive Streamlit Interface
- ⚡ Powered by Google Gemini

---

# 🏗️ Project Architecture

```text
                    User
                      │
                      ▼
              Streamlit Interface
                      │
                      ▼
             Coordinator Agent
        ┌────────┬────────┬────────┐
        │        │        │        │
        ▼        ▼        ▼        ▼
 Planner  Resource  Quiz  Progress
 Agent     Agent    Agent   Agent
        │        │        │
        └────────┴────────┘
                 │
                 ▼
          Analytics Agent
                 │
                 ▼
         Gemini AI + Tools Layer
```

---

# 📂 Project Structure

```text
learning-roadmap-concierge-ai/

├── app/
│   ├── agents/
│   └── ui/
│
├── config/
│
├── data/
│
├── memory/
│
├── skills/
│
├── tools/
│
├── requirements.txt
├── main.py
├── run.py
├── LICENSE
└── README.md
```

---

# 🧠 AI Agents

| Agent | Responsibility |
|--------|----------------|
| Coordinator Agent | Routes user requests |
| Planner Agent | Generates learning roadmaps |
| Resource Agent | Recommends learning resources |
| Quiz Agent | Generates quizzes |
| Progress Agent | Tracks completed topics |
| Profile Agent | Manages learner profile |
| Analytics Agent | Produces learning insights |

---

# 🛠️ Tech Stack

## Programming

- Python 3.11+

## AI

- Google Gemini API

## Frontend

- Streamlit

## Libraries

- google-genai
- python-dotenv
- requests
- rich
- pydantic

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/RohanAnalytics/learning-roadmap-concierge-ai.git
```

### Move into the project

```bash
cd learning-roadmap-concierge-ai
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it

**Windows**

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
MODEL_NAME=gemini-2.5-flash
APP_NAME=Learning Roadmap Concierge AI
DEBUG=True
```

---

# ▶️ Running the Application

### Run the Streamlit interface

```bash
streamlit run app/ui/streamlit_app.py
```

or

```bash
python run.py
```

---

# 💡 Example Workflow

1. User selects a learning goal.
2. Profile Agent stores user information.
3. Planner Agent generates a personalized roadmap.
4. Resource Agent recommends learning resources.
5. Progress Agent tracks completed topics.
6. Quiz Agent evaluates understanding.
7. Analytics Agent summarizes learning progress.

---

# 📊 Current Capabilities

- ✅ Personalized Learning Roadmaps
- ✅ Learning Progress Tracking
- ✅ AI Resource Recommendations
- ✅ AI Quiz Generation
- ✅ AI Learning Analytics
- ✅ User Profile Management
- ✅ Persistent Progress Storage

---

# 📌 Future Improvements

- Authentication
- Cloud Database Integration
- PDF Roadmap Export
- Voice Assistant
- Daily Learning Notifications
- Multi-language Support
- Adaptive Learning Paths
- Leaderboards

---

# 👨‍💻 Author

**Rohan Rawat**

Data Analyst | AI Enthusiast | Power BI Developer

**GitHub:**  
https://github.com/RohanAnalytics

**LinkedIn:**  
(Add your LinkedIn Profile URL)

---

# 📄 License

This project is licensed under the MIT License.
