from mistralai import Mistral

# Initialize the Mistral client with your API key
api_key = "Mgkw2azh24EGH2iBA2AqDK5okbClIUVV"
client = Mistral(api_key=api_key)

def chat(user_message: str) -> str:
    """Send a message to Mistral AI and get a response."""
    message = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return message.choices[0].message.content

def main():
    """Main bot loop for interactive chat."""
    print("Mistral AI Bot - Type 'exit' to quit")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            response = chat(user_input)
            print(f"\nBot: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
