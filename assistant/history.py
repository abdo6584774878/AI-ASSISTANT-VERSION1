from google.genai import types


def memory_to_gemini_history(messages):
    history = []

    for role, message in messages:
        if role == "user":
            gemini_role = "user"
        elif role == "assistant":
            gemini_role = "model"
        else:
            raise ValueError(f"Invalid message role : {role}")
            
        content = types.Content(
            role=gemini_role,
            parts=[
                types.Part(text=message)
            ]
        )

        history.append(content)

    return history