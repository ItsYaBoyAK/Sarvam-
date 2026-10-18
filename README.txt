Grievance Drafter MVP

Run on Windows:
1. Extract these files into E:\Akshath\Sarvam (or your chosen project folder).
2. Add your real key to .env: SARVAM_API_KEY=your_key
3. Open PowerShell in that folder and run:
   python -m pip install -r requirements.txt
   python app.py
4. Open the local Gradio URL shown in the terminal.

Features:
- Typed complaints and voice recording/upload.
- Sarvam Saaras v4 transcription and Sarvam-105B Conversations drafting.
- Structured draft, suggested department/tags, missing details, and official CPGRAMS reference links.
- Local tracking IDs and manually entered lifecycle updates in grievances.json.

Important limitations:
- Does not submit to CPGRAMS or retrieve official status automatically.
- Tracking is local and updates are manually entered.
- Citations are limited to official CPGRAMS reference links supplied in the app; the app does not verify case allegations or dynamically research legal claims.
- Keep .env and grievances.json private. Do not commit either file.
