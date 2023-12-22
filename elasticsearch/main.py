from rag_elasticsearch import chain

if __name__ == "__main__":
    """
    question = "What is included in my Northwind Health Plus plan that is not in standard?"
    response = chain.invoke(
        {
            "question": question,
            "chat_history": [],
        }
    )
    print(response)

    follow_up_question = "Does my plan cover eye exams?"

    response = chain.invoke(
        {
            "question": follow_up_question,
            "chat_history": [
                question,
                response
            ],
        }
    )
    print(response)
    """
    history=[]
    print("You can ask a question.")
    while True:
        user_prompt = input()
        if(user_prompt == "exit"):
            break
        response = chain.invoke(
            {
                "question": user_prompt,
                "chat_history": history
            }
        )
        print(response)
        history.append(user_prompt)
        history.append(response)
        
