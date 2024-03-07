from openai import OpenAI
import streamlit as st
import re

# Title for your app
st.title("Dynamic Prompt Generator")

# Initializing the OpenAI client with the API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Ensuring necessary variables are in the session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to append messages and get response
def append_and_get_response(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Function to dynamically create form based on chosen prompt template
def generate_form_based_on_template(template):
    # Find placeholders within the template
    placeholders = re.findall(r'\{(.*?)\}', template)
    
    # Create a dictionary to store user inputs for each placeholder
    user_inputs = {}
    with st.sidebar:
        with st.form("dynamic_form"):
            for placeholder in placeholders:
                # Create an appropriate field for each placeholder
                user_inputs[placeholder] = st.text_input(placeholder.capitalize())
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                # Fill the template with user inputs
                filled_prompt = template.format(**user_inputs)
                return filled_prompt
    return None

prompt_templates = {
    "Thank You Letter for Donors": "Please write a thank you letter for donors of {nonprofitName}. Here is more info: {moreInfo}",
    "Event Reminder": "Send a reminder for {eventName} on {eventDate}. Here are the details: {eventDetails}"
}

# Select a prompt template
with st.sidebar:
    template_option_label = st.selectbox("Choose a prompt template", options=list(prompt_templates.keys()))
    template_option = prompt_templates[template_option_label]

# Generate form and get filled prompt based on selected template
filled_prompt = generate_form_based_on_template(template_option)
if filled_prompt:
    append_and_get_response(filled_prompt)

# Chat input for additional messages
if additional_prompt := st.chat_input("How can I improve this text?"):
    append_and_get_response(additional_prompt)

# Buttons for predefined actions
if st.button("Refine Tone"):
    append_and_get_response("Please refine the tone of this text to be more professional.")

if st.button("Add Gratitude"):
    append_and_get_response("Please add more expressions of gratitude.")

if st.button("Make It Shorter"):
    append_and_get_response("Please make this text shorter while keeping the essential gratitude message.")