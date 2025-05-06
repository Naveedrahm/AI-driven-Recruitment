import os
import pandas as pd
import re

# Helpers to extract sections
def extract_section(text, section_name):
    pattern = rf"{section_name}:(.*?)(\n[A-Z][a-z]+:|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip().lower() if match else ""

# Simple keyword match function
def keyword_match_score(text_section, keywords):
    if not text_section:
        return 0
    score = 0
    for kw in keywords:
        if kw in text_section:
            score += 1
    return min(score, 10)

# Load job description
with open('jobDescription.txt', 'r', encoding='utf-8') as f:
    jd_text = f.read().lower()

#Defined the words for looking
required_skills = ['python', 'excel', 'data visualization', 'machine learning']
preferred_education = ['engineering', 'computer science', 'environmental science']
desired_experience = ['internship', 'project', 'reporting', 'sustainability']

# Process resumes
resumes_folder = 'resumes'
results = []

for filename in os.listdir(resumes_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(resumes_folder, filename), 'r', encoding='utf-8') as f:
            text = f.read().lower()

        skills_text = extract_section(text, 'skills')
        education_text = extract_section(text, 'education')
        experience_text = extract_section(text, 'experience')

        skill_score = keyword_match_score(skills_text, required_skills)
        edu_score = keyword_match_score(education_text, preferred_education)
        exp_score = keyword_match_score(experience_text, desired_experience)
        total = skill_score + edu_score + exp_score

        results.append({
            "filename": filename,
            "skill_score": skill_score,
            "education_score": edu_score,
            "experience_score": exp_score,
            "total_score": total
        })
with open('results/scores.txt', 'w', encoding='UTF-8') as txt_file:    
    for row in results:
        txt_file.write(
            f"{row['filename']} - Skill: {row['skill_score']}, "
            f"Education: {row['education_score']}, "
            f"Experience: {row['experience_score']}, "
            f"Total: {row['total_score']}\n"
        )
# Save results
os.makedirs('results', exist_ok=True)
df = pd.DataFrame(results)
df.to_csv('results/scores.csv', index=False)
print("Done! Scores saved to results/scores.csv.")

