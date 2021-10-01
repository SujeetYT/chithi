import streamlit as st
import markdown
import time
from mailer import Mailer

st.title("✉️ CHITHI")
st.subheader("Send emails in Bulk ⚡")
st.markdown("*****")
st.markdown("##### Who's sending the mail? 🤔")
mailid = st.text_input("Email:")
passwrd = st.text_input("Password:", type="password")

server = st.selectbox("Choose your Mail Provider", [
    "Gmail", "Yahoo", "Outlook", "Hotmail", "iCloud"])
st.warning("Please allow {}'s [Third Part Apps](http://www.google.com/settings/security/lesssecureapps) for mailing with us.".format(
    st.session_state.get("server", server)))
# TODO: Change links for Less Secure Apps of all the mail providers

st.markdown("""*****
# Tell me about recipients ✨""")
recipients = st.text_input("Recipient:")
bcc = st.text_input("Bcc: \t")
st.info("Comma separated Id's")

st.markdown("""*****
# What's the message? 🔥""")

subject = st.text_input("Subject:")
st.info(
    """We support Markdown 🎉 If you are new to Markdown check this [Guide](https://www.markdownguide.org/basic-syntax/).""")
col1, col2 = st.columns(2)
body = col1.text_area("Body:", height=300)
col2.markdown(st.session_state.get("body", body), unsafe_allow_html=True)
view_html = st.checkbox("View Raw HTML")
if view_html:
    st.code(markdown.markdown(st.session_state.get("body", body)))
attachments = st.file_uploader("Attachments:", accept_multiple_files=True)

mailer = Mailer(mailid, passwrd, server.lower())


def mail():
    mailer.send_mail(to=recipients, bcc=bcc, subject=subject,
                     body=body, attachments=attachments)
    with st.spinner("Sending..."):
        time.sleep(5)
        st.success("Mail sent successfully!")


st.button("Send 📮", on_click=mail)
