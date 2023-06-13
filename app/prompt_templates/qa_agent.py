QA_ETHICAL_AGENT="""
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
Utilizing your extensive understanding of common moral and ethical principles, please evaluate the following user's query {{question}}. Analyze the potential implications and outcomes associated with the query, considering various ethical frameworks such as consequentialism, deontology, and virtue ethics, among others. Also consider the social, cultural, and legal context of the query. Is the user's query ethical and/or moral? 
{{~/user}}

{{#assistant~}}
Observation: Let's see if the query is offensive.
Decision:{{#select 'ethic' logprobs='logprobs'}}Yes{{or}}No{{/select}}

{{#if (equal ethic "Yes")~}}
Final Answer: I'm sorry, but I can't answer that.
{{else}}

{{#user~}}
Here are the relevant documents from our database:{{search question}}
Given the documents listed, can you determine an answer to the following question based solely on the provided information: {{question}} Note that your response MUST contain either 'yes' or 'no'.
{{~/user}}

Observation: I need to determine if I can infer an answer to the question based solely on the returned documents.
Thought: Let's first gen a bullet points summary of the returned documents trying to grasp the most relevant elements to the question.
Summary {{gen 'summary' temperature=0 max_tokens=100}}
Decision:{{#select 'answer' logprobs='logprobs'}}Yes{{or}}No{{/select}}

{{#if (equal answer "Yes")~}}
Thought: I believe I can answer {{question}} based on the information contained in the summary. 
Final Answer: {{gen 'answer' temperature=0.7 max_tokens=50}}
{{else}}
Thought: I don't think I can answer the question based on the information contained in the returned documents.
Final Answer: I'm sorry, but I don't have sufficient information to provide an answer to this question.
{{/if}}

{{/if}}
{{~/assistant}}"""