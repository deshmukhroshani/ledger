from google import genai
from google.genai import types
import re

def generate_quiz(demographics):
    prompt = (
        f"Make me a financial literacy quiz for someone with the following demographics:\n"
        f"- Country: {demographics['Country']}\n"
        f"- Age: {demographics['Age Range']}\n"
        f"- Education: {demographics['Education']}\n"
        f"- Employment Status: {demographics['Employment Status']}\n"
        f"- Estimated Annual Income: {demographics['Estimated Income']}\n\n"
        f"For each of the following sections, generate 3 yes/no questions. "
        f"Format the output so that each section starts with its name as a header, followed by the 3 questions. "
        f"Each question should be answerable with Yes or No. "
        f"The format should be as follows:\n"
        f"## Budgeting and Saving\n"
        f"1. [Question text]\n"
        f"2. [Question text]\n"
        f"3. [Question text]\n"
        f"## Taxes\n"
        f"...\n"
        f"## Investing\n"
        f"...\n"
        f"## Debt Management\n"
        f"...\n"
        f"Do not provide answers, only the questions. "
        f"Questions should be suitable for radio button selection (Yes/No) in a web form."
    )

    client = genai.Client(
        vertexai=True,
        project="hack-team-off-the-ledger",
        location="global",
    )

    model = "gemini-2.5-flash-lite"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=4096,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        output += chunk.text
    return output


def generate_roadmap(demographics, quiz_responses):
    prompt = (
        f"Based on the following user demographics and quiz responses, provide a detailed and actionable financial literacy roadmap "
        f"that focuses on their weak areas. The roadmap should always be broken down by these topics: Budgeting, Taxes, Investing, and Debt Management. "
        f"For each topic, include 2 beginner-friendly steps. Each step should include:\n"
        f"- A short label\n"
        f"- A 1–2 sentence summary\n"
        f"- 1–2 external resources (article, video, or site) in Markdown link format\n\n"
        f"Return in this format:\n"
        f"## Budgeting\n"
        f"1. Label: short label\n"
        f"   Summary: explanation...\n"
        f"   Resources:\n"
        f"   - [title](https://example.com)\n"
        f"   - [title](https://example2.com)\n"
        f"## Taxes\n"
        f"...\n"
    )

    client = genai.Client(
        vertexai=True,
        project="hack-team-off-the-ledger",
        location="global",
    )

    model = "gemini-2.5-flash-lite"
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    config = types.GenerateContentConfig(
        temperature=0.9,
        top_p=0.95,
        max_output_tokens=4096,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    output = ""
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=config):
        output += chunk.text

    # --- Parse structured output ---
    roadmap = {}
    section_pattern = r"##\s*(.*?)\n(.*?)(?=\n##|$)"
    step_pattern = r"\d+\.\s*Label:\s*(.*?)\n\s*Summary:\s*(.*?)\n\s*Resources:\s*((?:\s*-\s*\[.*?\]\(.*?\)\n?)*)"

    subtitle_map = {
        "Budgeting": "Budgeting & Emergency Fund",
        "Taxes": "Tax Filing & Optimization",
        "Investing": "Stocks, Bonds & Portfolio Building",
        "Debt Management": "Loans & Repayment Strategies"
    }

    for topic, block in re.findall(section_pattern, output, re.DOTALL):
        topic = topic.strip()
        roadmap[topic] = {
            "subtitle": subtitle_map.get(topic, ""),
            "topics": [],
            "status": "In Progress"
        }

        for label, summary, resources_raw in re.findall(step_pattern, block.strip(), re.DOTALL):
            resources = re.findall(r"- \[(.*?)\]\((.*?)\)", resources_raw)
            roadmap[topic]["topics"].append({
                "label": label.strip(),
                "summary": summary.strip(),
                "resources": resources
            })

    return roadmap
