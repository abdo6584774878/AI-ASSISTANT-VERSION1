from google.genai import types


def memory_to_gemini_history(messages):
    history = []

    for role, message in messages:
        gemini_role = "model" if role == "assistant" else "user"

        content = types.Content(
            role=gemini_role,
            parts=[
                types.Part(text=message)
            ]
        )

        history.append(content)

    return history