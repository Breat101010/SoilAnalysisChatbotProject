import os
import google.generativeai as genai
import re #text processing
import textwrap #formatting long text

#API Confiuration
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set it before running ")
    exit()

genai.configure(api_key=api_key)

#Gemini Model
GeminiModel = 'models/gemini-2.5-flash-lite'

#Knowledge file
KnowledgeDir = 'knowledge_base'

#Load Knowledge Base
def load_knowledge_base(directory):
    """Load all text files from the knowledge base directory."""
    knowledge={}
    print(f"Loading the knowledge base from: {directory}")
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    knowledge[filename] = f.read()
                print(f"-Loaded: {filename}")
            except Exception as e:
                print(f"Error Loading {filename}: {e}")
    if not knowledge:
        print("No .txt file found in knowledge base")
        print("Please ensure files are there!!")
    return knowledge

#RAG (Retrieval Augmented Generation) fxn

def get_relevant_knowledge(query, knowledge_base):
    """keyword based retrieval from our knowledge base."""

    relevant_chunks = []
    #make query lower case for case insensitive matching
    query_lower = query.lower() 

    #Key words to look for
    keywords_to_files = {
        'ph': ['zimbabwe_soil_types.txt', 'zimbabwe_agricultural_practices.txt', 'zimbabwe_soil_fertility_issues.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'nitrogen': ['zimbabwe_soil_fertility_issues.txt', 'zimbabwe_crop_nutrient_requirements.txt', 'zimbabwe_agricultural_practices.txt'],
        'phosphorus': ['zimbabwe_soil_fertility_issues.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'potassium': ['zimbabwe_soil_fertility_issues.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'npk': ['zimbabwe_crop_nutrient_requirements.txt'],
        'maize': ['zimbabwe_common_crops.txt', 'zimbabwe_crop_nutrient_requirements.txt', 'zimbabwe_agricultural_practices.txt'],
        'soil type': ['zimbabwe_soil_types.txt'],
        'fertility': ['zimbabwe_soil_fertility_issues.txt', 'zimbabwe_agricultural_practices.txt'],
        'amendments': ['zimbabwe_agricultural_practices.txt', 'zimbabwe_soil_fertility_issues.txt'],
        'organic matter': ['zimbabwe_soil_fertility_issues.txt', 'zimbabwe_agricultural_practices.txt'],
        'zimbabwe': ['zimbabwe_soil_types.txt', 'zimbabwe_common_crops.txt', 'zimbabwe_agricultural_practices.txt', 'zimbabwe_soil_fertility_issues.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'crop': ['zimbabwe_common_crops.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'cultivation': ['zimbabwe_agricultural_practices.txt'],
        'drought': ['zimbabwe_agricultural_practices.txt', 'zimbabwe_common_crops.txt'],
        'sandy soil': ['zimbabwe_soil_types.txt', 'zimbabwe_soil_fertility_issues.txt', 'zimbabwe_agricultural_practices.txt'],
        'clay soil': ['zimbabwe_soil_types.txt'],
        'liming': ['zimbabwe_agricultural_practices.txt', 'zimbabwe_soil_fertility_issues.txt'],
        'cotton': ['zimbabwe_common_crops.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'tobacco': ['zimbabwe_common_crops.txt'],
        'sorghum': ['zimbabwe_common_crops.txt'],
        'millet': ['zimbabwe_common_crops.txt'],
        'groundnuts': ['zimbabwe_common_crops.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'beans': ['zimbabwe_common_crops.txt'],
        'wheat': ['zimbabwe_common_crops.txt', 'zimbabwe_crop_nutrient_requirements.txt'],
        'manure': ['zimbabwe_agricultural_practices.txt', 'zimbabwe_soil_fertility_issues.txt'],
        'compost': ['zimbabwe_agricultural_practices.txt', 'zimbabwe_soil_fertility_issues.txt']
    }
    #files to check given keywords
    files_to_check = set()
    for keyword, files in keywords_to_files.items():
        if keyword in query_lower:
            files_to_check.update(files)

    #if no keywords give general zimbabwean files
    if not files_to_check:
        files_to_check.add('zimbabwe_soil_types.txt')
        files_to_check.add('zimbabwe_common_crops.txt')
        files_to_check.add('zimbabwe_agricultural_practices.txt')
        relevant_info = knowledge_base.get('zimbabwe_agricultural_practices.txt', '')

    relevant_chunks = []
    for filename in files_to_check:
        if filename in knowledge_base:
            relevant_chunks.append(f"--- information from {filename} ---\n{knowledge_base[filename]}\n--- End of {filename} ---")

    return "\n\n".join(relevant_chunks) if relevant_chunks else ""

def generate_response(user_query, knowledge_base_content, history):
    """Generates response using Gemini whilst coupled with knowledge base...RAG"""
    model = genai.GenerativeModel(GeminiModel)
    chat = model.start_chat(history=history)


    #Prompt with instructions and context...
    prompt = textwrap.dedent(f"""
    You are called Leecia so introduce yourself and you are an AI soil analysis and farming expert for Zimbabwe.
    Your goal is to provide accurate, concise, and actionable advice to farmers based on your agricultural knowledge, their soil parameters and agricultural queries.
    Prioritize scientific accuracy and local relevance (Zimbabwean context).
    If you are asked about soil parameters (like pH, NPK levels), always ask the user for specific values if they haven't provided them.
    If you cannot provide a precise answer based on the provided information, state your limitation and suggest consulting a local agricultural extension officer or conducting a professional soil test.

    Here is relevant knowledge about Zimbabwean agriculture and soil:
    {knowledge_base_content}

    User's query: {user_query}

    Provide your response in a clear, easy-to-understand format for a farmer.
    """)
    #send prompt to gemini
    try:
        response= chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Im sorry i had an error trying to generate a response:{e}. Please try again"
    
#Main Bot Loop
def run_chatbot():
    print("Welcome to Leecia Soil Analysis Chatbot!")
    print("I can help you with questions about soil, crops and farming practices in Zimbabwe.")
    print("Type 'exit' to quit")

    #load the knowledge at the start
    knowledge_base = load_knowledge_base(KnowledgeDir)
    if not knowledge_base:
        print("Leecia cant work without knowledge. Exiting!!!")
        return
    #Chat history for you know...

    chat_history = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == 'exit':
            print("Thank for using Leecia chatbot. Goodbye!!")
            break

        if not user_input:
            print("Please ask question or enter soil parameters...")
            continue

        #Retrieve relevant knowledge
        relevant_info = get_relevant_knowledge(user_input, knowledge_base)

        if relevant_info:
            print("Relevant knowledge base content was retrieved.")

        else:
            print("No relevant knowledge found in the knowledge base for your query.")
            #general stuff
            relevant_info = knowledge_base.get('zimbabwe_agricultural_practices.txt', '')

         #generate response 
        response = generate_response(user_input, relevant_info, chat_history)


         #print response
        print(f"\nChatbot: {response}")

#Run Bot
if __name__ == "__main__":
    run_chatbot()



