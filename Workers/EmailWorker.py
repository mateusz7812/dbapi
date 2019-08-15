import smtplib


class EmailWorker:
    def prepare(self):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("thelistermaster@gmail.com", "Lists49admiN")
            s.quit()
            return True
        except Exception:
            return False

    def send(self, values: {}):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("thelistermaster@gmail.com", "Lists49admiN")

        message = values["message"]
        s.sendmail(values["sender"], values["receiver"], message)

        s.quit()
        return True
