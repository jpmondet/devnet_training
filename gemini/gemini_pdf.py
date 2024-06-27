#! /usr/bin/env python3

### Install required modules and set the envvar for Gemini API Key
# pip install google.generativeai
# pip install langchain-google-genai
# pip install langchain
# pip install langchain_community
# pip install jupyter

# export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

# Import Modules
from argparse import ArgumentParser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter


def summarize(url: str) -> str:
    # Initialize Model
    #llm = ChatGoogleGenerativeAI(model="gemini-pro")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    # Load the blog
    # loader = WebBaseLoader(url)
    # loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    #loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    loader = PyPDFLoader(url)
    docs = loader.load()


    # Define the Summarize Chain
    template = """Write the key points as a list of the following:
        "{text}"
        CONCISE SUMMARY:"""

    prompt = PromptTemplate.from_template(template)

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=600, length_function=len, add_start_index=True)
    # texts = text_splitter.create_documents([docs[0].page_content])
    # chain = load_summarize_chain(llm, chain_type="map_reduce")
    # chain.run(texts)

    # Invoke Chain
    response = stuff_chain.invoke(docs)
    # print(response["output_text"])
    return response["output_text"]


def main() -> None:
    parser = ArgumentParser(
        prog="sum_articles",
        description="Sum articles passed as parameter",
    )
    parser.add_argument("-u", "--url", type=str, help="url of the article to sum")
    args = parser.parse_args()

    summary: str = summarize(args.url)
    print(summary)


if __name__ == "__main__":
    main()
