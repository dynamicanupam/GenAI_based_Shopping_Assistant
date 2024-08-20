# ShopAssist AI

## 1. Project Background
In today's digital age, online shopping has become the go-to option for many consumers. However, the overwhelming number of choices and the lack of personalized assistance can make the shopping experience daunting. To address this, we have developed ShopAssist AI, a chatbot that combines the power of large language models and rule-based functions to ensure accurate and reliable information delivery.

## 2. Problem Statement
Given a dataset containing information about laptops (product names, specifications, descriptions, etc.), build a chatbot that parses the dataset and provides accurate laptop recommendations based on user requirements.

## 3. Approach
1. **Conversation and Information Gathering:** The chatbot will utilize language models to understand and generate natural responses. Through a conversational flow, it will ask relevant questions to gather information about the user's requirements.
2. **Information Extraction:** Once the essential information is collected, rule-based functions come into play, extracting the top 3 laptops that best match the user's needs.
3. **Personalized Recommendation:** Leveraging this extracted information, the chatbot engages in further dialogue with the user, efficiently addressing their queries and aiding them in finding the perfect laptop solution.

## 4. System Functionalities

- **User Interface:** ShopAssistAI provides a user-friendly web interface where users can interact with the conversational AI assistant.
- **Conversational AI:** The core of ShopAssistAI is the conversational AI powered by OpenAI's chat model. It guides the user through the process by asking relevant questions and understanding their needs.
- **User Input Moderation:** User input is moderated using OpenAI's moderation API to ensure a safe and secure conversation.
- **User Profile Extraction:** The AI assistant extracts key information from the conversation to build a user profile that reflects their laptop preferences (budget, screen size, processing power, etc.) using OpenAI's function calling mechanism to convert a user requirement string into a JSON object.

### 4.1 Extracting User Requirements

ShopAssistAI utilizes OpenAI's chat-completion endpoint to generate responses and potentially extract user requirements within the conversation flow. This is achieved by sending prompts and conversation history to the API, and the response might contain user-expressed preferences. While OpenAI's API doesn't natively convert text to JSON, OpenAI’s function calling mechanism is used to convert user string extracts to relevant user requirements as key-value pairs.

### 4.2 Building the User Profile

The extracted key-value pairs are used to construct a user profile dictionary in JSON format, representing the user's preferences for various laptop attributes. We have a dataset `laptop_data.csv` where each row describes the features of a single laptop and also has a small description at the end. The chatbot will leverage large language models to parse this `Description` column and provide recommendations.

## 5. System Architecture

ShopAssistAI follows a client-server architecture. Users interact with the web interface hosted on a server running the Flask application. The application interacts with OpenAI's API for conversation generation and moderation and retrieves and compares laptop data from an external database.

![stages](https://github.com/user-attachments/assets/e6e690f5-8bb2-4cf6-9b13-08b7eaee14f9)

![systemdesign](https://github.com/user-attachments/assets/001e9fff-763e-4a54-9cc0-6633021f7ea0)

## 6. Implementation Details

The Flask application utilizes various functionalities:

- **Routing:** Maps user requests to appropriate functions based on URLs.
- **Conversation Management:** Handles conversation initiation, response generation through OpenAI's chat model, and conversation history maintenance.
- **User Input Processing:** Captures user input, performs moderation checks, and extracts user profiles from conversation history (converting user input string to JSON using OpenAI Function calling).
- **Recommendation Logic:** Compares user profiles with laptop data, validates recommendations, and generates recommendation text.

### Prerequisites
- Python 3.7+
- OpenAI API Key(you have to add openai api key in the empty txt file (OpenAI_API_Key))

### Getting Started

To get started with ShopAssist AI, follow these steps:

1. **Clone the repository:**
   ```
   git clone https://github.com/rajuaiml777/ShopAssistAI.git
   cd ShopAssistAI
   ```
2. **Lunch VS Code from Anaconda**
   - In VS Code go to `File` > `Open Folder...` and select the `ShopassistAI` folder.
   - Open a terminal in VS Code (``Ctrl+` `` or go to `Terminal` > `New Terminal`).
2. **Install dependencies:**
```   
pip install -r requirements.txt
```
3. **Initialize the conversation:**  
```
python app.py
```
#### Note: This version includes steps to create and activate the Conda environment with Python 3.11.9 0r above, ensuring users set up python environment correctly before installing dependencies and running the application.

## 7. Appendix - A

### Key Points:

- User interacts through a web browser.
- Flask web app receives the request and routes it to the appropriate function based on the URL.
- Two main functionalities: Invite flow (initial conversation) and Recommendation flow.
- Both functionalities involve:
  - Moderating user input.
  - Using OpenAI's chat model to generate responses.
  - Extracting user profile or validating recommendations.
- The application communicates with an external source (likely a database) to compare user profiles with laptop data.
- Recommendations are validated before presenting them to the user.
- The conversation history is updated after each interaction.

## 8. Appendix - B

User output example screenshot:

1. Screenshot 1:

![ScreenshotA](Images/Screenshot1.png)

2. Screenshot 2:

![ScreenshotB](Images/Screenshot2.png)

3. Screenshot 3:

![ScreenshotC](Images/Screenshot3.png)

4. Screenshot 4:

![ScreenshotD](Images/Screenshot4.png)
