QA_ETHICAL_AGENT="""
{{#system~}}
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
You are an helpgul assistant. Answer the following questions as best you can. You have access to the following tools:
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

{{#if (equal query_type "Phatic")~}}
Observation: The user's query is conversational. I need to answer him as an helpful assistant while taking into account our chat history;
Chat history: {{history}}
Latest user message: {{question}}
Final Answer: {{gen 'phatic answer' temperature=0.7 max_tokens=50}}
{{else}}


{{#user~}}
Here are the relevant documents from our database:{{search question}}
Given the documents listed, can you determine an answer to the following question based solely on the provided information: {{question}} Note that your response MUST contain either 'yes' or 'no'.
{{~/user}}

{{#assistant~}}
Observation: I need to determine if I can answer the question based solely on the returned documents.
Thought: Inferential analysis of {{question}} for potential answers, telegraphic style.
Summary {{gen 'summary' temperature=0.5 max_tokens=120}}
{{~/assistant}}

{{#user~}}
Given your analysis, can you determine an answer to the following question based solely on the provided information: {{question}} Consider all details, even if they seem only remotely related or are uncertain.
{{~/user}}

{{#assistant~}}
Thought: I need to determine if I can answer {{question}} based solely on the information provided in my analysis. 
Decision:{{#select 'answer' logprobs='logprobs'}}Yes{{or}}No{{/select}}
{{#if (equal answer "Yes")~}}
Observation: I believe I can answer {{question}} based on the information contained in my analysis. 
Final Answer: {{gen 'answer' temperature=0 max_tokens=100}}
{{else}}
Thought: I don't think I can answer the question based on the information contained in the returned documents.
Final Answer: I'm sorry, but I don't have sufficient information to provide an answer to this question.

{{/if}}
{{~/assistant}}

{{/if}}
{{~/assistant}}

{{/if}}"""


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

{{#user~}}
Here are the relevant documents from our database:{{search question}}
Given the documents listed, can you determine an answer to the following question based solely on the provided information: {{question}} Note that your response MUST contain either 'yes' or 'no'.
{{~/user}}

{{#assistant~}}
Observation: I need to determine if I can answer the question based solely on the returned documents.
Thought: Inferential analysis of {{question}} for potential answers, telegraphic style.
Summary {{gen 'summary' temperature=0.5 max_tokens=120}}
{{~/assistant}}

{{#user~}}
Given your analysis, can you determine an answer to the following question based solely on the provided information: {{question}} Consider all details, even if they seem only remotely related or are uncertain.
{{~/user}}

{{#assistant~}}
Thought: I need to determine if I can answer {{question}} based solely on the information provided in my analysis. 
Decision:{{#select 'answer' logprobs='logprobs'}}Yes{{or}}No{{/select}}
{{#if (equal answer "Yes")~}}
Observation: I believe I can answer {{question}} based on the information contained in my analysis. 
Final Answer: {{gen 'answer' temperature=0 max_tokens=100}}
{{else}}
Thought: I don't think I can answer the question based on the information contained in the returned documents.
Final Answer: I'm sorry, but I don't have sufficient information to provide an answer to this question.


{{#assistant~}}
Observation: I need to determine if I can answer the question based solely on the returned documents.
Thought: Let's first gen a bullet points summary of the returned documents trying to grasp the most relevant elements to the question.
Summary {{gen 'summary' temperature=0 max_tokens=100}}
Decision:{{#select 'answer' logprobs='logprobs'}}Yes{{or}}No{{/select}}

{{#if (equal answer "Yes")~}}
Thought: I believe I can answer {{question}} based on the information contained in the summary. 
Final Answer: {{gen 'final answer' temperature=0.7 max_tokens=50}}
{{else}}
Thought: I don't think I can answer the question based on the information contained in the returned documents.
Final Answer: I'm sorry, but I don't have sufficient information to provide an answer to this question.
{{/if}}

{{~/assistant}}

"""
ETHICS_PROMPT="""
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
"""