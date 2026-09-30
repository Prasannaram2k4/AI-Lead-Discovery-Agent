from playwright.sync_api import sync_playwright
from groq import Groq
import json
import time
import random
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key= os.getenv("GROQ_KEY"))

def score_lead (name, location , service , description):
    promt = f"""
    You are an AI assistant that scores leads for a high-end web development agency.

    Ideal Customer Profile:
    - Service: Web Development or Web Design
    - Budget: High (over $2000). Note: budget is often not mentioned on Bark.
    - Clear project description
    - Professional business purpose

    Score this lead from 0.0 to 1.0 based on how well it matches.

    Lead Details:
    - Name: {name}
    - Location: {location}
    - Service: {service}
    - Description: {description}

    Reply with ONLY a JSON object like this, nothing else:
    {{
        "score": 0.95,
        "reason": "one sentence explanation"
    }}
    """
    
    response = client.chat.completions.create(
        messages=[
            {
                "role" : "user" ,
                "content" : promt
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    result = json.loads(response.choices[0].message.content)
    return result

def generate_pitch(name , location , service , description):
    promt = f"""
    You are an expert sales copywriter for a high-end web development agency.

    Write a personalized 3 paragraph pitch for this lead.

    Rules:
    - Paragraph 1: Personal greeting mentioning their NAME and SERVICE requested.
    - Paragraph 2: Reference specific details from their DESCRIPTION to show you read it.
    - Paragraph 3: Call to action - invite them to chat on a quick 15 min call.

    You MUST mention at least 2 specific details from their request.
    Keep it friendly, professional and human. Not salesy.

    Lead Details:
    - Name: {name}
    - Location: {location}
    - Service: {service}
    - Description: {description}

    Write the 3 paragraphs directly. No labels. No "Paragraph 1:" etc.
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role" : "user" ,
                "content" : promt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    
    return response.choices[0].message.content

def scrape_leads():
    leads = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Login
        print("Logging in...")
        page.goto("https://www.bark.com/en/gb/login/")
        time.sleep(random.uniform(1.5 , 3))

        for char in os.getenv("EMAIL"):
            page.type('#loginId', char)
            time.sleep(random.uniform(0.05, 0.15))
        time.sleep(random.uniform(1.5 , 3))

        for char in os.getenv("PASSWORD"):
            page.type('#password', char)
            time.sleep(random.uniform(0.05, 0.15))

        time.sleep(random.uniform(1.5 , 3))
        page.click('button.blue')
        page.wait_for_url("**/sellers/home/**", timeout=15000)
        print("Logged in! ✅")

        print("Going to leads page...")
        page.goto("https://www.bark.com/sellers/dashboard/")
        time.sleep(random.uniform(1.5 , 3))

        print("Scrolling to load more leads...")
        for i in range(3):
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(random.uniform(1.5, 2.5))
        print("Scrolling done!")

        lead_cards = page.query_selector_all('.leads-list-item-card')
        print(f"Found {len(lead_cards)} leads!")
        
        for i, card in enumerate(lead_cards[:10], start=1):
            print(f"Scraping lead {i}...")
            try:
                name = card.query_selector('.lead-name').inner_text() if card.query_selector('.lead-name') else "N/A"
                location = card.query_selector('.lead-location').inner_text() if card.query_selector('.lead-location') else "N/A"
                service = card.query_selector('.lead-service').inner_text() if card.query_selector('.lead-service') else "N/A"
                description = card.query_selector('.lead-description').inner_text() if card.query_selector('.lead-description') else "N/A"
                
                leads.append({
                    "name": name,
                    "location": location,
                    "service": service,
                    "description": description
                })
            except Exception as e:
                pass
                
    return leads

def main():
    print("=" * 50)
    print("🤖 BARK.COM AI LEAD AGENT")
    print("=" * 50 + "\n")

    print("📋 STEP 1 - Scraping leads from Bark.com...")
    print("-" * 50)
    leads = scrape_leads()
    print(f"✅ Successfully scraped {len(leads)} leads!")

    print("\n🧠 STEP 2 - Analyzing leads with AI...")
    print("-" * 50 + "\n")
    
    results = []
    
    high_count = 0
    med_count = 0
    low_count = 0
    pitch_count = 0

    for i, lead in enumerate(leads, start=1):
        print(f"[{i}/{len(leads)}] Analyzing - {lead['name']} from {lead['location']}")
        print(f"  Service: {lead['service']}")
        
        try:
            score_data = score_lead(lead['name'], lead['location'], lead['service'], lead['description'])
            score = score_data.get('score', 0)
            reason = score_data.get('reason', '')
            lead['score'] = score
            lead['reason'] = reason
        except Exception as e:
            print(f"  Error parsing score: {e}")
            score = 0
            reason = "Error scoring"
            lead['score'] = score
            lead['reason'] = reason
            
        if score > 0.7:
            score_icon = "🔥"
            high_count += 1
        elif score >= 0.4:
            score_icon = "⭐"
            med_count += 1
        else:
            score_icon = "❌"
            low_count += 1
            
        print(f"  Score: {score} {score_icon}")
        print(f"  Reason: {reason}")
        
        print("  Generating pitch...")
        pitch = generate_pitch(lead['name'], lead['location'], lead['service'], lead['description'])
        lead['pitch'] = pitch
        pitch_count += 1
        results.append(lead)
        print("  Pitch: ✅ Generated!\n")
        print(f"--- PITCH FOR {str(lead['name']).upper()} ---")
        print(pitch)
        print()

    print("\n💾 STEP 3 - Saving results...")
    print("-" * 50)
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)
    print("✅ Saved to results.json\n")

    print("=" * 50)
    print("📊 SUMMARY REPORT")
    print("=" * 50)
    print(f"Total leads analyzed: {len(leads)}")
    print(f"🔥 High quality leads: {high_count}")
    print(f"⭐ Medium quality:     {med_count}")
    print(f"❌ Low quality:        {low_count}")
    print(f"📝 Pitches generated:  {pitch_count}\n")
    print("✅ Agent completed successfully!")

if __name__ == "__main__":
    main()
