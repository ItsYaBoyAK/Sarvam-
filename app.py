import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import gradio as gr
from sarvamai import SarvamAI

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
DATA_FILE = ROOT / "grievances.json"

# Read .env without adding python-dotenv as a dependency.
if ENV_FILE.exists():
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and "=" in line:
            name, value = line.split("=", 1)
            if name.strip() == "SARVAM_API_KEY" and not os.environ.get(name.strip()):
                os.environ[name.strip()] = value.strip().strip('"').strip("'")

API_KEY = os.environ.get("SARVAM_API_KEY")
MODEL = "sarvam-105b-conversations"

CPGRAMS_HOME = "https://pgportal.gov.in/V7/Home"
CPGRAMS_GUIDELINES = (
    "https://www.pgportal.gov.in/Home/OtherGuidlines"
)

SYSTEM_PROMPT = f"""
You help citizens prepare clear, factual draft grievances for possible submission
through India's CPGRAMS portal. You are a drafting assistant, not a government
officer, lawyer, or CPGRAMS integration.

Return a concise, well-structured draft with:
1. Suggested subject
2. Department / authority (mark as a suggestion; explain uncertainty)
3. Problem statement
4. Facts and timeline (only what the citizen supplied)
5. Action requested / desired remedy
6. Missing information the citizen should add
7. Suggested category/tags
8. Evidence and citations

Do not invent dates, names, amounts, events, laws, rules, department jurisdiction,
registration numbers, or sources. Separate allegations from verified facts.
Do not imply the complaint has been filed or that the department tag is official.
If the complaint lacks details, identify the gaps instead of guessing.
Cite official sources only when relevant and only for claims those sources support.
The verified official references available for general CPGRAMS process/scope are:
- CPGRAMS portal: {CPGRAMS_HOME}
- CPGRAMS policy guidelines page: {CPGRAMS_GUIDELINES}
Do not use these sources as evidence that the citizen's allegations are true.
If you cannot verify a specific legal or departmental claim from the supplied
information, say it needs verification. Keep the final draft suitable for citizen review.
"""

def read_records():
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def write_records(records):
    DATA_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def get_client():
    if not API_KEY:
        raise gr.Error(
            "SARVAM_API_KEY is missing. Add your real key to .env, save it, "
            "and restart this app. Do not paste it into the chat."
        )
    return SarvamAI(api_subscription_key=API_KEY)

def transcribe_audio(audio_path):
    if not audio_path:
        return ""
    response = get_client().speech_to_text.transcribe(
        file=audio_path,
        model="saaras:v4",
        mode="transcribe",
    )
    transcript = getattr(response, "transcript", None)
    if not transcript:
        raise gr.Error("Sarvam returned no transcript. Try a clearer/shorter recording.")
    return transcript

def make_draft(complaint):
    response = get_client().chat.completions(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": complaint},
        ],
        max_tokens=1800,
    )
    return response.choices[0].message.content or "No draft returned."

def draft_grievance(typed_text, audio_path):
    typed_text = (typed_text or "").strip()
    transcript = transcribe_audio(audio_path) if audio_path else ""
    complaint = transcript or typed_text
    if not complaint:
        raise gr.Error("Enter a complaint or upload a voice recording.")
    draft = make_draft(complaint)
    record_id = uuid.uuid4().hex[:10].upper()
    record = {
        "id": record_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "Draft created",
        "original_complaint": complaint,
        "draft": draft,
        "updates": [],
    }
    records = read_records()
    records.append(record)
    write_records(records)
    sources = (
        "\n\n---\n### Verified official references\n"
        f"- [CPGRAMS portal]({CPGRAMS_HOME}) — official portal and general process.\n"
        f"- [CPGRAMS policy guidelines]({CPGRAMS_GUIDELINES}) — official policy guidance index.\n\n"
        "**Important:** These links are general official references, not proof of the specific allegations. "
        "Review every detail and department suggestion before submitting. This app does not submit to CPGRAMS."
    )
    return complaint, draft + sources, record_id, f"Saved locally. Tracking ID: `{record_id}`"

def list_tracking():
    records = read_records()
    if not records:
        return "No grievances saved yet."
    lines = ["| Tracking ID | Created (UTC) | Status |", "|---|---|---|"]
    for item in reversed(records[-100:]):
        lines.append(
            f"| {item.get('id','')} | {item.get('created_at','')[:19]} | {item.get('status','')} |"
        )
    return "\n".join(lines)

def get_record(record_id):
    wanted = (record_id or "").strip().upper()
    for item in read_records():
        if item.get("id", "").upper() == wanted:
            update_text = "\n".join(
                f"- {u.get('at','')[:19]} UTC — {u.get('status','')}: {u.get('note','')}"
                for u in item.get("updates", [])
            ) or "No updates yet."
            return (
                f"### {item['id']} — {item.get('status','')}\n\n"
                f"**Created:** {item.get('created_at','')}\n\n"
                f"**Original complaint / transcript**\n\n{item.get('original_complaint','')}\n\n"
                f"**Draft**\n\n{item.get('draft','')}\n\n"
                f"**Lifecycle updates**\n\n{update_text}"
            )
    return "Tracking ID not found in this app's local records."

def update_status(record_id, status, note):
    wanted = (record_id or "").strip().upper()
    records = read_records()
    for item in records:
        if item.get("id", "").upper() == wanted:
            item["status"] = status
            item.setdefault("updates", []).append({
                "at": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "note": (note or "").strip(),
            })
            write_records(records)
            return f"Updated {wanted}: {status}\n\n{get_record(wanted)}"
    return "Tracking ID not found. Create a draft first."

with gr.Blocks(title="Grievance Drafter") as demo:
    gr.Markdown(
        "# Grievance Drafter\n"
        "Turn a spoken or typed citizen complaint into a structured draft for review. "
        "This MVP stores records locally and does **not** file grievances with CPGRAMS."
    )
    with gr.Tab("Draft a grievance"):
        typed = gr.Textbox(
            label="Citizen complaint (typed)",
            placeholder="Describe what happened, where, when, and what resolution you want…",
            lines=6,
        )
        audio = gr.Audio(
            label="Or record/upload a voice complaint",
            sources=["microphone", "upload"],
            type="filepath",
        )
        make_button = gr.Button("Transcribe and draft", variant="primary")
        transcript_out = gr.Textbox(label="Transcript / complaint used", lines=5)
        draft_out = gr.Markdown()
        tracking_id_out = gr.Textbox(label="Local tracking ID", interactive=False)
        save_status = gr.Markdown()
        make_button.click(
            draft_grievance,
            inputs=[typed, audio],
            outputs=[transcript_out, draft_out, tracking_id_out, save_status],
        )
    with gr.Tab("Track and update"):
        refresh_button = gr.Button("Refresh saved grievances")
        list_out = gr.Markdown()
        refresh_button.click(list_tracking, outputs=list_out)
        record_id = gr.Textbox(label="Local tracking ID")
        view_button = gr.Button("View record")
        record_out = gr.Markdown()
        view_button.click(get_record, inputs=record_id, outputs=record_out)
        gr.Markdown(
            "Add a status update when you receive one outside this app. "
            "Updates are user-entered and are not fetched from CPGRAMS automatically."
        )
        status = gr.Dropdown(
            choices=[
                "Draft created", "Ready for citizen review", "Submitted by citizen",
                "Acknowledged", "In progress", "Resolved", "Appeal needed", "Closed"
            ],
            value="Ready for citizen review",
            label="New status",
        )
        note = gr.Textbox(label="Update note (optional)", lines=2)
        update_button = gr.Button("Save status update")
        update_out = gr.Markdown()
        update_button.click(
            update_status,
            inputs=[record_id, status, note],
            outputs=update_out,
        )
    gr.Markdown(
        "---\n"
        "**Privacy:** Do not enter unnecessary sensitive personal information. "
        "Drafts and transcripts are saved in `grievances.json` on this computer. "
        "Restrict access to this file and do not commit it."
    )

if __name__ == "__main__":
    demo.launch()
