import json
from difflib import get_close_matches
from textblob import TextBlob

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Knowledge base file '{file_path}' not found. Creating a new one.")
        return {"questions": []}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{file_path}'. Initializing with empty knowledge base.")
        return {"questions": []}

def save_knowledge_base(file_path: str, data: dict):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"Knowledge base saved to '{file_path}'.")
    except Exception as e:
        print(f"Error saving knowledge base to '{file_path}': {e}")

def find_best_match(user_input: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_input.lower(), [q.lower() for q in questions], n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

def analyze_sentiment(text: str) -> str:
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0.5:
        return "very positive"
    elif sentiment_score > 0:
        return "positive"
    elif sentiment_score < -0.5:
        return "very negative"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"

def chat_bot():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    print("Bot: Hi! I'm here to help you with banking-related questions. Type 'quit' to exit.")

    while True:
        user_input = input('You: ')

        normalized_input = user_input.lower().strip()

        if normalized_input == 'quit':
            break

        if normalized_input in ['hello', 'hi', 'hey']:
            print("Bot: Hello! How can I assist you today?")
            continue
        elif normalized_input in ['thanks', 'thank you']:
            print("Bot: You're welcome!")
            continue
        elif normalized_input in ['okay', 'ok']:
            print("Bot: Alright!")
            continue

        best_match = find_best_match(normalized_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(f'Bot: {answer}')
            else:
                print("Bot: I don't have an answer for that.")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": normalized_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

        # Perform sentiment analysis on user input
        sentiment = analyze_sentiment(user_input)

        if sentiment == "very positive":
            print("Bot: That's wonderful to hear! Is there anything else I can assist you with?")
        elif sentiment == "positive":
            print("Bot: I'm glad you're feeling positive! How can I help?")
        elif sentiment == "very negative":
            print("Bot: I'm sorry to hear that you're feeling very negative. Please feel free to share more.")
        elif sentiment == "negative":
            print("Bot: I understand it's frustrating. Let's work together to find a solution.")
        else:
            print("Bot: Let's continue. How can I assist you?")

    print("Bot: Goodbye!")

    # Prompt for user feedback
    feedback = input("Bot: Did you find the information helpful? Please provide feedback (yes/no): ")
    if feedback.lower() == 'yes':
        print("Bot: Thank you for your feedback!")
    else:
        print("Bot: We'll work on improving our responses based on your feedback. Thank you!")

if __name__ == '__main__':
    chat_bot()