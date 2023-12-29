# Comments Reasoner

A basic demo that retrieves comments for a given product from a marketplace (Trendyol), and sends them to LLM to get
a short summary of the common problems about the product.
It asks the same question both to the Azure AI and Ollama Llama2 model.
The query result may not match exactly the product, because we are using the markeplace's search function and get the 
first product.
