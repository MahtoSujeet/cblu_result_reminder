from datetime import datetime
import os

import requests
from bs4 import BeautifulSoup


ADHAR = os.getenv("ADHAR")
REGNO= os.getenv("REGNO")


RESPONSETEXT = """<select class="form-control" data-val="true" data-val-required="The AcademicSessionID field is required." id="AcademicSessionID" name="AcademicSessionID"><option selected="selected" value="0">-- Select Session --</option>
<option selected="selected" value="0">Old Result</option>
<option value="7">Jul-Aug 2023</option>
<option value="9">December 2023</option>
</select>"""

class CBLUAPI:
    def __init__(self):
        self.base_url = "https://result.cblu.online/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_token(self):
        response = self.session.get(self.base_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            token_element = soup.find("input", {"name":"__RequestVerificationToken"})
            return token_element.get("value")

        return "ERORR: " + str(response.text)




    def is_result_out(self, token) -> bool:

        payload=f"RegistrationNo={REGNO}&AadharNo={ADHAR}&ResultType=0&__RequestVerificationToken={token}"

        headers = {
           "Content-Type": "application/x-www-form-urlencoded",
           "Content-Length": str(len(payload)),
           "Host": "result.cblu.online",
           "Origin": "https://result.cblu.online",
           "Referer": "https://result.cblu.online/",
        }

        self.session.headers.update(headers)
        response = self.session.post(self.base_url, data=payload)

        with open("logs.txt", "a") as f:
            f.write(f"Checked on {datetime.now()}\n")

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
           
            parent_element = soup.find(id='AcademicSessionID')
            self.text = str(parent_element)
            return (str(parent_element)!=RESPONSETEXT)


        return False

if __name__=="__main__":
    client = CBLUAPI()
    token = client.get_token()
    flag = client.is_result_out(token)
    if flag:
        print("No change")
    else: print("change")


