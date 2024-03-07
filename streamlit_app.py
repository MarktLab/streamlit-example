from openai import OpenAI
import streamlit as st
import re

# Title for your app
st.title('[AFT Fundraising Writer](https://annualfundtoolkit.com)')

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
    with st.form("dynamic_form"):
        for placeholder in placeholders:
            # Replace underscores with spaces and apply title case for a prettier label
            pretty_placeholder = placeholder.replace("_", " ").title()
            # Create an appropriate field for each placeholder
            user_input = st.text_input(pretty_placeholder)
            user_inputs[placeholder] = user_input
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Fill the template with user inputs
            filled_prompt = template.format(**user_inputs)
            return filled_prompt
    return None


prompt_templates = {
    "Thank You Letter for Donors": "Please write a thank you letter for donors of {nonprofit_name}. Here is more info: {more_info}",
    "Event Reminder": "Send a reminder for {event_name} on {event_date}. Here are the details: {event_details}"
}

# Select a prompt template
with st.sidebar:
    template_option_label = st.selectbox("Choose a prompt template", options=list(prompt_templates.keys()))
    template_option = prompt_templates[template_option_label]

    # Generate form and get filled prompt based on selected template
    filled_prompt = generate_form_based_on_template(template_option)

    whynow = st.button("Why Now?")
    fight = st.button("Fight Injustice")
    gratitude = st.button("Add Gratitude")
    impact = st.button("Impact")
    concise = st.button("Make It Concise")
    woman = st.button("Woman's Voice")
    plain = st.button("Plainspoken English")

# Buttons for predefined actions
if whynow:
    append_and_get_response("Rewrite to answer these questions: Why should the reader take action now? What will happen if they don't take action?")

if fight:
    append_and_get_response("Rewrite to answer these questions: Is there a wrong that must be set right? Something to fight for or against?")

if gratitude:
    append_and_get_response("Please add more expressions of gratitude.")

if impact:
    append_and_get_response("Rewrite to answer this question: what impact is the donor having?")

if concise:
    append_and_get_response("Please make this more concise while keeping the essential message.")

if woman:
    append_and_get_response("Please write it in a woman's voice.")

if plain:
    append_and_get_response("Please use plainspoken English.")


if filled_prompt:
    append_and_get_response(filled_prompt)

# Chat input for additional messages
if additional_prompt := st.chat_input("How can I improve this text?"):
    append_and_get_response(additional_prompt)