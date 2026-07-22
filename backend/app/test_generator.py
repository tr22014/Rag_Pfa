from services.generator import Generator

generator = Generator()

context = """
The goal of this internship is to build an intelligent platform
that centralizes enterprise knowledge,
indexes documents automatically,
and answers questions in natural language.
"""

question = "What is the objective of the internship?"

answer = generator.generate(
    question=question,
    context=context
)

print(answer)