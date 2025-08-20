import random

def generate_captcha():
    captcha='   '
    for i in range(2):
        a=str(random.randint(0,9))
        b=chr(random.randint(97,122))  #lower case
        c=chr(random.randint(65,80))  #upper case
        captcha=captcha+' '+a+' '+b+' '+c+' '
        #return(captcha)
        #captcha += f'{a} {b} {c}'
    return(captcha + '    ')
generate_captcha()
