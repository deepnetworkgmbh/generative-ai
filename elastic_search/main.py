from rag_elasticsearch import chain
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

if __name__ == "__main__":
    """
    question = "What is included in my Northwind Health Plus plan that is not in standard?"
    follow_up_question = "Does my plan cover eye exams?"
    """
    system_message = """
        You are an assistant that helps the company employees with their healthcare plan questions, and questions about the employee handbook. Be brief in your answers.
    """

    history=[SystemMessage(content=system_message)]
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
        history.append(HumanMessage(content=user_prompt))
        history.append(AIMessage(content=response))
        
