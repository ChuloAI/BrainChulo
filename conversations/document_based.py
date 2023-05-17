from langchain.document_loaders import TextLoader
from memory.chroma_memory import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationChain
from langchain.agents import Tool
from langchain.schema import OutputParserException
from llms.oobabooga_llm import OobaboogaLLM
from prompt_templates.document_based_conversation import Examples, ConversationWithDocumentTemplate
from settings import logger, load_config
from langchain.agents import (
    AgentExecutor,
    LLMSingleActionAgent,
    Tool,
)
from prompt_templates.custom_agent import (
    CustomAgentPromptTemplate,
    CustomAgentOutputParser,
    template
)
from langchain import LLMChain


config = load_config()

USE_AGENT = config.use_agent

def echo(in_):
    return in_


class DocumentBasedConversation():
    def __init__(self):
        """
        Initializes an instance of the class. It sets up LLM, text splitter, vector store, prompt template, retriever,
        conversation chain, tools, and conversation agent if USE_AGENT is True.
        """

        self.llm = OobaboogaLLM()
        # self.text_splitter = CharacterTextSplitter(
        #     chunk_size=1000, chunk_overlap=0)
        # self.vector_store_docs = Chroma(collection_name="docs_collection")
        # self.vector_store_convs = Chroma(collection_name="convos_collection")

        # convs_retriever = self.vector_store_convs.get_store().as_retriever(
        #     search_kwargs=dict(top_k_docs_for_context=10))

        # convs_memory = VectorStoreRetrieverMemory(retriever=convs_retriever)

        # self.prompt = ConversationWithDocumentTemplate(
        #     input_variables=[
        #         "input",
        #         "history"
        #     ],
        #     document_store=self.vector_store_docs,
        # )

        # self.conversation_chain = ConversationChain(
        #     llm=self.llm,
        #     prompt=self.prompt,
        #     memory=convs_memory,
        #     verbose=True
        # )

        if USE_AGENT:
            tools = [
                Tool(
                    name="SearchLongTermMemory",
                    func=self.search,
                    description="""useful when you need to search very specific information in long-term memory.
Note that your long-term memory is limited, so more often than the information is NOT available in your memory.
Examples of use:

Example 1:
Question: What is the author's name?
Thought: I need to check my long-term memory
Action: SearchLongTermMemory
Action Input: "Author Name"
Observation: "Jack Black"
Thought: I now know the answer.
Final Answer: The author's name is Jack Black.

Example 2:
Question: Who is the author?
Thought: I need to check my long-term memory
Action: SearchLongTermMemory
Action Input: "Author Name"
Observation: Document[]
Thought:  
Example 3:
Question: Hi
Thought: This is not a question.
Final Answer: Hello, friend! How can I help you?

""",
                )
            , Tool(
                name="Say",
                func=echo,
                description="""Use to talk back to the human.
Example:
Action: Say
Action Input:
Hello, world!

Observation: Hello, world!
Final Answer: Hello, world!
""",
            )]
            prompt = CustomAgentPromptTemplate(
                template=template,
                tools=tools,
                input_variables=["input", "intermediate_steps"],
            )

            output_parser = CustomAgentOutputParser()
            llm_chain = LLMChain(llm=self.llm, prompt=prompt)

            tool_names = [tool.name for tool in tools]
            agent = LLMSingleActionAgent(
                llm_chain=llm_chain,
                output_parser=output_parser,
                stop=["\nObservation:"],
                allowed_tools=tool_names,
            )

            agent_executor = AgentExecutor.from_agent_and_tools(
                agent=agent, tools=tools, verbose=True
            )

            self.conversation_agent = agent_executor



    def load_document(self, document_path):
        """
        Load a document from a file and add its contents to the vector store.

        Args:
          document_path: A string representing the path to the document file.

        Returns:
          None.
        """
        text_loader = TextLoader(document_path, encoding="utf8")
        documents = text_loader.load()
        documents = self.text_splitter.split_documents(documents)

        self.vector_store_docs.add_documents(documents)

    def search(self, search_input):
        """
        Search for the given input in the vector store and return the top 10 most similar documents with their scores.
        This function is used as a helper function for the SearchLongTermMemory tool

        Args:
          search_input (str): The input to search for in the vector store.

        Returns:
          List[Tuple[str, float]]: A list of tuples containing the document text and their similarity score.
        """
        logger.info(f"Searching for: {search_input} in LTM")
        docs = self.vector_store_docs.similarity_search_with_score(
            search_input, top_k_docs_for_context=10)
        return docs

    def predict(self, input):
        """
        Predicts a response based on the given input.

        Args:
          input (str): The input string to generate a response for.

        Returns:
          str: The generated response string.

        Raises:
          OutputParserException: If the response from the conversation agent could not be parsed.
        """
        if USE_AGENT:
            try:

                response = self.conversation_agent.run(
                    input=input
                )
            except OutputParserException as e:
                response = str(e)
                if not response.startswith("Could not parse LLM output: `"):
                    raise e
                response = response.removeprefix(
                    "Could not parse LLM output: `").removesuffix("`")
        else:
            raise ValueError("Agent is the only option :)")
            # response = self.conversation_chain.predict(input=input)

        return response
