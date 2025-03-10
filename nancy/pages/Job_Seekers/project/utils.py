import streamlit as st
class utils:
  flag = False
  flag1 = False
  resetT = False
  email = " "
  @classmethod
  def init_session_state(self):
    #st.session_state.logged_in = False
    st.session_state['selected_option'] = 'Login'
    st.session_state['button_clicked'] = False
    st.session_state['signout'] = False
    st.session_state['email_placeholder'] = ''
    st.session_state['password_placeholder'] = ''
    st.session_state['show_login'] = True
    st.session_state['show_signup'] = True
    # Additional session state variables
    st.session_state['user_authenticated'] = False
    st.session_state['show_admin_form']= False
    if 'logged_in' not in st.session_state:
      st.session_state.logged_in = False
  @classmethod
  def login_state(self):
    #st.session_state['signedout'] = True
    st.session_state['signout'] = True
    st.session_state['user_authenticated'] = True
    if st.session_state.user_authenticated:
      self.flag = True
    st.session_state['show_login'] = False
    st.session_state['show_signup'] = False
    st.session_state['show_admin_form'] = True
    st.session_state.logged_in = True

  @classmethod
  def sign_out(self):
      #st.session_state['button_clicked'] = False
      #st.session_state['signedout'] = False
      st.session_state['signout'] = False
      #st.session_state['username'] = ""
      #st.session_state['useremail'] = ""
      st.session_state['email_placeholder'] = st.empty()
      st.session_state['password_placeholder'] =' '
      st.session_state['show_login'] = True
      st.session_state['show_signup'] = True
      st.session_state['show_admin_form'] = False
      self.flag = False
      st.session_state.logged_in = False
      #st.session_state['form_key'] = 'some_unique_key'  
     
  @classmethod
  def forgot_password(self,reset_token):
    self.flag1 = True
    self.resetT = reset_token
    #print("Set the flags ", self.resetT, self.flag1)

  @classmethod
  def password_set(self):
    self.flag1 = False
