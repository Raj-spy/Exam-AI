from langchain_core.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} multiple-choice question about {topic}.\n\n"
        "Return ONLY valid JSON. Do not include explanations, markdown, backticks, or any extra text.\n"
        "Your JSON must follow this exact schema with these fields:\n"
        "- question: a clear, specific question string\n"
        "- options: an array of exactly 4 possible answer strings\n"
        "- correct_answer: one of the options that is correct\n\n"
        "Example output:\n"
        '[{\n'
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        '}]\n\n'
        "Important: the entire response must be parsable as JSON."
    ),
    input_variables=["topic", "difficulty"]
)

fill_blank_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} fill-in-the-blank question about {topic}.\n\n"
        "Return ONLY valid JSON. Do not include explanations, markdown, backticks, or any extra text.\n"
        "Your JSON must follow this schema:\n"
        "- question: a sentence containing _____ where the blank goes\n"
        "- answer: the correct word or phrase\n\n"
        "Example output:\n"
        '[{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}]\n\n'
        "Important: the entire response must be parsable as JSON."
    ),
    input_variables=["topic", "difficulty"]
)