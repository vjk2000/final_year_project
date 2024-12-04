import os
from dotenv import load_dotenv
import streamlit as st
import time


from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Chroma
HF_T = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_T





template = """
User: You are an AI Assistant that follows instructions extremely well.
Please be truthful and give direct answers. Refer the Below Given Examples and understand what makes an text Phishing and Spam
Examples:
1,Urgent:Account Security Alert,Your account has been compromised!Click here to reset your password now = Phishing,1
2,Attention Required: Verify Your Account,We detected unusual activity on your account. Please confirm your identity by clicking the link below=Phishing,1
3,Important: Immediate action Required,Your account is at risk! Verify your account information to avoid suspension=Phishing,1
4,Claim Your Prize Now!,Congratulations! You've won a prize. Click here to claim it now.=Phishing,1
5,Your amazon order confirmation,Your recent order cannot be processed. Click here to update payment information=Phishing,1
6,Weekly newsletter ,Stay updated with our latest news and offers.Click here to read our newsletter=Safe,0
7,Your monthly statement,Your monthly statement is ready for review. Log in to your account to view it now.=Safe,0
8,Invitation to our webinar,Join us for an exclusive webinar on soft skills. Register now to secure your spot=Safe,0
9,Your recent purchase confirmation,Thank you for your purchase! Click here to view your order details.=Safe,0
10,Reminder: Upcoming Appointment,Just a friendly reminder about your upcoming appointment. Click here for more information=Safe,0
11,Your Account Has Been Compromised,We've noticed suspicious activity on your account. Click the link to secure your account now.=Phishing,1
12,Urgent: Immediate Action Required,Your account is at risk! Click here to confirm your identity and prevent unauthorized access.=Phishing,1
13,Important: Verify Your Payment Information,Your payment details need to be updated. Please log in and verify your information to avoid account suspension=Phishing,1
14,Claim Your Reward Now!,Congratulations! You've been selected to receive a special reward. Click the link to claim it before it expires.=Phishing,1
15,Your PayPal Account Has Been Limited,We've detected unusual activity on your PayPal account. Click here to confirm your identity and restore access.=Phishing ,1
16,Weekly Update: New Product Features,Discover the latest features and improvements in our newest update. Click here to learn more.=Safe,0
17,Your Invoice Is Ready for Payment,Your invoice for [service/product] is now available. Log in to your account to view and pay it.=Safe,0
18,Invitation to Our Annual Conference,You're invited to attend our annual conference. Register now to secure your spot and take advantage of early bird pricing.=Safe,0
19,Your Flight Itinerary,Your flight itinerary for [date] is attached. Review the details and contact us if you have any questions=Safe,0
20,Reminder: Upcoming Webinar Tomorrow,Don't forget to join our webinar tomorrow on [topic]. Click here to register and reserve your spot.=Safe,0

Now for the following text Identify whether it is phishing or safe


New Text: {text}
Assistant:
"""



llm = HuggingFaceEndpoint(
    endpoint_url="huggingfaceh4/zephyr-7b-beta",
    max_new_tokens = 2048,
    repetition_penalty =  1.1,
    temperature = 0.5,
    top_p = 0.9,
    return_full_text = False,
)


prompt = ChatPromptTemplate.from_template(template)
#prompt_questions = ChatPromptTemplate.from_template(template_questions)
output_parser = StrOutputParser()


chain = (
    {
        "text": RunnablePassthrough(),
    }
    | prompt
    | llm
    | output_parser
)

st.title("phishing attack detection")
st.write(" Using LLM")
# Input section: User inputs the topic for the blog titles
user_input = st.text_input("Enter the mail content", "...")
# Button to trigger the title generation
if st.button("Generate"):
  result = chain.invoke(user_input)
  st.write(result)
