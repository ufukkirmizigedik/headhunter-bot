# 🤖 HeadHunter GPT Job Tracker

This is an automated job application system for hh.ru.  
It searches for relevant job offers based on predefined queries and uses GPT to evaluate suitability and generate custom cover letters in Russian.  
If a job fits the profile, it automatically sends an application with a personalized message.

## 🔧 Setup

1. Register a client app at [hh.ru OAuth page](https://hh.ru/oauth/)
2. Wait for approval and obtain:
   - `client_id`
   - `client_secret`

3. Run the `config.py` file to authenticate:
```bash
python config.py



Paste the code parameter from the redirected URL after login.

This will give you an access_token (starts with USER...).
Paste that into the main.py file.




4.Set your OpenAI API key in main.py as OPENAI_API_KEY.

▶️ Usage

python main.py


Pulls job listings from hh.ru

Filters out low salary or irrelevant dates

Sends requirements to GPT (with examples)

If GPT says "ДА" → generates custom message and applies

Logs everything in the logs/ folder



🧠 Tech Stack
requests, BeautifulSoup, openai, hh.ru API

Prompt engineering with examples

JSON logging

Token rate limit handling (429-safe)

Russian-language GPT strategy

📄 License
MIT — feel free to use, improve or fork.
