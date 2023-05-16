import config from '../config';

class InternalService {
    constructor() {
        this.baseUrl = config.baseUrl;
    }

    async getConversation(id) {
        if(id) {
            return this.request(`/conversations/${id}`, "GET");
        } else {
            // POST to /conversations to create a new conversation
            return this.request('/conversations', 'POST')
        }
    }

    async request(url, method, payload = {}, headers = {}, params = { }) {
        const defaultHeaders = {
            'Access-Control-Request-Method': 'GET, DELETE, HEAD, POST, OPTIONS',
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