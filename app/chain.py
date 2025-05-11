from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class Chain:
    def __init__(self):
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        # defining the LLM model
        self.llm = ChatGroq(
            model = "gemma2-9b-it",
            temperature = 0.5,
            api_key = groq_api_key
        )
        
    def get_answer(self, question: str, docs_data):
        # Creating the prompt
        prompt = PromptTemplate(
            input_variables = ['question', 'pages_data'],
            template = 
            '''
            ## Question:
            {question}
            
            ## Page Data:
            {pages_data}
            
            ## Instruction on what to do:
            In the 'Page data' session I had provided the list of dictonaries.
            Each dictonary have following keys:
                doc_title: title of the document
                page_no.: page number in the document mentioned in doc_title
                page_content: content in the page
            Your job is to analyze the page_content and provide the answer to the question mentioned in the 'Question' session.
            Your answer should be based on the information provided in 'Page Data' session only.
            Also, at the end of the answer in next line mentioned want document and page number you had refered, like '\n References: '<document_name>' page <page_number>.'. If you are not able to get the answer then no need to mentioned this.
            If you are not able to get the answer then answer should be 'No information in the provided documents.' only, no need to add references.
            Do not provide preamble.
            
            ## Answer (No Preamble):
            '''
        )
        # creating a chain - which pass the prompt to the defined LLM model
        answer_chain = LLMChain(
            llm = self.llm,
            prompt = prompt
        )
        # running the chain
        answer = answer_chain.run({'question': question, 'pages_data': docs_data})
        return answer