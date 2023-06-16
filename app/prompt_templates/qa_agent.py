QA_ETHICAL_AGENT="""
{{#system~}}
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
You are a helpful assistant. Answer the following questions as best you can. You have access to the following tools:
Search: Useful for when you need to answer questions about current events. The input is the question to search relevant information.
{{~/system}}

{{#block hidden=True}}
{{~! The assistant either starts the conversation or not, depending on if the user query is offensive or no}}
{{#user~}}
Utilizing your extensive understanding of common moral and ethical principles, please evaluate the following user's query {{question}}. Analyze the potential implications and outcomes associated with the query, considering various ethical frameworks such as consequentialism, deontology, and virtue ethics, among others. Also consider the social, cultural, and legal context of the query. Is the user's query ethical and/or moral? 
{{~/user}}

{{#assistant~}}
Observation: Let's see if the query is offensive.
Decision:{{#select 'offensive' logprobs='logprobs'}}Yes{{or}}No{{/select}}
{{~/assistant}}
{{/block}}

{{#if (equal offensive 'Yes')~}}
Final Answer: I'm sorry, but I can't answer that.
{{else}}

{{~! The assistant then classifies the user intent to decide whether he needs to enter qa mode}}
{{#user~}}
Question: {{question}}
Now classify the intent behind this question:{{question}} Identify if this question is phatic (serving a social function) or referential (seeking information). Provide reasoning for your classification based on elements like the content, structure, or context of the user's input.
{{~/user}}

{{#assistant~}}
Thought: I need to evaluate the user's query and determine its intent - is {{question}} phatic or referential?
Decision:{{#select 'query_type' logprobs='logprobs'}}Phatic{{or}}Referential{{/select}}
{{~/assistant}}

{{#if (equal query_type "Phatic")~}}
Observation: The user's query is conversational. I need to answer as an helpful assistant while taking into account our chat history;
Chat history: {{history}}
Latest user message: {{question}}
Thought: I need to stay in my role of an helpful assistant and make casual conversation.
Final Answer: {{gen 'phatic answer' temperature=0.7 max_tokens=50}}
{{else}}

{{#user~}}
Here are the relevant documents from our database:{{set 'documents' (search question)}}
Using the concept of deixis, please evaluate if the answer to {{question}} is in :{{documents}}. Note that your response MUST contain either 'yes' or 'no'.
{{~/user}}

{{#assistant~}}
Thought: I need to determine if the answer to {{question}} is in: {{documents}}.
Decision:{{#select 'answerable' logprobs='logprobs'}}Yes{{or}}No{{/select}}

{{#if (equal answerable "Yes")~}}
Observation: I believe I can answer {{question}} based on the information contained in my analysis.
Thought: Now that I know that I can answer, I should provide the information to the user.
Final Answer: {{gen 'answer' temperature=0 max_tokens=100}}
{{else}}
Thought: I don't think I can answer the question based on the information contained in the returned documents.
Final Answer: I'm sorry, but I don't have sufficient information to provide an answer to this question.

{{/if}}
{{~/assistant}}

{{/if}}

{{/if}}



"""


QA_AGENT= """
{{#system~}}
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
Answer the following questions as best you can. You have access to the following tools:
Search: Useful for when you need to answer questions about current events. The input is the question to search relevant information.
{{~/system}}

{{#user~}}
Question: {{question}}
{{~/user}}

{{#assistant~}}
Thought: Let's first check our database.
Action: Check Question
Action Input: {{question}}
{{~/assistant}}

{{~! The assistant then classifies the user intent to decide whether he needs to enter qa mode}}
{{#user~}}
Question: {{question}}
Now classify the intent behind this question:{{question}} Identify if this question is phatic (serving a social function) or referential (seeking information). Provide reasoning for your classification based on elements like the content, structure, or context of the user's input.
{{~/user}}

{{#assistant~}}
Thought: I need to evaluate the user's query and determine its intent - is {{question}} phatic or referential?
Decision:{{#select 'query_type' logprobs='logprobs'}}Phatic{{or}}Referential{{/select}}
{{~/assistant}}

{{#if (equal query_type "Phatic")~}}
Observation: The user's query is conversational. I need to answer as an helpful assistant while taking into account our chat history;
Chat history: {{history}}
Latest user message: {{question}}
Thought: I need to stay in my role of an helpful assistant and make casual conversation.
Final Answer: {{gen 'phatic answer' temperature=0.7 max_tokens=50}}
{{else}}

{{#user~}}
Here are the relevant documents from our database:{{set 'documents' (search question)}}
Using the concept of deixis, please evaluate if the answer to {{question}} is in :{{documents}}. Note that your response MUST contain either 'yes' or 'no'.
{{~/user}}

{{#assistant~}}
Thought: I need to determine if the answer to {{question}} is in: {{documents}}.
Decision:{{#select 'answerable' logprobs='logprobs'}}Yes{{or}}No{{/select}}

{{#if (equal answerable "Yes")~}}
Observation: I believe I can answer {{question}} based on the information contained in my analysis.
Thought: Now that I know that I can answer, I should provide the information to the user.
Final Answer: {{gen 'answer' temperature=0 max_tokens=100}}
{{else}}
Thought: I don't think I can answer the question based on the information contained in the returned documents.
Final Answer: I'm sorry, but I don't have sufficient information to provide an answer to this question.

{{/if}}
{{~/assistant}}

{{/if}}

"""
ETHICS_PROMPT= '''
{{#system~}}
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
Answer the following questions as best you can. You have access to the following tools:
Search: Useful for when you need to answer questions about current events. The input is the question to search relevant information.
{{~/system}}

{{~! The assistant either starts the conversation or not, depending on if the user query is offensive or no}}
{{#user~}}
Utilizing your extensive understanding of common moral and ethical principles, please evaluate the following user's query {{question}}. Analyze the potential implications and outcomes associated with the query, considering various ethical frameworks such as consequentialism, deontology, and virtue ethics, among others. Also consider the social, cultural, and legal context of the query. Is the user's query ethical and/or moral? 
{{~/user}}

{{#assistant~}}
Observation: Let's see if the query is offensive.
Decision:{{#select 'ethic' logprobs='logprobs'}}Yes{{or}}No{{/select}}
{{~/assistant}}

'''