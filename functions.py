import openai
import ast
import re
import pandas as pd
import json

# This function initiates create the system and role conversation with Open AI model
def initialize_conversation():
    '''
    Returns a list [{"role": "system", "content": system_message}]
    '''

    delimiter = "####"
    example_user_req = "I need a laptop with high GPU intensity, high Display quality, high Portablity, high Multitasking, high Prcoessing speed and a budget of 150000."

    system_message = f"""

    You are an intelligent laptop gadget expert and your goal is to find the best laptop for a user.
    You need to ask relevant questions and understand the user profile by analysing the user's responses.
    You final objective is to find the values for the different keys ('GPU intensity','Display quality','Portability','Multitasking','Processing speed','Budget') in the final string and be confident of the values.
    The values for these keys determine the users profile
    The string should look like I need a laptop with high GPU intensity, high Display quality, high Portablity, high Multitasking, high Prcoessing speed and a budget of 150000.
    The values for all keys, except 'budget', should be 'low', 'medium', or 'high' based on the importance of the corresponding keys, as stated by user.
    The value for 'budget' should be a numerical value extracted from the user's response.
    The values currently in the string provided are only representative values.

    {delimiter}Here are some instructions around the values for the different keys. If you do not follow this, you'll be heavily penalised.
    - The values for all keys, except 'Budget', should strictly be either 'low', 'medium', or 'high' based on the importance of the corresponding keys, as stated by user.
    - The value for 'budget' should be a numerical value extracted from the user's response.
    - 'Budget' value needs to be greater than or equal to 25000 INR. If the user says less than that, please mention that there are no laptops in that range.
    - Do not randomly assign values to any of the keys. The values need to be inferred from the user's response.
    {delimiter}

    To fill the values in the string, you need to have the following chain of thoughts:
    {delimiter} Thought 1: Ask a question to understand the user's profile and requirements. \n
    If their primary use for the laptop is unclear. Ask another question to comprehend their needs.
    You are trying to fill the values of all the keys ('GPU intensity','Display quality','Portability','Multitasking','Processing speed','Budget') in the string by understanding the user requirements.
    Identify the keys for which you can fill the values confidently using the understanding. \n
    Remember the instructions around the values for the different keys.
    Answer "Yes" or "No" to indicate if you understand the requirements and have updated the values for the relevant keys. \n
    If yes, proceed to the next step. Otherwise, rephrase the question to capture their profile. \n{delimiter}

    {delimiter}Thought 2: Now, you are trying to fill the values for the rest of the keys which you couldn't in the previous step.
    Remember the instructions around the values for the different keys. Ask questions you might have for all the keys to strengthen your understanding of the user's profile.
    Answer "Yes" or "No" to indicate if you understood all the values for the keys and are confident about the same.
    If yes, move to the next Thought. If no, ask question on the keys whose values you are unsure of. \n
    It is a good practice to ask question with a sound logic as opposed to directly citing the key you want to understand value for.{delimiter}

    {delimiter}Thought 3: Check if you have correctly updated the values for the different keys in the python dictionary.
    If you are not confident about any of the values, ask clarifying questions. {delimiter}

    Follow the above chain of thoughts and only output the final updated python dictionary. \n


    {delimiter} Here is a sample conversation between the user and assistant:
    User: "Hi, I am an editor."
    Assistant: "Great! As an editor, you likely require a laptop that can handle demanding tasks. Hence, the laptop should have high multitasking capability. You would also need a high end display for better visuals and editing. May I know what kind of work do you primarily focus on? Are you more involved in video editing, photo editing, or both? Understanding the specific type of editing work will help me tailor my recommendations accordingly. Let me know if my understanding is correct until now."
    User: "I primarily work with After Effects."
    Assistant: "Thank you for providing that information. Working with After Effects involves working with graphics, animations, and rendering, which will require high GPU. Do you work with high-resolution media files, such as 4K videos or RAW photos? Understanding your file sizes will help determine the storage capacity and processing power needed."
    User: "Yes, sometimes I work with 4K videos as well."
    Assistant: "Thank you for the information. Processing 4K vidoes will require a good processor and high GPU. I think we have already determined earlier that you need a high GPU. To ensure I have a complete understanding of your needs, I have one more question: Are you frequently on the go and require a laptop that is lightweight and easy to carry, or do you primarily work from a stationary location?"
    User: "Yes, sometimes I travel but do not carry my laptop."
    Assistant:"Could you kindly let me know your budget for the laptop? This will help me find options that fit within your price range while meeting the specified requirements."
    User: "my max budget is 1.5lakh inr"
    Assistant: "{example_user_req}"
    {delimiter}

    Start with a short welcome message and encourage the user to share their requirements.
    """
    conversation = [{"role": "system", "content": system_message}]
    # conversation = system_message
    return conversation

# The function encapsulates the chat completions API call to Open AI
def get_chat_model_completions(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        #temperature=0, # this is the degree of randomness of the model's output
        #max_tokens = 300
    )
    return response.choices[0].message.content


# The following fucntion checks the user input for content inputed for moderation check
def moderation_check(user_input):
    response = openai.moderations.create(input=user_input)
    moderation_output = response.results[0].flagged
    if moderation_output == True:
        return "Flagged"
    else:
        return "Not Flagged"

# The intent confirmation layer evaluates the output of the chat completion from Open AI API
def intent_confirmation_layer(response_assistant):
    delimiter = "####"
    prompt = f"""
    You are a senior evaluator who has an eye for detail.
    You are provided an string input. You need to see that in the string the values for following 
    1. GPU intensity
    2. Display Quality
    3. Portability
    4. Multi tasking
    5. Processing speed
    6. Budget
    have been captured successfully. Return Yes Or No

    The values for all keys, except 'budget', must be 'low', 'medium', or 'high' and the value of 'budget' must be a number. 

    Please not that every key should have a value and budget should be a valid number

    Remember return No if any one of the values is not captured

    """
    messages=[{"role": "system", "content":prompt },{"role": "user", "content":f"""Here is the input: {response_assistant}""" }]
    confirmation = openai.chat.completions.create(
                                    model="gpt-3.5-turbo",
                                    messages = messages)

    return confirmation.choices[0].message.content


# The intent confirmation layer evaluates the output of the chat completion from Open AI API
def get_user_requirement_string(response_assistant):
    delimiter = "####"
    prompt = f"""
    You are given a string where the user requirements for the given keys different keys ('GPU intensity','Display quality','Portability','Multitasking','Processing speed','Budget') has
    been captured inside that. The values for all keys, except 'budget', will be 'low', 'medium', or 'high' and the value of 'budget' will be a number.
    
    You have to give out the string in the format where only the user intent is present and the output should match the given format
    I need a laptop with high GPU intensity, medium display quality, high portablity, high multi tasking, high processing speed and a budget of 100000.
    The values currently in the string provided are only representative values.

    Here is a sample input and output 

    input : Great! Based on your requirements, I have a clear picture of your needs. You prioritize low GPU intensity, high display quality, low portability, high multitasking, high processing speed, and have a budget of 200000 INR. Thank you for providing all the necessary information.
    output : I need a laptop with low GPU intensity, high display quality, low portablity, high multitasking, high processing speed and a budget of 200000.
    """
    messages=[{"role": "system", "content":prompt },{"role": "user", "content":f"""Here is the input: {response_assistant}""" }]
    confirmation = openai.chat.completions.create(
                                    model="gpt-3.5-turbo",
                                    messages = messages)

    return confirmation.choices[0].message.content

# Create custom function for using Open AI function calling
shopassist_custom_functions = [
    {
        'name': 'extract_user_info',
        'description': 'Get the user laptop information from the body of the input text',
        'parameters': {
            'type': 'object',
            'properties': {
                'GPU intensity': {
                    'type': 'string',
                    'description': 'GPU intensity of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Display quality': {
                    'type': 'string',
                    'description': 'Display quality of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Portability': {
                    'type': 'string',
                    'description': 'The portability of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Multitasking': {
                    'type': 'string',
                    'description': 'The multitasking abiliy of the user requested laptop. The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Processing speed': {
                    'type': 'string',
                    'description': 'The processing speed of the user requested laptop.  The values  are ''low'', ''medium'', or ''high'' based on the importance of the corresponding keys, as stated by user'
                },
                'Budget': {
                    'type': 'integer',
                    'description': 'The budget of the user requested laptop. The values are integers.'
                }
            }
        }
    }
]

# Calls OpenAI API to return the function calling parameters
def get_chat_completions_func_calling(input, include_budget):
  final_message = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": input}
    ]

  completion = openai.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = final_message,
    functions = shopassist_custom_functions,
    function_call = 'auto'
  )
  function_parameters = json.loads(completion.choices[0].message.function_call.arguments)
  budget = 0
  if include_budget:
      budget = function_parameters['Budget']

  return extract_user_info(function_parameters['GPU intensity'], function_parameters['Display quality'], function_parameters['Portability'], function_parameters['Multitasking'],
                                       function_parameters['Processing speed'], budget)

# The local function that we have written to extract the laptop information for user
def extract_user_info(GPU_intensity, Display_quality, Portability, Multitasking, Processing_speed, Budget):
    """

    Parameters:
    GPU_intensity (str): GPU intensity required by the user.
    Display_quality (str): Display quality required by the user.
    Portability (str): Portability required by the user.
    Multitasking (str): Multitasking capability required by the user.
    Processing_speed (str): Processing speed required by the user.
    Budget (int): Budget of the user.

    Returns:
    dict: A dictionary containing the extracted information.
    """
    return {
        "GPU intensity": GPU_intensity,
        "Display quality": Display_quality,
        "Portability": Portability,
        "Multitasking": Multitasking,
        "Processing speed": Processing_speed,
        "Budget": Budget
    }

# Compare and find laptops that match user requirements
def compare_laptops_with_user(user_requirements):
    laptop_df= pd.read_csv('laptop_data.csv')
    laptop_df['laptop_feature'] = laptop_df['Description'].apply(lambda x: product_map_layer(x))
    budget = int(user_requirements.get('Budget', '0')) #.replace(',', '').split()[0])
    filtered_laptops = laptop_df.copy()
    filtered_laptops['Price'] = filtered_laptops['Price'].str.replace(',','').astype(int)
    filtered_laptops = filtered_laptops[filtered_laptops['Price'] <= budget].copy()
    mappings = {
        'low': 0,
        'medium': 1,
        'high': 2
    }
    # Create 'Score' column in the DataFrame and initialize to 0
    filtered_laptops['Score'] = 0
    for index, row in filtered_laptops.iterrows():
        user_product_match_str = row['laptop_feature']
        laptop_values = get_chat_completions_func_calling(user_product_match_str, False)
        score = 0

        for key, user_value in user_requirements.items():
            if key.lower() == 'budget':
                continue  # Skip budget comparison
            laptop_value = laptop_values.get(key, None)
            laptop_mapping = mappings.get(laptop_value.lower(), -1)
            user_mapping = mappings.get(user_value.lower(), -1)
            if laptop_mapping >= user_mapping:
                ### If the laptop value is greater than or equal to the user value the score is incremented by 1
                score += 1

        filtered_laptops.loc[index, 'Score'] = score

    # Sort the laptops by score in descending order and return the top 5 products

    top_laptops = filtered_laptops.drop('laptop_feature', axis=1)
    top_laptops = top_laptops.sort_values('Score', ascending=False).head(3)

    return top_laptops.to_json(orient='records')

def recommendation_validation(laptop_recommendation):
    data = json.loads(laptop_recommendation)
    data1 = []
    for i in range(len(data)):
        if data[i]['Score'] > 2:
            data1.append(data[i])

    return data1

def initialize_conv_reco(products):
    system_message = f"""
    You are an intelligent laptop gadget expert and you are tasked with the objective to \
    solve the user queries about any product from the catalogue: {products}.\
    You should keep the user profile in mind while answering the questions.\

    Start with a brief summary of each laptop in the following format, in decreasing order of price of laptops:
    1. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>
    2. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>

    """
    conversation = [{"role": "system", "content": system_message }]
    return conversation

def product_map_layer(laptop_description):
    delimiter = "#####"
    lap_spec = "Laptop with (Type of the Graphics Processor) GPU intensity, (Display Type, Screen Resolution, Display Size) display quality, (Laptop Weight) portablity, (RAM Size) multi tasking, (CPU Type, Core, Clock Speed) processing speed"

    values = {'low','medium','high'}

    prompt=f"""
    You are a Laptop Specifications Classifier whose job is to extract the key features of laptops and classify them as per their requirements.
    To analyze each laptop, perform the following steps:
    Step 1: Extract the laptop's primary features from the description {laptop_description}
    Step 2: Store the extracted features in {lap_spec} \
    Step 3: Classify each of the items in {lap_spec} into {values} based on the following rules: \
    {delimiter}
    GPU Intensity:
    - low: <<< if GPU is entry-level such as an integrated graphics processor or entry-level dedicated graphics like Intel UHD >>> , \n
    - medium: <<< if mid-range dedicated graphics like M1, AMD Radeon, Intel Iris >>> , \n
    - high: <<< high-end dedicated graphics like Nvidia RTX >>> , \n

    Display Quality:
    - low: <<< if resolution is below Full HD (e.g., 1366x768). >>> , \n
    - medium: <<< if Full HD resolution (1920x1080) or higher. >>> , \n
    - high: <<< if High-resolution display (e.g., 4K, Retina) with excellent color accuracy and features like HDR support. >>> \n

    Portability:
    - high: <<< if laptop weight is less than 1.51 kg >>> , \n
    - medium: <<< if laptop weight is between 1.51 kg and 2.51 kg >>> , \n
    - low: <<< if laptop weight is greater than 2.51 kg >>> \n

    Multitasking:
    - low: <<< If RAM size is 8 GB, 12 GB >>> , \n
    - medium: <<< if RAM size is 16 GB >>> , \n
    - high: <<< if RAM size is 32 GB, 64 GB >>> \n

    Processing Speed:
    - low: <<< if entry-level processors like Intel Core i3, AMD Ryzen 3 >>> , \n
    - medium: <<< if Mid-range processors like Intel Core i5, AMD Ryzen 5 >>> , \n
    - high: <<< if High-performance processors like Intel Core i7, AMD Ryzen 7 or higher >>> \n
    {delimiter}

    {delimiter}
    Here is input output pair for few-shot learning:
    input 1: "The Dell Inspiron is a versatile laptop that combines powerful performance and affordability. It features an Intel Core i5 processor clocked at 2.4 GHz, ensuring smooth multitasking and efficient computing. With 8GB of RAM and an SSD, it offers quick data access and ample storage capacity. The laptop sports a vibrant 15.6" LCD display with a resolution of 1920x1080, delivering crisp visuals and immersive viewing experience. Weighing just 2.5 kg, it is highly portable, making it ideal for on-the-go usage. Additionally, it boasts an Intel UHD GPU for decent graphical performance and a backlit keyboard for enhanced typing convenience. With a one-year warranty and a battery life of up to 6 hours, the Dell Inspiron is a reliable companion for work or entertainment. All these features are packed at an affordable price of 35,000, making it an excellent choice for budget-conscious users."
    output 1" "Laptop with medium GPU intensity, medium Dsiplay quality, medium Portability, high Multitaksing, medium Processing speed"
    
    {delimiter}
    ### Strictly don't keep any other text in the values for the keys other than low or medium or high. Also return only the string and nothing else###
    """
    input = f"""Follow the above instructions step-by-step and output the string {lap_spec} for the following laptop {laptop_description}."""
    #see that we are using the Completion endpoint and not the Chatcompletion endpoint
    messages=[{"role": "system", "content":prompt },{"role": "user","content":input}]

    response = get_chat_model_completions(messages)
    return response
