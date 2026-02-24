from src.models.question_schemas import MCQQuestion, FillBlankQuestion
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException

import re
import json


class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self, prompt, topic, difficulty):
        """
        Invoke LLM, extract first valid JSON object,
        sanitize it, and return parsed dict.
        """

        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(
                    f"Generating question for topic {topic} with difficulty {difficulty}"
                )

                response = self.llm.invoke(
                    prompt.format(topic=topic, difficulty=difficulty)
                )

                raw = response.content
                cleaned = raw.strip()

                self.logger.info(f"RAW LLM OUTPUT:\n{raw}")

                # Extract first JSON object
                match = re.search(r"\{.*\}", cleaned, re.DOTALL)
                if not match:
                    raise ValueError("No JSON object found in LLM response")

                json_str = match.group(0)

                # Fix invalid escape sequences
                json_str = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", json_str)

                data = json.loads(json_str)

                return data

            except Exception as e:
                self.logger.error(f"Generation attempt failed: {str(e)}")

                if attempt == settings.MAX_RETRIES - 1:
                    raise CustomException(
                        f"Generation failed after {settings.MAX_RETRIES} attempts",
                        e,
                    )

    # ------------------ MCQ ------------------

    def generate_mcq(self, topic: str, difficulty: str = "medium") -> MCQQuestion:
        try:
            data = self._retry_and_parse(mcq_prompt_template, topic, difficulty)

            question = MCQQuestion(**data)

            # Relaxed validation
            options_normalized = [opt.strip().lower() for opt in question.options]

            if len(options_normalized) != 4:
                raise ValueError("Invalid MCQ Structure")

            correct_normalized = question.correct_answer.strip().lower()

            if correct_normalized not in options_normalized:
                raise ValueError("Correct answer mismatch")

            self.logger.info("Generated valid MCQ")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException("MCQ generation failed", e)

    # ------------------ Fill in Blank ------------------

    def generate_fill_blank(self, topic: str, difficulty: str = "medium") -> FillBlankQuestion:
        try:
            data = self._retry_and_parse(fill_blank_prompt_template, topic, difficulty)

            question = FillBlankQuestion(**data)

            if "___" not in question.question:
                raise ValueError("Fill in blanks should contain '___'")

            self.logger.info("Generated valid Fill in Blank question")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate fill blank: {str(e)}")
            raise CustomException("Fill in blanks generation failed", e)