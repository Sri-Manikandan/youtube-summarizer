import streamlit as st
from pytube import YouTube
from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()

chat = ChatOpenAI(model="gpt-3.5-turbo")

client = OpenAI()

def process_video(url):
    try:
        yv = YouTube(url)
    except:
        st.error("Invalid URL!")
    d_video = yv.streams.filter(only_audio=True).first()
    try:  
        d_video.download(filename="temp.mp3")
    except:  
        st.error("Some Error!")
    audio_file = open("temp.mp3", 'rb')
    transcription = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )

    messages = [
        SystemMessage(content="You're a helpful assistant that summarize the content given to you."),
        HumanMessage(content=f"Help me to summarize the content of this video transcription in detail,{transcription}"),
    ]
    response = chat.invoke(messages)
    st.write(response.content)

def main():
    with st.sidebar:
        st.header("Youtube Video Link")
        url = st.text_input(placeholder="Enter the Youtube Url", label="Enter the Youtube Url")
        if st.button('Process'):
            with st.spinner("Processing..."):
                process_video(url)
    st.header("Youtube Video Summarizer")
    st.text_input(placeholder="Ask your question here", label="Ask your question here")
    if st.button("Ask"):
        


if __name__ == '__main__':
    main()
    




