import os
from pathlib import Path

# Load SARVAM_API_KEY from this project's .env without extra dependencies.
for line in (Path(__file__).with_name(".env").read_text(encoding="utf-8").splitlines()):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip('"').strip("'"))

api_key = os.environ.get("SARVAM_API_KEY")
if not api_key:
    raise SystemExit("SARVAM_API_KEY is empty. Add your key to .env, then run this script again.")

from sarvamai import SarvamAI

client = SarvamAI(api_subscription_key=api_key)
response = client.chat.completions(
    model="sarvam-105b-conversations",
    messages=[{"role": "user", "content": "Reply with a brief greeting."}],
)
print(response.choices[0].message.content)
