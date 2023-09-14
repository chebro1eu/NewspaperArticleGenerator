import streamlit as st, tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
from creds import serperkey,apikey
# Streamlit app
st.subheader('Last Week In...')

# Get OpenAI API key, Serper API key, number of results, and search query
with st.sidebar:
    openai_api_key = apikey
    serper_api_key = serperkey
    num_results = st.number_input("Number of Search Results", min_value=3, max_value=10)
    st.caption("*Search: Uses Serper API only, retrieves search results.*")
    
search_query = st.text_input("Search Query", label_visibility="collapsed")
col1, col2 = st.columns(2)

# If the 'Search' button is clicked
if col1.button("Search"):
    # Validate inputs
    if not openai_api_key.strip() or not serper_api_key.strip() or not search_query.strip():
        st.error(f"Please provide the missing fields.The apikeys or the search query")
    else:
        try:
            with st.spinner("Please wait..."):
                # Show the top X relevant news articles from the previous week using Google Serper API
                search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=serper_api_key)
                result_dict = search.results(search_query)

                if not result_dict['news']:
                    st.error(f"No search results for: {search_query}.")
                else:
                    for i, item in zip(range(num_results), result_dict['news']):
                        st.success(f"Title: {item['title']}\n\nLink: {item['link']}\n\nSnippet: {item['snippet']}")
        except Exception as e:
            st.exception(f"Exception: {e}")


            