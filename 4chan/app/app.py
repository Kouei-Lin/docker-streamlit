import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def fetch_mentions_from_4chan(board_letter, word):
    url = f"https://a.4cdn.org/{board_letter}/catalog.json"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json()
        mention_times = []
        for page in posts:
            for thread in page['threads']:
                thread_url = f"https://a.4cdn.org/{board_letter}/thread/{thread['no']}.json"
                thread_response = requests.get(thread_url)
                if thread_response.status_code == 200:
                    thread_data = thread_response.json()
                    for post in thread_data['posts']:
                        if 'com' in post and word.lower() in post['com'].lower():
                            mention_times.append(datetime.fromtimestamp(post['time']).hour)
        return mention_times
    else:
        return None

def main():
    st.title("When does Sir post?")

    board_letter = st.text_input("Board Letter (e.g. 'biz'): ").lower()
    word = st.text_input("Word to search (e.g. 'kleros'): ").lower()

    if st.button("Count Mentions"):
        if board_letter and word:
            mention_times = fetch_mentions_from_4chan(board_letter, word)
            if mention_times is not None:
                st.write(f"Total mentions: {len(mention_times)} times")

                # Create a pandas DataFrame to count mentions by hour
                mention_counts = pd.Series(mention_times).value_counts().sort_index()

                # Plot the scatter chart with axis labels
                plt.figure(figsize=(10, 6))
                plt.scatter(mention_counts.index, mention_counts.values, marker='o')
                plt.xlabel("Hour of the Day")
                plt.ylabel("Mentions Count")
                plt.title("Hourly Mentions Count throughout the Day")
                plt.xlim(0, 24)  # Set x-axis limits from 0 to 24
                plt.ylim(0, mention_counts.max() + 1)  # Set y-axis limits
                plt.xticks(range(0, 25))
                plt.yticks(range(int(mention_counts.max()) + 1))
                st.pyplot(plt)
            else:
                st.write("Failed to fetch data from 4chan API.")
        else:
            st.write("Please enter both the board letter and word.")

if __name__ == "__main__":
    main()

