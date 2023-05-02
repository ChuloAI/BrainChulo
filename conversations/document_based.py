from langchain.document_loaders import TextLoader
from memory.chroma_memory import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, initialize_agent, AgentType, load_tools
from langchain.schema import OutputParserException
from llms.oobabooga_llm import OobaboogaLLM
from prompt_templates.document_based_conversation import Template, Examples
from settings import logger, load_config

config = load_config()

USE_AGENT = config.use_agent


class DocumentBasedConversation():
    def __init__(self):
        """
        Initializes an instance of the class. It sets up LLM, text splitter, vector store, prompt template, retriever,
        conversation chain, tools, and conversation agent if USE_AGENT is True.
        """

        self.llm = OobaboogaLLM()
        self.text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0)
        self.vector_store = Chroma()
        self.prompt = PromptTemplate(
            input_variables=[
                "history",
                "input"],
            template=Template)
        retriever = self.vector_store.get_store().as_retriever(
            search_kwargs=dict(top_k_docs_for_context=10))
        memory = VectorStoreRetrieverMemory(retriever=retriever)

        self.conversation_chain = ConversationChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=memory,
            verbose=True
        )

        if USE_AGENT:
            tools = load_tools([])

            tools.append(
                Tool(
                    name="FriendlyDiscussion",
                    func=self.conversation_chain.run,
                    description="useful when you need to discuss with a human based on relevant context from previous conversation",
                ))

            tools.append(
                Tool(
                    name="SearchLongTermMemory",
                    func=self.search,
                    description="useful when you need to search for information in long-term memory",
                ))

            self.conversation_agent = initialize_agent(
                tools,
                self.llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                memory=memory,
                verbose=True)

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

        self.vector_store.add_documents(documents)

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
        docs = self.vector_store.similarity_search_with_score(
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
                    input=f"{Examples}\n{input}")
            except OutputParserException as e:
                response = str(e)
                if not response.startswith("Could not parse LLM output: `"):
                    raise e
                response = response.removeprefix(
                    "Could not parse LLM output: `").removesuffix("`")
        else:
            response = self.conversation_chain.predict(input=input)

        return response
