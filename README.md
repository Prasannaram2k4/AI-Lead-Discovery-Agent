# 🤖 AI Lead Discovery Agent

An intelligent, automated sales agent that scrapes leads from Bark.com, scores them against an Ideal Customer Profile (ICP) using AI, and generates highly personalized outreach pitches.


Walkthrough:-

https://github.com/user-attachments/assets/ac232bff-a30d-47cb-b757-aef52e4ee52c



<img width="1300" height="812" alt="Screenshot 2026-10-01 at 3 15 32 AM" src="https://github.com/user-attachments/assets/f1c840fc-b636-4ff5-9ce6-3fdc564e6bb5" />


<img width="1304" height="818" alt="Screenshot 2026-10-01 at 3 16 10 AM" src="https://github.com/user-attachments/assets/79098cc1-3005-4378-af13-cab9cc77e150" />


<img width="1292" height="815" alt="Screenshot 2026-10-01 at 3 16 38 AM" src="https://github.com/user-attachments/assets/e4f5af5d-bffb-4a9f-a329-7c29e064cc31" />


<img width="1295" height="813" alt="Screenshot 2026-10-01 at 3 16 52 AM" src="https://github.com/user-attachments/assets/90824fdf-d7b6-4b55-8585-0c38581b79d7" />


<img width="1304" height="812" alt="Screenshot 2026-10-01 at 3 17 00 AM" src="https://github.com/user-attachments/assets/5ded85d0-0c49-4fd9-b43a-95cd9765d4a5" />



## ✨ Features
- 🕷️ **Automated Scraping:** Uses Playwright to securely log into Bark.com and extract lead details.
- 🧠 **AI Lead Scoring:** Evaluates leads using Groq and Llama 3.3 (70B), filtering out low-quality prospects based on budget, service, and intent.
- ✍️ **Hyper-Personalized Pitching:** Acts as an expert sales copywriter to draft tailored 3-paragraph outreach messages that reference specific details from the lead's request.
- 📊 **Summary Reports:** Exports qualified leads and their generated pitches to a structured `results.json` file.

<img width="1301" height="728" alt="Screenshot 2026-10-01 at 3 15 47 AM" src="https://github.com/user-attachments/assets/67199542-532f-4737-bab4-b00854589c59" />


<img width="1298" height="819" alt="Screenshot 2026-10-01 at 3 17 30 AM" src="https://github.com/user-attachments/assets/7de6a5b4-bea7-4376-9c4e-5c3e8a921f0e" />


## 🛠️ Tech Stack
- **Python 3**
- **Playwright** (Web Automation & Scraping)
- **Groq API** (Fast LLM Inference using `llama-3.3-70b-versatile`)
- **Dotenv** (Environment management)

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-lead-discovery-agent.git
   cd ai-lead-discovery-agent




