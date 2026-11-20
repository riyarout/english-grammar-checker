import gradio as gr
import requests

def check_grammar(text):
    if not text.strip():
        return "Please enter a sentence.", ""

    try:
        response = requests.post(
            "https://api.languagetool.org/v2/check",
            data={"text": text, "language": "en-US"},
            timeout=30
        )
        response.raise_for_status()
        matches = response.json()["matches"]

        corrected = text

        for match in sorted(matches, key=lambda x: x["offset"], reverse=True):
            if match["replacements"]:
                start = match["offset"]
                end = start + match["length"]
                replacement = match["replacements"][0]["value"]
                corrected = corrected[:start] + replacement + corrected[end:]

        suggestions = ""
        for i, match in enumerate(matches, 1):
            suggestions += f"{i}. {match['message']}\n"
            if match["replacements"]:
                suggestions += "Suggestion: " + match["replacements"][0]["value"] + "\n\n"

        if not matches:
            suggestions = "No grammar mistakes found!"

        return corrected, suggestions

    except Exception as e:
        return "Unable to check grammar.", str(e)


app = gr.Interface(
    fn=check_grammar,
    inputs=gr.Textbox(lines=5, label="Enter Your Sentence"),
    outputs=[
        gr.Textbox(label="Corrected Sentence"),
        gr.Textbox(label="Grammar Suggestions")
    ],
    title="AI-Based English Grammar Checker",
    description="Check English grammar and get corrections instantly."
)

app.launch(server_name="0.0.0.0", server_port=7860)
