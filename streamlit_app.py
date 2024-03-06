import streamlit as st
import openai

# Function to query OpenAI API
def query_openai(prompt):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

st.title('Nonprofit Marketing Assistant')

# SECTION 1: Collecting Inputs
with st.form("input_form"):
    nonprofit_name = st.text_input('Nonprofit name')
    campaign_start_date = st.date_input('Campaign start date')
    more_info_about_campaign = st.text_area('More info about the campaign')
    submitted = st.form_submit_button('Submit')

# SECTION 2: Chat Environment
if submitted:
    custom_prompt = f"Please write a thank you letter for {nonprofit_name} that will be sent on {campaign_start_date}. Here is more info about the campaign: {more_info_about_campaign}"
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    st.session_state.conversation.append(f"Prompt: {custom_prompt}")

    # Querying OpenAI Assistant API
    openai_response = query_openai(custom_prompt)
    st.session_state.conversation.append(f"AI Response: {openai_response}")
    
    for message in st.session_state.conversation:
        st.text_area("Chat", value=message, height=300, key=message[:15])