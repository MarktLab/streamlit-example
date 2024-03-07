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
    

   
# Form for initial user input
with st.sidebar.form("user_info"):
    nonprofitName = st.text_input("Nonprofit Name")
    moreInfo = st.text_area("More Info")
    submitted = st.form_submit_button("Submit")

if submitted:
    first_prompt = f"Please write a thank you letter for donors of {nonprofitName}. Here is more info: {moreInfo}"
    append_and_get_response(first_prompt)

# Chat input for additional messages
if additional_prompt  := st.chat_input("How can I improve this text?"):
    append_and_get_response(additional_prompt)



# Buttons for predefined actions
if st.button("Refine Tone"):
    append_and_get_response("Please refine the tone of this text to be more professional.")

if st.button("Add Gratitude"):
    append_and_get_response("Please add more expressions of gratitude.")

if st.button("Make It Shorter"):
    append_and_get_response("Please make this text shorter while keeping the essential gratitude message.")