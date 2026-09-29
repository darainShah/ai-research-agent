from app.generation.llm import LLM


llm = LLM()


context = """
The model was trained using Indian air quality data.
The dataset contains observations collected from multiple
Indian cities.
"""


question = "What data was used to train the model?"


answer = llm.generate(
    question=question,
    context=context
)


print("\n==============================")
print("ANSWER")
print("==============================")

print(answer)