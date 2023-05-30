<template>
  <div class="container">
    <h1 class="title">Guidance Langchain App</h1>
    <div class="button-container">
      <button class="btn" @click="loadModel">Load Model</button>
      <button class="btn" @click="loadTools">Load Tools</button>
      <!-- Reload Modules Button -->
      <button class="btn" @click="reloadModules">Reload Modules</button>
    </div>
    <div class="form-group">
      <input class="form-input" v-model="question" placeholder="Enter a question here..." />
      <button class="btn submit-btn" @click="submitQuestion">Submit</button>
    </div>
    <div v-if="answer" class="answer-container">
      <h2 class="subtitle">Reasoning</h2>
      <p class="text">{{ answer.reasoning }}</p>
      <h2 class="subtitle">Final Answer</h2>
      <p class="text">{{ answer.finalAnswer }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      question: '',
      answer: null,
    };
  },
  methods: {
     async loadModel() {
  try {
    const response = await axios.post('http://localhost:5001/load_model');
    console.log(response.data); // you can handle the response as needed
  } catch (error) {
    console.error(error);
  }
},
    async loadTools() {
      try {
        const response = await axios.post('http://localhost:5001/load_tools');
        console.log(response.data); // you can handle the response as needed
      } catch (error) {
        console.error(error);
      }
    },
    async submitQuestion() {
      try {
        const response = await axios.post('http://localhost:5001/run_script', { question: this.question });
        let responseData = response.data.answer;

        const startString = "Anupama Nadella is 50 years old.";
        const startStringIndex = responseData.indexOf(startString);
        
        // We add the length of startString to get the index immediately after it
        let reasoningData = responseData.slice(startStringIndex + startString.length);

        // Now we want to remove the final answer from reasoningData
        const splitData = reasoningData.split("Final Answer:");
        let finalAnswer = "No final answer found.";

        // Check if there are at least 3 instances of "Final Answer:"
        if (splitData.length >= 2) {
          // The second instance is at index 1 because array indices start at 0
          finalAnswer = splitData[1].trim();
          // Remove final answer from reasoningData
          reasoningData = splitData[0].trim();
        }

        this.answer = {
          finalAnswer: finalAnswer,
          reasoning: reasoningData
        };
      } catch (error) {
        console.error(error);
      }
    },
    async reloadModules() {
      try {
        const response = await axios.post('http://localhost:5001/reload_modules');
        console.log(response.data); // handle the response as needed
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  background-color: #f6f6f6;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.title {
  text-align: center;
  margin-bottom: 25px;
}

.subtitle {
  margin-top: 20px;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.form-input {
  flex-grow: 1;
  margin-right: 20px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.btn {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  color: #fff;
  background-color: #007BFF;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #0056b3;
}

.submit-btn {
  flex-basis: 100px;
}

.answer-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
}

.text {
  margin-bottom: 20px;
}
</style>

