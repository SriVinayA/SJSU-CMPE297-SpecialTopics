import requests
import json
import streamlit as st

class OllamaAPI:
    def __init__(self):
        self.request = {
            "url": "http://localhost:11434/api/generate",
            "headers": {
                "Content-Type": "application/json"
            },
            "data": {
                "model": "gemma2:2b",  # Updated to match your installed model
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_tokens": 2048,
                    "num_ctx": 2048  # Context window for 2B model
                }
            }
        }

    def get_response(self, prompt):
        try:
            # Simple prompt formatting
            self.request["data"]["prompt"] = prompt
            
            # Make the API call
            response = requests.post(
                self.request["url"], 
                headers=self.request["headers"], 
                json=self.request["data"]
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            return result.get("response", "No response received")
            
        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to Ollama. Please make sure Ollama is running locally."
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid response from server"

def main():
    st.set_page_config(
        page_title="Gemma 2B Chat",
        page_icon="🤖"
    )
    
    st.title("🤖 Chat with Gemma 2B")
    
    # Add a sidebar for model parameters
    with st.sidebar:
        st.header("Model Parameters")
        temperature = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.7, 0.1, 
                              help="Higher values make output more creative but less focused")
        max_tokens = st.slider("Max Response Length", 128, 2048, 1024, 64, 
                             help="Maximum number of tokens in the response")
        
        st.markdown("""
        ### Model Info
        Currently using: **Gemma 2B**
        - Lightweight but capable model
        - Good for general tasks
        - 2048 token context window
        """)

    # Initialize the API client
    if 'ollama_client' not in st.session_state:
        st.session_state.ollama_client = OllamaAPI()

    # Update model parameters based on sidebar inputs
    st.session_state.ollama_client.request["data"]["options"].update({
        "temperature": temperature,
        "max_tokens": max_tokens
    })

    # Create a chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Welcome message
    if not st.session_state.messages:
        st.markdown("""
        👋 Welcome! I'm running on the Gemma 2B model locally through Ollama.
        
        I can help you with:
        - Writing and answering questions
        - Basic code tasks
        - Simple analysis
        - General conversation
        
        Note: As a 2B parameter model, I have some limitations compared to larger models.
        """)

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response = st.session_state.ollama_client.get_response(prompt)
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Add clear chat and retry buttons in columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.experimental_rerun()
    with col2:
        if st.button("Retry Last Response", use_container_width=True) and st.session_state.messages:
            if len(st.session_state.messages) >= 2:
                # Remove the last response
                st.session_state.messages.pop()
                last_prompt = st.session_state.messages[-1]["content"]
                # Generate new response
                with st.chat_message("assistant"):
                    with st.spinner("Regenerating response..."):
                        new_response = st.session_state.ollama_client.get_response(last_prompt)
                        st.write(new_response)
                st.session_state.messages.append({"role": "assistant", "content": new_response})
                st.experimental_rerun()

if __name__ == "__main__":
    main()