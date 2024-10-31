import argparse
import textwrap
import glob
from multiprocessing import Pool
from contextlib import ExitStack
from timeit import default_timer as timer
import platform

def get_args():
    parser = argparse.ArgumentParser(
        description="keyword search through 36,092 threat intel reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
        search_keyword_mt.py "sharpchromium"
        search_keyword_mt.py "sharpchromium,xworm"
        ''')
    )

    parser.add_argument('keyword', action='store', type=str, help="Enter keywords to search (separated by commas)")
    args = parser.parse_args() # parse arguments

    args_dict = vars(args)

    return args_dict

def format_pool(content_files, keywords):
    """format the pool for each worker to open 5 files at a time

    Parameters:
    -----------
    content_files: list
        content.txt file paths
    keywords: str
        one or more keywords

    Returns:
    --------
    pools : list
        jobs for the workers
    """

    pools = []
    for i in range(0, len(content_files), 5):
        pools.append([content_files[i:i+5], keywords])

    return pools

def search_file(files, keywords):
    """searches each files for matching keywords

    Uses context manager to open 5 files at a time.

    Parameters:
    -----------
    files : list
        file paths to open
    keywords: str
        one or more keywords

    Returns:
    --------
    results : list
        search results
    """
    
    results = []
    keywords = keywords.split(",")

    with ExitStack() as stack:
        working_files = [stack.enter_context(open(x, "r", encoding="utf-8", errors='ignore')) for x in files]
        
        for i, lines in enumerate(working_files):
            line_hits = []

            # search each line
            for line_num, line in enumerate(lines):
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        line_hits.append([line_num + 1, line, keyword])

            # record hits for each file
            if len(line_hits):
                link_path = files[i].replace('content.txt','link.md')
                
                # read link file
                with open(link_path, 'r', encoding="utf-8", errors='ignore') as link_file:
                    line = link_file.read()
                link = line.split('](')[-1].strip()[:-1]
                
                results.append([files[i], link, line_hits])
    
    return results
    
def format_data_for_dataframe(results):
    """format the search results data for a dataframe

    Parameters:
    -----------
    results : list
        contains nested search results

    returns:
    --------
    data : list
        contains data for dataframe
    """

    data = []

    for pool in results:
        for file in pool:
            file_path = file[0]
            report_url = file[1]
            hits_list = file[2]
            
            total_keyword_hits = 0
            for hit in hits_list:
                line_num = hit[0]
                hit_text = hit[1]
                keyword = hit[2]

                total_keyword_hits += 1

            data.append([report_url, keyword, total_keyword_hits])
    
    return data

def main():
    # read args
    args = get_args()
    
    # parse keywords
    keywords = args['keyword'].split(',')
    keywords = [keyword.strip() for keyword in keywords if keyword.strip()]

    os_type = platform.system()
    # get all content files 
    if os_type == 'Windows':
        content_files = glob.glob(r".\Intel Reports\**\content.txt", recursive=True)
    else:
        content_files = glob.glob("./Intel Reports/**/content.txt", recursive=True)
    
    # prep data for the pool
    # send all keywords at once in csv format
    keywords = ",".join(keywords)
    queue = format_pool(content_files, keywords)
    
    # start multi-threaded file search
    with Pool() as pool:
        results = pool.starmap(search_file, queue)
    
    results = [item for item in results if item]
    streamlit_data = format_data_for_dataframe(results)
    print(streamlit_data)

if __name__ == "__main__":
    main()