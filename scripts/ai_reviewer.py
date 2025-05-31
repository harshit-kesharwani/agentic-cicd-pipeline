import os
import openai
from git import Repo

openai.api_key = os.getenv("OPENAI_API_KEY")
repo = Repo(".")

def get_code_diff():
    diff = repo.git.diff('HEAD~1')
    return diff if diff else "No changes."

def review_code(diff_text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a senior code reviewer. Review code diffs, provide a score (0-100), suggestions, and optionally improved code."},
            {"role": "user", "content": f"Review this code diff:\n{diff_text}"}
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    diff = get_code_diff()
    review = review_code(diff)
    print("AI Review Output:\n", review)
    with open("ai_review_output.txt", "w") as f:
        f.write(review)

if __name__ == "__main__":
    main()
