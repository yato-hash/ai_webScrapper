from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (  # we need to give llm some more detail so that it knows what to do with that as well as the dom content that we're about to pass it
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model='llama3')#

def parse_with_ollama(dom_chunks,parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model # first we will go to the prompt and then we will go to the model

    parsed_results = [] # grab the results and store them in this list

    for i, chunk in enumerate(dom_chunks,start=1):# enumerate is nothing it's just going to iterate over dom_chunks and return objects containing the index and the value at dom_chunks[idx]
        response = chain.invoke(
            {"dom_content" : chunk , "parse_description":parse_description}
        ) #call the llm , need to pass variable and they need to match the variables in the template

        print(f"Parsed batch {i} of {len(dom_chunks)}")# logging information , b/c the process will take time , so need some type of output to know something is going on
        parsed_results.append(response)
    
    return '\n'.join(parsed_results)