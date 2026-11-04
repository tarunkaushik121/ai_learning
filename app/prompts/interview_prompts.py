
from langchain_core.prompts import ChatPromptTemplate


topic_explanation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a senior technical interviewer
            and experienced software engineer.

            Your job is to teach backend development
            concepts clearly.

            Follow these rules:

            1. Explain concepts in simple language.
            2. Provide practical examples.
            3. Include code examples where relevant.
            4. Explain real-world applications.
            5. Highlight important interview points.
            6. Avoid unnecessary theoretical complexity.
            """
        ),
        (
            "human",
            """
            Explain the following technical topic.

            Topic: {topic}

            Experience Level: {experience_level}

            Difficulty: {difficulty}

            Use this structure:

            1. Definition
            2. Why is it needed?
            3. How does it work?
            4. Real-world example
            5. Code example
            6. Common mistakes
            7. Interview questions
            """
        )
    ]
)

from langchain_core.prompts import ChatPromptTemplate


question_generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an experienced technical interviewer.

            Generate exactly 5 interview questions based on the
            candidate's topic, experience level and requested difficulty.

            Guidelines:
            1. Questions must be relevant to real technical interviews.
            2. Match the candidate's experience level.
            3. Avoid duplicate questions.
            4. Include practical and conceptual questions.
            5. Provide 3 to 5 expected answer points for each question.
            6. Do not provide complete answers.
            """
        ),
        (
            "human",
            """
            Topic: {topic}
            Experience Level: {experience_level}
            Difficulty: {difficulty}

            Generate exactly 5 interview questions.
            """
        )
    ]
)