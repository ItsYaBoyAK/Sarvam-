# Grievance Drafter

An AI-powered grievance drafting assistant that helps citizens convert spoken or typed complaints into structured, clear, and formal administrative grievances suitable for review before submission through India's CPGRAMS portal.

## Features

- Voice Complaint Input: Record or upload a voice complaint.
- Speech-to-Text: Uses Sarvam AI Saaras v4 to transcribe speech.
- AI-Powered Drafting: Uses Sarvam AI's Sarvam-105B Conversations model to create structured grievance drafts.
- Structured Complaints: Organizes complaints into a subject, problem statement, facts, requested action, suggested department, and relevant tags.
- Missing Information Detection: Highlights details the citizen may need to provide.
- Official References: Provides links to official CPGRAMS resources for reference.
- Local Tracking: Generates tracking IDs and supports manually entered status updates.
- Simple Interface: Built using Python and Gradio.

## Tech Stack

- Python
- Gradio
- Sarvam AI API
- Saaras v4 Speech-to-Text
- Sarvam-105B Conversations
- JSON-based local storage

## Project Structure

    grievance-drafter/
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md

## Requirements

- Python 3.10 or a compatible version supported by the installed dependencies
- A Sarvam AI API key
- Internet connection for API requests

## Installation and Setup

1. Clone the repository:

   git clone https://github.com/YOUR_USERNAME/grievance-drafter.git

2. Navigate to the project directory:

   cd grievance-drafter

3. Install the dependencies:

   python -m pip install -r requirements.txt

4. Create a file named .env in the project directory.

5. Add your Sarvam AI API key:

   SARVAM_API_KEY=your_actual_api_key

6. Start the application:

   python app.py

7. Open the local Gradio URL displayed in your terminal.

## How to Use

1. Open the Grievance Drafter web interface.
2. Enter a complaint as text or record/upload a voice complaint.
3. Click "Transcribe and draft".
4. Review the transcript and generated grievance carefully.
5. Check the suggested department, requested action, and missing information.
6. Save the local tracking ID for future reference.
7. Use the tracking section to view the saved record and manually record updates.

## Official References

CPGRAMS Portal:
https://pgportal.gov.in/V7/Home

CPGRAMS Policy Guidelines:
https://www.pgportal.gov.in/Home/OtherGuidlines

Sarvam AI Documentation:
https://docs.sarvam.ai/

Speech-to-Text Documentation:
https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview

Chat Completion Documentation:
https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview

## Important Limitations

- This is an MVP and a drafting assistant, not an official government service.
- The application does not submit grievances to CPGRAMS.
- It does not automatically retrieve official complaint status.
- Tracking records and status updates are stored locally.
- Department recommendations and generated content may be incorrect and must be reviewed.
- Official reference links do not independently verify a citizen's allegations.
- The application should not be treated as legal advice.

## Security and Privacy

- Never commit your real API key or .env file to GitHub.
- Keep .env and grievances.json excluded using .gitignore.
- Do not enter unnecessary sensitive personal information.
- Local records may contain private complaint details; protect access to them.
- Before public deployment, implement appropriate authentication, access controls, and secure storage.

## Future Improvements

- Support for additional Indian languages.
- Editable transcripts and interactive follow-up questions.
- More accurate department recommendations backed by verified official sources.
- Downloadable grievance documents in PDF format.
- Database-backed storage and improved privacy controls.
- Automated tests and improved error handling.
- Official status integration if an authorized API becomes available.

## License

Choose and add an appropriate open-source license before distributing this project.

## Disclaimer

This project is intended to help citizens prepare and organize grievance drafts. It is not affiliated with or endorsed by the Government of India or CPGRAMS. Citizens should verify the generated information and submit grievances through the appropriate official channels themselves.
