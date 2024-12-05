import streamlit as st
import subprocess
import pandas as pd
import ast
import glob
import platform
from timeit import default_timer as timer
import json

@st.cache_data
def export_df(df):
    return df.to_csv(index=False).encode("utf-8")

def execute_search(user_keywords):
    process = subprocess.run(['python', 'search_keyword_mt_sl.py', f'{user_keywords}'], capture_output=True, text=True, encoding='utf-8')

    stdout = process.stdout
    
    # any unhandled exceptions thrown during the subprocess execution will 
    # result in a blank string to be returned,
    # therefore causing a JSONDecodeError during json.loads()
    result_list = json.loads(stdout.strip())
    
    result_df = pd.DataFrame(result_list, columns=['report_url', 'keyword', 'count', 'path'])

    return result_df

def main():

    os_type = platform.system()
    # get all content files 
    if os_type == 'Windows':
        total_content_files = len(glob.glob(r".\Intel Reports\**\content.txt", recursive=True))
    else:
        total_content_files = len(glob.glob("./Intel Reports/**/content.txt", recursive=True))

    st.set_page_config(
        page_title="Search Threat Reports",
        page_icon="🔍",
        )
    st.title(f"Search {total_content_files:,} Threat Reports")

    #try:
    st.write("## Submit Keyword(s)")

    default_keyword = "anydesk"
    user_keywords = st.text_area("Enter one or more keywords in csv format", value=default_keyword)
    
    button = st.button(label="Submit")
    if button:
        start = timer()
        result_df = execute_search(user_keywords)
        end = timer()

        total_records_returned = len(result_df)
        
        if total_records_returned<=5:
            st.dataframe(result_df, height=150)
        elif total_records_returned >= 50:
            st.dataframe(result_df, height=1000)
        elif total_records_returned > 100:
            st.dataframe(result_df, height=1000)
        else:
            st.dataframe(result_df, height=200)
        
        run_time = end - start
        st.write(f"Search completed in {run_time:.2f} seconds.\nTotal Reports: {total_records_returned:,}")

        # To download the data we have just selected
        st.write("### Download Data")
        file_name = st.text_input("file name", value="search_results", key="out_file")
        
        if not '.csv' in file_name:
            file_name += '.csv'
        
        st.download_button(
            label="Press to Download",
            data=export_df(result_df),
            file_name=f"{file_name}",
            mime="text/csv",
            key="download-csv",
        )
            
    #except:
    #    st.text("Error please try again..")

if __name__ == "__main__":
    main()