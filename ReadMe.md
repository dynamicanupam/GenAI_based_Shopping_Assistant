# ShopAssist AI

## Project Background
In today's digital age, online shopping has become the go-to option for many consumers. However, the overwhelming number of choices and the lack of personalized assistance can make the shopping experience daunting. To address this, we have developed ShopAssist AI, a chatbot that combines the power of large language models and rule-based functions to ensure accurate and reliable information delivery.

## Problem Statement
Given a dataset containing information about laptops (product names, specifications, descriptions, etc.), build a chatbot that parses the dataset and provides accurate laptop recommendations based on user requirements.

## Dataset
We have a dataset `laptop_data.csv` where each row describes the features of a single laptop and also has a small description at the end. The chatbot will leverage large language models to parse this `Description` column and provide recommendations.

## Approach
1. **Conversation and Information Gathering:** The chatbot will utilize language models to understand and generate natural responses. Through a conversational flow, it will ask relevant questions to gather information about the user's requirements.
2. **Information Extraction:** Once the essential information is collected, rule-based functions come into play, extracting the top 3 laptops that best match the user's needs.
3. **Personalized Recommendation:** Leveraging this extracted information, the chatbot engages in further dialogue with the user, efficiently addressing their queries and aiding them in finding the perfect laptop solution.

## System Design

### Stage 1
1. **Intent Clarity Layer**
2. **Intent Confirmation Layer**

### Stage 2
1. **Product Mapping Layer**
2. **Product Information Extraction Layer**

### Stage 3
1. **Product Recommendation Layer**

## Major Functions
- `initialize_conversation()`: Initializes the variable conversation with the system message.
- `get_chat_completions()`: Takes the ongoing conversation as the input and returns the response by the assistant.
- `moderation_check()`: Checks if the user's or the assistant's message is inappropriate. If any of these is inappropriate, it ends the conversation.
- `intent_confirmation_layer()`: Evaluates if the chatbot has captured the user's profile clearly.
- `dictionary_present()`: Checks if the final understanding of the user's profile is returned by the chatbot as a Python dictionary.
- `compare_laptops_with_user()`: Compares the user's profile with the different laptops and comes back with the top 3 recommendations.
- `initialize_conv_reco()`: Initializes the recommendations conversation.


### Prerequisites
- Python 3.7+
- OpenAI API Key(you have to add openai api key in the empty txt file (OpenAI_API_Key))
