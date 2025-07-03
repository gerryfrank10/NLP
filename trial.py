from vllm import LLM, SamplingParams

llm = LLM(model='mistralai/Mistral-7B-v0.1', tensor_parallel_size=1)
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)
outputs = llm.generate(
    "What is capital of Tanzania?",
    sampling_params=sampling_params)
for output in outputs:
    print(output.outputs[0].text)