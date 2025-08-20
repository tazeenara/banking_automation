import gmail
email_id=""
app_pass="sfsj xalo ixps xpgn"

def send_openacn_ack(uemail,uname,uacn,upass):
    con=gmail.GMail(email_id,app_pass)
    sub="Congratulation😊,Account Open Successfully"
    upass=upass.replace(' ','')
    utext=f'''Hello,{uname}
Welcome to ABC Bank
Your Acc No is {uacn}
Your Pass is {upass}
Kindly change your password when you login first

Thanks
ABC Bank
Noida

'''
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp(uemail,otp,amt):
    con=gmail.GMail(email_id,app_pass)
    sub="otp for fund transfer"

    utext=f"""Your otp is {otp} to transfer amount {amt}

Kindly use this otp to complete transfer
Please don't share to anyone else

Thanks
ABC Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def send_otp_4_pass(uemail,otp):
    con=gmail.GMail(email_id,app_pass)
    sub="otp for password recovery"

    utext=f"""Your otp is {otp} to recover password


Please don't share to anyone else

Thanks
ABC Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)