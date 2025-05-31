from openai import OpenAI
import os

from git import Repo
import subprocess

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
repo = Repo(".")



def get_code_diff():
    repo = Repo(".")
    commits = list(repo.iter_commits('HEAD', max_count=2))
    
    if len(commits) < 2:
        # If there's only one commit, get the whole file tree as "added"
        diff = repo.git.diff('--staged')
        if not diff:
            diff = subprocess.run(['git', 'show'], capture_output=True, text=True).stdout
    else:
        diff = repo.git.diff('HEAD~1')
        
    return diff


import os
from openai import AzureOpenAI

def review_code(diff_text):
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-02-15-preview",  # Use the correct API version you're working with
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
    )

    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],  # Deployment name, not model ID
        messages=[
            {
                "role": "system",
                "content": "You are a senior code reviewer. Review code diffs, provide a score (0-100), suggestions, and optionally improved code."
            },
            {
                "role": "user",
                "content": f"Review this code diff:\n{diff_text}"
            }
        ]
    )

    return response.choices[0].message.content



def main():
    diff = get_code_diff()
    review = review_code(diff)
    print("AI Review Output:\n", review)
    with open("ai_review_output.txt", "w") as f:
        f.write(review)

if __name__ == "__main__":
    main()
