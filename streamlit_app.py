import streamlit as st
import openai

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

assistant = client.beta.assistants.create(
    name="Direct Response Copywriter",
    instructions="You are an amazing copywriter. Your style is plainspoken and direct.",
    model="gpt-4-turbo-preview"
)
# Function to query OpenAI Assistant API
def query_openai_assistant(prompt):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    assistant_id = "your-assistant-id-here"  # Replace with your actual Assistant ID
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or your Assistant's model
        messages=[{"role": "user", "content": prompt}],
        assistant=assistant_id,
    )
    return response.choices[0].message['content']

st.title('Nonprofit Marketing Assistant')

# SECTION 1: Input form for generating initial prompt
with st.form("input_form", clear_on_submit=True):
    st.write("SECTION 1: Please complete these fields")
    nonprofit_name = st.text_input('Nonprofit name', key="nonprofit_name")
    campaign_start_date = st.date_input('Campaign start date', key="campaign_start_date")
    more_info_about_campaign = st.text_area('More info about the campaign', key="more_info")
    submit_button = st.form_submit_button('Generate Prompt')

# Process form submission
if submit_button:
    custom_prompt = f"Please write a thank you letter for {nonprofit_name} that will be sent on {campaign_start_date}. Here is more info about the campaign: {more_info_about_campaign}"
    st.session_state.conversation.append({"text": custom_prompt, "is_user": False})

    # Query OpenAI Assistant and append response
    ai_response = query_openai_assistant(custom_prompt)
    st.session_state.conversation.append({"text": ai_response, "is_user": True})

# Display chat interface
st.write("SECTION 2: Chat Environment")
user_input = st.chat_input("Type your message here", key="chat_input", placeholder="Enter your message...")
if user_input:
    # Append user query to conversation and get AI response
    st.session_state.conversation.append({"text": user_input, "is_user": True})
    ai_response = query_openai_assistant(user_input)
    st.session_state.conversation.append({"text": ai_response, "is_user": False})

# Render conversation
for chat in st.session_state.conversation:
    if chat["is_user"]:
        st.chat_message(chat["text"], is_user=True)
    else:
        st.chat_message(chat["text"], is_user=False)
