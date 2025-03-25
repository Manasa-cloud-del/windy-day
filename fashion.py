import openai
import streamlit as st
import pandas as pd

# Set your OpenAI API key
openai.api_key = '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'

# Function to analyze sentiment using OpenAI
def analyze_sentiment(text):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # You can also try other models like "gpt-3.5-turbo"
            prompt=f"Analyze the sentiment of the following review:\n\n{text}\n\nSentiment (positive, negative, neutral):",
            max_tokens=50,  # We only need a short response
            timeout=600,
            temperature=0  # Set to 0 to get deterministic output
        )
        sentiment = response.choices[0].text.strip()
        return sentiment
    except Exception as e:
        return f"Error: {e}"

# Function to process the data and analyze sentiment for each review
def sentiment_analysis_on_reviews(df):
    # Check if the "Sample Review" column exists
    if 'Sample Review' not in df.columns:
        st.error("The 'Sample Review' column is missing in the uploaded file.")
        return df
    
    # Apply sentiment analysis to the 'Sample Review' column
    df['Sentiment'] = df['Sample Review'].apply(analyze_sentiment)
    return df

# Streamlit UI
def data_analysis_dashboard():
    st.title("Data Analysis Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Upload excel File", type=["xlsx"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        # Display dataframe preview
        st.write("Data preview:")
        st.dataframe(df.head())
        
        # Perform sentiment analysis on the 'Sample Review' column
        df = sentiment_analysis_on_reviews(df)
        
        
        # Show the results
        st.subheader("Sentiment Analysis Results")
        st.dataframe(df[['Sample Review', 'Sentiment']])

users_db = {}

# Function to handle the sign-up process
def sign_up_user():
    st.title("Sign Up Form")
    
    # Collecting user inputs with unique keys
    username = st.text_input("Username", key="username_input")
    email = st.text_input("Email", key="email_input")
    password = st.text_input("Password", type="password", key="password_input")
    
    # Handle sign up button
    if st.button("Sign Up", key="signup_button"):
        if username and email and password:
            if username in users_db:
                st.error("Username already exists!")
            else:
                users_db[username] = {"email": email, "password": password}
                st.success("User signed up successfully!")
                st.session_state.signed_up = True  # Set signed_up to True after successful sign-up
                st.session_state.username = username  # Save username in session state
                st.experimental_rerun()  # Rerun the app to go to the next step
        else:
            st.error("Please fill out all fields.")


# Main app flow
def main():
    # Initialize session state if it hasn't been set yet
    if "signed_up" not in st.session_state:
        st.session_state.signed_up = False  # Initialize the signed_up key
    
    if not st.session_state.signed_up:
        sign_up_user()
    else:
        data_analysis_dashboard()
    
    # Run the app
if __name__ == "__main__":
    main()
