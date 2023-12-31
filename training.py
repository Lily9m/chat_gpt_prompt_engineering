import openai
import os
import pandas as pd
import numpy as np

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Principle 1: Write clear and specific instructions
text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""
response = get_completion(prompt)
print(response)

#Tactic 2: Ask for a structured output
#JSON HTML

prompt = f"""
Generate a list of three made-up book titles along \
with their authors and genres.
Provide them in JSON format with the following keys:
book_id,title,author,genre.
"""
response = get_completion(prompt)
print(response)

text_1 = f"""
Making a cup of tea is easy! First, you need to get some \
water boiling. while that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \
hot enough, just pour it over the tea bag. \
Let it sit for a bit so the tea can steep. After a\
few minutes, take out the tea bag. If you \
like, you can add some sugar or milk to taste. \
And that's it! You've got yourself a delicious \
cup of tea to enjoy. 
"""
prompt = f"""
You will be provided with text delimited by triple quotes.
If it contains a sequence of instructions, \
re-write those instructions in the following format:

Step 1 - ...
Step 2 - ...
...
Step N - ...
if the text does not contain a sequence of instructions, \
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""
response =get_completion(prompt)
print("Completion for Text 1:")
print(response)

#Tactic 4: Few shot prompting 
prompt = f"""
Your task is to answer in a consistent style. 
<child>: Teach me about patience. 
<grandparent>: The river that carves the deepest\
valley flows from a modest spring; the \
grandest symphony or originates from a single note; \
the most intricate tapestry begins with a solitery thread. 

<child>: Teach me about resillience.
"""
response = get_completion(prompt)
print(response)

#Principle2: Give the model time to "think"
#Tactic 1: Specify the steps required to complete a task 

text = f"""
In a charming village, siblings Jack and Jill set out on \
a quest to fetch water from a hilltop \
well. As they climbed, singing joyfully, misfortune \
struck-Jack tripped on a stone and tumbled \
down the hill, with jill following suit. \
Though slightly battered, the pair returned home to \
comforting embraces. Despite the mishap,\
their adventures spirits remained undimmed, and they \
continued exploring with delight.
"""

prompt_1 = f"""
Perform the following actions:
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French Summary.
4 - Output a Json object that contains the following\
keys: french summary, num_names.prompt

Separate your answers with line breaks.prompt

Text:
'''{text}'''
"""
response = get_completion(prompt_1)
print("Completion for prompt 1:")
print(response)

#Ask for output in a specified format

prompt_2 = f"""
Your task is to perform the following actions:
1-Summarize the following text delimited by <> with 1 sentence. 
2- Translate the summary into French.
3- List each name in the French summary. 
4- Output a Json object that contains the following keys: french_summary, num_names.prompt_1

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""
response = get_completion(prompt_2)
print("\nCompletion for prompt 2:")
print(response)

