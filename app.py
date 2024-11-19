import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Machine Learning Jobs @ Wuzzuf",
    page_icon="🤖",
    layout="wide"
)

# Title and Header Section
st.title("🤖 Machine Learning Jobs Dashboard")
st.header("Web Scraping Project")
st.markdown("""
### Scraping the data from [Wuzzuf.com](https://wuzzuf.net/)
This project is created by **ElHussin Sobhy**. Below, you can explore jobs scraped from Wuzzuf.
""")

# Load Data
data = pd.read_csv('jobs.csv')

# Sidebar for Filters and User Input
st.sidebar.header("Job Filters")
num_jobs = st.sidebar.number_input("Number of Jobs to Display", min_value=1, max_value=100, value=5)

# Multiselect for Columns
columns_to_show = st.sidebar.multiselect(
    "Select Information to Display",
    options=['Title', 'Company', 'Location', 'Date', 'Experience', 'Salary', 'Skills', 'Link'],
    default=['Title','Date', 'Company', 'Location', 'Link']
)

# Display Jobs Dynamically
st.header("Job Listings")

if not columns_to_show:
    st.warning("Please select at least one column to display.")
else:
    for i in range(min(num_jobs, len(data))):  # Ensure we don't exceed available jobs
        job_details = []
        if 'Title' in columns_to_show:
            job_details.append(f"### {i+1}. {data['title'][i]}")
        if 'Company' in columns_to_show:
            job_details.append(f"- **Company**: {data['company'][i][:-1]}")  # Clean trailing characters
        if 'Location' in columns_to_show:
            job_details.append(f"- **Location**: {data['location'][i]}")
        if 'Date' in columns_to_show:
            job_details.append(f"- **Date**: {data['date'][i]}")
        if 'Experience' in columns_to_show:
            job_details.append(f"- **Experience**: {data['experience_needed'][i]}")
        if 'Salary' in columns_to_show:
            job_details.append(f"- **Salary**: {data['salary'][i]}")
        if 'Skills' in columns_to_show:
            try:
                skills = ' - '.join(eval(data['skills'][i]))
            except:
                skills = data['skills'][i]
            job_details.append(f"- **Skills**: {skills}")
        if 'Link' in columns_to_show:
            job_details.append(f"- [Apply here]({data['link'][i]})")

        # Render job details with a separator
        st.markdown("\n".join(job_details))
        st.markdown("---")

# Display the DataFrame (Optional)
with st.expander("View Raw Data"):
    st.dataframe(data)

# Footer
st.markdown("""
---
**Contact Information**:
If you have any feedback or questions, feel free to contact me at [elhussinsobhy@gmail.com](mailto:elhussinsobhy@gmail.com).
""")
