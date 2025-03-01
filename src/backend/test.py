from chain_composer import ChainComposer

from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from chain_composer import ChainComposer

# Load the API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


# Step 1: Define the output models
class FirstDerivative(BaseModel):
    first_derivative: str


# Here we are telling the LLM for the first layer we want output in the following format:
# {
#     "first_derivative": "<answer>"
# }


# Step 2: Define the second layer output model
class SecondDerivative(BaseModel):
    second_derivative: str


# Here we are telling the LLM for the second layer we want output in the following format:
# {
#     "second_derivative": "<answer>"
# }

# Step 3: Create the prompts
# Define the first layer system message
first_derivative_system_message = """
You are a helpful assistant, who takes the first derivative of a function and returns the result in the following format:

{{
    "first_derivative": "<answer>"
}}

Note: You should always return json. Do not include the markdown json format, just return the json.
"""

# Define the second layer system message
second_derivative_system_message = """
You are a helpful assistant, who takes a second derivative and returns the result in the following format:

{{
    "second_derivative": "<answer>"
}}

Note: You should always return json. Do not include the markdown json format, just return the json.
"""

# Define the human message for the first layer
human_message = """
Equation:

{equation}
"""

# Define the human message for the second layer
human_message_2 = """
Original Equation:

{equation}

First Derivative:

{first_derivative}
"""

# Step 4: Create the chain
# Define the chain with the json parser
# Here we'll be using the json parser, but you can also use pydantic and string parsers
cp = ChainComposer(
    model="gemini-2.0-flash-thinking-exp-01-21",
    api_key=api_key,
)

cp.add_chain_layer(  # Add the first layer
    system_prompt=first_derivative_system_message,  # The system message for the layer
    human_prompt=human_message,  # The human message for the layer
    parser_type="json",  # The parser type for the layer
    pydantic_output_model=FirstDerivative,  # The output model for the layer
    output_passthrough_key_name="first_derivative",  # The key name for the output passthrough
).add_chain_layer(  # Add the second layer
    system_prompt=second_derivative_system_message,  # The system message for the layer
    human_prompt=human_message_2,  # The human message for the layer
    parser_type="json",  # The parser type for the layer
    pydantic_output_model=SecondDerivative,  # The output model for the layer
    output_passthrough_key_name="second_derivative_output",  # The key name for the output passthrough
)

# Run the chain by calling the `run()` method and passing in a dictionary of variables.
# Here we start running it by providing the `equation` variable. This will be used in the first and second layers' human prompts.
# The `output_passthrough_key_name` argument we passed in to the `add_chain_layer()` method will be used to
# insert new variables into this dictionary, thus allowing the flow of outputs into placeholder variables in the prompts.
result = cp.run({"equation": "2x^2 + 3x + 2"})

print(result)

# for a prettier output, you can import `json` and use `json.dumps()`
# print(json.dumps(result, indent=4))
