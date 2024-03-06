from openai import OpenAI
import streamlit as st

# Title for your app
st.title("Thank You Letter Writer")

# Initializing the OpenAI client with the API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Ensuring necessary variables are in the session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Form for initial user input
with st.form("user_info"):
    nonprofitName = st.text_input("Nonprofit Name")
    moreInfo = st.text_input("More Info")
    submitted = st.form_submit_button("Submit")

if submitted:
    first_prompt = f"Please write a thank you letter for donors of {nonprofitName}. Here is more info: {moreInfo}"
    st.session_state.messages.append({"role": "user", "content": first_prompt})

    with st.chat_message("user"):
        st.markdown(first_prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        # Assuming st.write_stream is a hypothetical function to handle streaming responses
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
# Displaying previous chat messages
#for message in st.session_state.messages:
#    with st.chat_message(message["role"]):
#        st.markdown(message["content"])

# Chat input for additional messages
if prompt := st.chat_input("What is up?"):
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
        # Assuming st.write_stream is a hypothetical function to handle streaming responses
        response = st.write_stream(stream)  
    st.session_state.messages.append({"role": "assistant", "content": response})