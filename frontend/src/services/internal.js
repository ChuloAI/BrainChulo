import config from '../config';

class InternalService {
    constructor() {
        this.baseUrl = config.baseUrl;
    }

    /* Get the current conversation or create a new one */
    async getConversation(id) {
        if(id) {
            return await this.request(`/conversations/${id}`, "GET");
        } else {
            // POST to /conversations to create a new conversation
            return await this.request('/conversations', 'POST')
        }
    }

    /* Send a message to a conversation */
    async sendMessage(conversationId, message) {
        return await this.request(`/conversations/${conversationId}/messages`, 'POST', message);
    }

    /* Upload file */
    async uploadFile(conversationId, file) {
        const formData = new FormData();
        formData.append("conversation_id", conversationId);
        formData.append("file", file.file, file.file.name);

        const response = await fetch(`${this.baseUrl}/conversations/${conversationId}/files`, {
            method: "POST",
            body: formData,
            headers: {
                "accept": "application/json"
            }
        });

        return response.json();
    }

    /* Query the LLM */
    async queryLLM(query) {
        return await this.request(`/llm`, 'POST', {}, {}, {query: query});
    }

    /* Upvote a message */
    async upvoteMessage(conversationId, messageId) {
        return await this.request(`/conversations/${conversationId}/messages/${messageId}/upvote`, 'POST');
    }

    /* Downvote a message */
    async downvoteMessage(conversationId, messageId) {
        return await this.request(`/conversations/${conversationId}/messages/${messageId}/downvote`, 'POST');
    }

    /* Reset a message vote */
    async resetMessageVote(conversationId, messageId) {
        return await this.request(`/conversations/${conversationId}/messages/${messageId}/resetVote`, 'POST');
    }

    /* Reset the Database */
    async resetDatabase() {
        return await this.request(`/reset`, 'POST');
    }

    async request(url, method, payload = {}, headers = {}, params = { }) {
        if(method.toLowerCase() == "get") payload = undefined;
        else payload = JSON.stringify(payload);
        
        const defaultHeaders = {
            'Access-Control-Request-Method': 'GET, DELETE, HEAD, POST, OPTIONS',
            'accept': 'application/json',
            'Content-Type': 'application/json'
        };

        let fullPath = `${this.baseUrl}${url}`;

        if (Object.keys(params).length > 0) {
            fullPath = `${fullPath}?${new URLSearchParams(params).toString()}`;
        }

        const response = await fetch(fullPath, {
            method: method,
            body: payload,
            mode: 'cors',
            headers: Object.assign({}, defaultHeaders, headers),
        });

        return response.json();
    }
}

export default new InternalService();