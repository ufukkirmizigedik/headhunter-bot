import os
import requests
import re
import openai
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import random
import time
from openai import OpenAI

# === API Anahtarları ===
access_token = "your access token"
OPENAI_API_KEY = "your api key"
client = OpenAI(api_key=OPENAI_API_KEY)



headers = {
    "Authorization": f"Bearer {access_token}",
    "User-Agent": "InsightJobBot/1.0 (info@insightgram.ru)" #Write yours from hh.ru
}




search_queries = [
    "RPA",
    "RPA AND Pyhton",
    "AI AND automation",
    "AI agent OR AI агент",
    "ChatGPT OR GPT-4",
    "GPT API integration",
    "low-code OR no-code AND AI",
    "Python AND automation",
    "Python AND автоматизация",
]


profile_summary = """
Меня зовут Уфук, я инженер-автоматизатор и разработчик с опытом более 16 лет. Я проектирую и реализую решения, которые работают автономно, без участия человека — от уровня «железа» до ИИ-аналитики и Telegram-интеграций.

Я совмещаю опыт в:
— разработке ПО (Python full-stack, Flask, Django,Telegram, ETL, ML)
— электронике (пайка, сенсоры, NFC, Raspberry Pi, MicroPython)
— DevOps/деплой (VPS, cron, SSH, логирование)
-📌 Я не frontend-разработчик и не занимаюсь созданием сайтов или пользовательских интерфейсов.
Я строю backend-решения, автоматизирую процессы, обрабатываю данные и интегрирую AI.
Если нужно, могу реализовать простой web-интерфейс (Flask, HTML/CSS), но это не моя основная специализация.


💡 Что я реализовал:
• InsightGram — интеллектуальная AI-система для Telegram-аналитики (https://insightgram.ru)
• Финансовый бот — Telegram-сбор отчётности, визуализация KPI, auto-dashboard
• SkillAnalyzer — веб-сервис оценки Jupyter Notebook, рекомендации по коду
• IoT-терминалы — NFC-устройства для логистики, терминалы с сенсорами и автономным питанием
• ML-модель прогнозирования продаж (Time Series, Scikit-learn)

🧠 Навыки:
Python, SQL, Flask, Django, Pandas, Plotly, Seaborn, Aiogram, MicroPython, HTML/CSS, Git, Linux, Selenium, BeautifulSoup
Raspberry Pi, NFC (PN532), сенсоры, пайка, мультиметр
ClickHouse, PostgreSQL, devops-настройка на VPS (cron, ssh, logs)

📦 Аппарат + AI: я создаю решения под ключ — от микроконтроллера до AI-аналитики.

🗣️ Языки: Русский (C1), Турецкий (родной), Английский (B2)
🔗 GitHub: https://github.com/ufukkirmizigedik
"""




params = {
    "text": "query",
    "area": "1",
    "per_page": 20,
    "page": 0
}

def extract_requirements(html_description):
    text = BeautifulSoup(html_description, "html.parser").get_text(separator="\n")
    text = text.strip()
    match = re.search(r"(Требования[:\s\n]+)(.*?)(Обязанности[:\s\n]+|Условия[:\s\n]+|$)", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(2).strip()
    match = re.search(r"(Обязанности[:\s\n]+)(.*?)(Условия[:\s\n]+|$)", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(2).strip()
    return text[:1000]

def check_gpt_suitability(requirements: str) -> str:
    # Pozitif örnekleri oku
    try:
        with open("positive_examples.json", "r") as f:
            examples = json.load(f)
    except Exception as e:
        print(f"⚠️ Örnek dosya okunamadı: {e}")
        examples = []

    # En fazla 3 örnek kullan
    examples_text = ""
    for i, job in enumerate(examples[:3], 1):
        examples_text += f"{i}. Название: {job['название']}\n"
        examples_text += f"   Обязанности: {job['обязанности']}\n"
        examples_text += f"   Требования: {job['требования']}\n\n"

    prompt = f"""
Ты — профессиональный помощник, который анализирует описание вакансии и определяет, подходит ли она кандидату со следующими навыками:
- автоматизация на Python
- создание Telegram-ботов
- внедрение RPA и AI-решений
- анализ данных и SQL
- автоматизация отчетности

Вот 3 примера вакансий, которые были ранее признаны ПОДХОДЯЩИМИ:
{examples_text}

Теперь тебе нужно оценить следующую вакансию:

{requirements}

Ответь строго: "ДА" или "НЕТ".
"""


    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "Ты — помощник, оценивающий вакансии."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    answer = response.choices[0].message.content
    return answer.strip()

# === GPT: сопроводительное письмо ===
def generate_pismo(requirements):
    response = client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[
            {"role": "user", "content": f"""

Ты — кандидат по имени Уфук, который ищет новую работу в сфере автоматизации, Python и AI-решений.

Вот описание вакансии:

{requirements}

Вот краткое описание твоего опыта и сильных сторон:

{profile_summary}

Твоя задача — написать живое, убедительное и искреннее сопроводительное письмо, которое:

— звучит по-человечески, без шаблонов и клише;
— показывает, почему именно эта вакансия тебе интересна;
— объясняет, какие твои навыки и подходы помогают решать такие задачи;
— честно говорит, если чего-то ты ещё не делал, но умеешь решать похожие проблемы;
— создаёт впечатление, что кандидат мотивирован и хочет развиваться именно в этом направлении.

Не выдумывай фактов, которых нет в профиле. Лучше подчеркни реальные достижения, подход и образ мышления.

Сделай так, чтобы письмо захотелось прочитать до конца.

"""}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def get_resume_id():
    r = requests.get("https://api.hh.ru/resumes/mine", headers=headers)
    if r.status_code != 200:
        print(f"❌ /resumes/mine hatası ({r.status_code}):", r.text)
        return None
    data = r.json()
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["id"]
    print("❗ Резюме не найдено в аккаунте!")
    return None

def get_vacancy_detail(vacancy_id, retries=3):
    for attempt in range(retries):
        r = requests.get(f"https://api.hh.ru/vacancies/{vacancy_id}", headers=headers)
        if r.status_code == 200:
            time.sleep(random.uniform(1.2, 1.7))
            return r
        elif r.status_code == 429:
            wait = 2 ** attempt
            print(f"⏳ 429 Too Many Requests, {wait} saniye bekleniyor...")
            time.sleep(wait)
        else:
            print(f"❌ Detay alınamadı ({r.status_code}): {vacancy_id}")
            return None
    print(f"❌ {vacancy_id} için maksimum tekrar denemesi yapıldı.")
    return None

def apply_to_job(vacancy_id, pismo):
    resume_id = get_resume_id()
    if not resume_id:
        return {"status": "fail", "reason": "no_resume"}
    url = "https://api.hh.ru/negotiations"
    payload = {
        "vacancy_id": vacancy_id,
        "resume_id": resume_id,
        "message": pismo
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        json_response = response.json()
    except:
        json_response = {"error": response.text}

    if response.status_code in [200, 201, 204]:
        return True
    else:
        print(f"❌ ошибка отклик → Код {response.status_code}")
        print("↪️ ответ:", json_response)
        return {"status": "fail", "code": response.status_code, "response": json_response}

def has_already_applied(vacancy_id, query_text):
    safe_query = query_text.replace("/", "-")
    log_path = os.path.join("logs", f"{safe_query}.json")
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return any(entry["id"] == vacancy_id for entry in data)
    except:
        return False

def was_gpt_checked(vacancy_id, query_text):
    safe_query = query_text.replace("/", "-")
    log_path = os.path.join("logs", f"{safe_query}_gpt_decisions.json")
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return any(entry["id"] == vacancy_id for entry in data)
    except:
        return False

def log_gpt_decision(vacancy_id, decision, query_text):
    log_entry = {
        "id": vacancy_id,
        "decision": decision,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    safe_query = query_text.replace("/", "-")
    log_path = os.path.join("logs", f"{safe_query}_gpt_decisions.json")
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []
    data.append(log_entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_application(vacancy, pismo, query_text):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "id": vacancy["id"],
        "name": vacancy["name"],
        "company": vacancy["employer"]["name"],
        "url": vacancy["alternate_url"],
        "pismo": pismo
    }
    safe_query = query_text.replace("/", "-")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{safe_query}.json")
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []
    data.append(log_entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    for query in search_queries:
        print(f"\n🔎 Поиск по запросу: {query}")
        current_page = 0
        MAX_PAGES = 5

        while current_page < MAX_PAGES:
            params["text"] = query
            params["page"] = current_page
            response = requests.get("https://api.hh.ru/vacancies", headers=headers, params=params)
            if response.status_code != 200:
                print(f"❌ API hatası ({response.status_code}):", response.text)
                break

            data = response.json()
            vacancies = data.get("items", [])
            if not vacancies:
                break

            print(f"🔢 Найдено вакансий на странице {current_page + 1}: {len(vacancies)}")

            for vacancy in vacancies[:2]:
                vacancy_id = vacancy["id"]
                print(f"📌 Vacancy ID: {vacancy_id}")

                # === YENİ EKLENEN TARİH FİLTRESİ ===
                published_at = vacancy.get("published_at", "")
                if published_at:
                    publish_date = datetime.fromisoformat(published_at[:19])
                    if publish_date.date() != datetime.today().date():
                        print("📆 Bugün yayınlanmamış — atlanıyor.")
                        continue


                salary = vacancy.get("salary")
                if salary:
                    if salary.get("from") and salary["from"] < 100000:
                        print(f"💸 Зарплата слишком низкая (от {salary['from']}₽) — пропускаем.")
                        continue
                    if salary.get("to") and salary["to"] < 100000:
                        print(f"💸 Верхняя граница зарплаты низкая (до {salary['to']}₽) — пропускаем.")
                        continue

                if has_already_applied(vacancy_id, query):
                    print("⏩ Отклик уже отправлено, продолжаем.")
                    continue

                detail_response = get_vacancy_detail(vacancy_id)
                if not detail_response:
                    continue

                detail = detail_response.json()
                html_desc = detail.get("description", "")
                if not html_desc:
                    html_desc = detail.get("snippet", {}).get("responsibility", "")

                requirements = extract_requirements(html_desc)
                if not requirements.strip():
                    full_text = BeautifulSoup(html_desc, "html.parser").get_text()
                    if len(full_text.strip()) > 200:
                        print("⚠️ Требования не найдены, используется snippet.")
                        requirements = full_text.strip()
                    else:
                        print("⚠️ İlan açıklaması boş veya alınamadı, GPT değerlendirmesi atlanıyor.")
                        continue

                print(f"\n🔍 {vacancy['name']} ({vacancy_id}) — {vacancy['employer']['name']}")
                print(f"URL: {vacancy['alternate_url']}")
                if was_gpt_checked(vacancy_id, query):
                    print("⏭️ Bu ilan GPT ile daha önce kontrol edilmiş.")
                    continue

                decision = check_gpt_suitability(requirements)
                print("РЕШЕНИЕ GPT:", decision)
                log_gpt_decision(vacancy_id, decision, query)

                if "ДА" in decision.strip().upper():
                    print("✅ Подходит! — сопроводительное письмо готовится...")
                    pismo = generate_pismo(requirements)
                    print("--- Начало письмо ---")
                    print(pismo[:300], "...")
                    print("📤 Отклик отправляется...")
                    result = apply_to_job(vacancy_id, pismo)
                    if result is True:
                        print("✅ Отклик отправлен.")
                        log_application(vacancy, pismo, query)
                    else:
                        print("❌ Başvuru başarısız.")
                else:
                    print("⛔ Не подходит!, продолжаем.")

            current_page += 1

if __name__ == "__main__":
    main()