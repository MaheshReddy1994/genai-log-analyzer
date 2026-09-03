import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def main():
    log = "Permission denied: cannot access /var/log/syslog"
    prompt = f"""
    You are a Linux system administrator.
    Analyze the following log
    {log}
    Identify the root cause of the error and provide a solution.
    """
    #print(prompt)
    print("Sending request...")

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        #input="Say hello in one word."
        input = prompt
    )
    
    print("Response received!")

    print(interaction.output_text)
    


if __name__ == "__main__":
    main()