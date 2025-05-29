# core/recommendation_engine.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
import os

RESOURCE_CSV = "data/skill_learning_resources.csv"

def load_resource_data():
    if os.path.exists(RESOURCE_CSV):
        return pd.read_csv(RESOURCE_CSV)
    else:
        return pd.DataFrame(columns=[
            "skill", "platform", "title", "link",
            "duration_hrs", "difficulty", "source_type", "verified"
        ])

def search_google_learning_link(skill):
    print(f"🔍 Searching learning resource for: {skill}...")
    encoded_skill = urllib.parse.quote_plus(skill.lower())

    # Curated platforms with search URLs
    curated_platforms = {
        "FreeCodeCamp": f"https://www.google.com/search?q=site%3Afreecodecamp.org+{encoded_skill}",
        "KhanAcademy": f"https://www.google.com/search?q=site%3Akhanacademy.org+{encoded_skill}",
        "Coursera": f"https://www.coursera.org/search?query={encoded_skill}",
        "edX": f"https://www.edx.org/search?q={encoded_skill}",
        "Udemy": f"https://www.udemy.com/courses/search/?q={encoded_skill}",
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Step 1: Try FreeCodeCamp and KhanAcademy (free learning)
    for platform, url in curated_platforms.items():
        print(f"🔗 Trying: {platform}")
        try:
            if "google.com/search" in url:
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                search_results = soup.select("a")
                for link in search_results:
                    href = link.get("href")
                    if href and "url?q=" in href:
                        clean_link = href.split("url?q=")[1].split("&")[0]
                        if platform.lower() in clean_link:
                            print(f"✅ Found {platform} link: {clean_link}")
                            return clean_link
            else:
                # Direct platform URLs — no scraping needed
                print(f"🔗 Using direct link from {platform}")
                return url
        except Exception as e:
            print(f"⚠️ Error searching {platform}: {e}")
            continue

    # Final fallback — Google search
    fallback = f"https://www.google.com/search?q=learn+{encoded_skill}"
    print(f"🔁 Fallback to: {fallback}")
    return fallback


def recommend_learning_paths(missing_skills):
    df = load_resource_data()
    recommendations = []

    for skill in missing_skills:
        candidates = df[df["skill"].str.lower() == skill.lower()]

        if not candidates.empty:
            # Rank: verified > free > shorter
            candidates["score"] = (
                candidates["verified"].fillna(False).astype(int) * 3 +
                (candidates["source_type"].str.lower() == "free").astype(int) * 2 +
                (1 / candidates["duration_hrs"].fillna(1000).astype(float).replace(0, 1))
            )

            top = candidates.sort_values(by="score", ascending=False).iloc[0]
            recommendations.append({
                "skill": skill,
                "platform": top.get("platform", "unknown"),
                "title": top.get("title", "unknown"),
                "link": top.get("link", "unknown"),
                "duration_hrs": top.get("duration_hrs", "unknown"),
                "difficulty": top.get("difficulty", "unknown"),
                "source_type": top.get("source_type", "unknown"),
                "verified": top.get("verified", False)
            })
        else:
            # No match — fallback to Google
            scraped_link = search_google_learning_link(skill)
            new_entry = {
                "skill": skill,
                "platform": "Google Search",
                "title": f"Learn {skill}",
                "link": scraped_link,
                "duration_hrs": "",
                "difficulty": "",
                "source_type": "search",
                "verified": False
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(RESOURCE_CSV, index=False)
            recommendations.append(new_entry)
            time.sleep(random.uniform(1.5, 2.5))  # Polite scraping

    return recommendations
