#Basic Structure of GUI 
from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox
import time,random
from captcha_text import generate_captcha
from PIL import Image, ImageTk
from table_creation import generate
from email_test import send_openacn_ack, send_otp,send_otp_4_pass
import sqlite3 
import re



#call the tables_creation python file
generate()

############################ Header #########################
#Date/time Funtion
def show_dt():
    dt=time.strftime("%A %d-%b-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000,show_dt) #ms (1  sec)

#Animation of multiple image
list_imgs=['image/img1.png','image/img2.png','image/img3.png','image/img4.png','image/img5.png']
def image_animation():
    index=random.randint(0,4)
    img=Image.open(list_imgs[index]).resize((170,100))
    #convert jpgpr png image into ImageTk(bcz in GUI ImageTk images is work)
    imgtk=ImageTk.PhotoImage(img,master=root)
    #Put the image on header
    logo_lbl=Label(root,image=imgtk)
    logo_lbl.place(relx=0,rely=0)

    logo_lbl.image=imgtk
    logo_lbl.after(1000,image_animation)

root=Tk()
root.state('zoomed')
root.configure(bg='pink')

#Main Title of GUI
title_lbl=Label(root,text="Banking Automation",fg='blue',bg='pink',font=('Arial',40,'bold','underline'))
title_lbl.pack()

#Date and Time
dt_lbl=Label(root,font=('Arial',14),bg ='pink')
dt_lbl.pack(pady=3)
show_dt()

#Open Images
img=Image.open('image/img7.jpg').resize((170,100))
#convert jpgpr png image into ImageTk(bcz in GUI ImageTk images is work)
imgtk=ImageTk.PhotoImage(img,master=root)

#Put the image on header
logo_lbl=Label(root,image=imgtk)
logo_lbl.place(relx=0,rely=0)

#call the image animation function
image_animation()

################################## Footer ######################
# Footer code
footer_lbl=Label(root,font=('Arial',13,'bold'),fg='blue',bg='pink',text="Developed by \nTazeen @ 8890568979")
footer_lbl.pack(side='bottom')

####################### Inner Frame #######################
#for referesh captcha
code_captcha=generate_captcha()

#code of inner frame scrren
def main_screen():

    #Code of refresh captcha
    def refresh_captcha():
        global code_captcha
        code_captcha=generate_captcha()
        captcha_value_lbl.configure(text=code_captcha) 
    
    #boarder of frame
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.76)
     
    
    #Destroy main screen when we click on submit
    def forget():
        frm.destroy()
        fp_screen()
    
    #login Finction
    def login():
        #utype store the user selection choice like user/admin
        utype=acntype_cb.get()
        #uacn store the user acn no
        uacn=acnno_e.get()
        #upass store the user password
        upass=pass_e.get()

        #Manadatory rigt captcha
        ucaptcha=captcha_e.get()
        global code_captcha
        code_captcha=code_captcha.replace(' ','')

        if utype=='Admin':
            if uacn=='0' and upass=='admin':
                if code_captcha==ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Login","Invalid Captcha")    
            else:
                messagebox.showerror("Login","You are not Admin!")
            
        else:
            
            if code_captcha==ucaptcha:

                #selection of user is acn no and password is not match to the database show invalid otherwise valid
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where acn_acno=? and acn_pass=?'
                curobj.execute(query,(uacn,upass))
                row=curobj.fetchone()
                if row==None:
                    messagebox.showerror("Login","Invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(row[0],row[1])                
            else:
                messagebox.showerror("Login","Invalid captcha")

    #Account Type Label
    acntype_lbl=Label(frm,text='ACN Type',font=('Arial',13,'bold'),bg='powder blue')
    acntype_lbl.place(relx=.3,rely=.1)
    
    #Drop down option
    acntype_cb=Combobox(frm,values=['User','Admin'], font=('Arial',13,))
    #Default value is at 0 position
    acntype_cb.current(0)
    acntype_cb.place(relx=.40,rely=.1)
    
    
    #Account Number Label
    acnno_lbl=Label(frm,text='🔑 ACN',font=('Arial',13,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.3,rely=.2)
    
    #Account number entry
    acnno_e=Entry(frm,font=('Arial',13),bd=5)
    acnno_e.place(relx=.40,rely=.2)
    #cursor automatically come to entry of the user
    acnno_e.focus()
    
     
    #Password Label
    pass_lbl=Label(frm,text='🔒 Password',font=('Arial',13,'bold'),bg='powder blue')
    pass_lbl.place(relx=.3,rely=.3)
    
    #Password entry
    pass_e=Entry(frm,font=('Arial',13,),bd=5,show='*')
    pass_e.place(relx=.40,rely=.3) 


    #Capture label
    captcha_lbl=Label(frm,text='Captcha',font=('Arial',13,'bold'),bg='powder blue')
    captcha_lbl.place(relx=.3,rely=.4)

    #Capture Automatically generate from other code
    captcha_value_lbl=Label(frm,text=code_captcha,fg='green',font=('Arial',13,'bold'))
    captcha_value_lbl.place(relx=.40,rely=.4)

    #Making Refresh Button
    refresh_btn=Button(frm,text="refresh 🔄",command=refresh_captcha)
    refresh_btn.place(relx=.55,rely=.40)

    #captcha entry
    captcha_e=Entry(frm,font=('Arial',13,'bold'),bd=5)
    captcha_e.place(relx=.40,rely=.5)

    #Login Button
    submit_btn=Button(frm,text='Login',command=login,width=25,bg='yellow',bd=4,font=('Arial',13,'bold'))
    submit_btn.place(relx=.39,rely=.6)

    #Forgot Password Button
    fp_btn=Button(frm,text='Forget Password',command=forget,width=25,bg='yellow',bd=4,font=('Arial',13,'bold'))
    fp_btn.place(relx=.39,rely=.7)

    #New User Button
    #new_btn=Button(frm,text="New User",bg='yellow',bd=4,font=('Arial',13,'bold'))
    #new_btn.place(relx=.52,rely=.7)

#Screen when we click on forget password
def fp_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.76)

    #Function for back button
    def back():
        frm.destroy()
        main_screen()

    #forget password email otp
    def fp_pass():
        uemail=email_e.get()
        uacn=acnno_e.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where acn_acno=?'
        curobj.execute(query,(uacn,))
        torow=curobj.fetchone()
        if torow==None:
            messagebox.showerror("Forgot Password","ACN does not exist")
        else:
            if uemail==torow[3]:
                otp=random.randint(1000,9999)
                send_otp_4_pass(uemail,otp)
                messagebox.showinfo("Forgot Password","Otp send to your registered email, Kindly verify")
                    
                #verify otp function for forgot pass
                def verify_otp():
                        
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='select acn_pass from accounts where acn_acno=?'                          
                            curobj.execute(query,(uacn,))                        
                            #conobj.commit()
                            #conobj.close()
                            messagebox.showinfo('Forgot Password',f"Your Password is {curobj.fetchone()[0]} ")
                            conobj.close()
                            frm.destroy()
                            main_screen()
                        else:
                            messagebox.showerror("Forgot Password","Invalid otp!")
                
                otp_e=Entry(frm,width=27,font=('Arial',11),bd=4)
                otp_e.place(relx=.4,rely=.6)
                otp_e.focus()
                    
                #verify Button after user select user login
                verify_btn=Button(frm,text='Verify',bg='yellow',bd=5,font=('Arial',11,'bold'),command=verify_otp)
                verify_btn.place(relx=.8,rely=.6)

            else:
                messagebox.showerror("Forgot Password","Email is not matched")   

    #Back Button
    back_btn=Button(frm,text='Back',bg='yellow',bd=5,font=('Arial',13,'bold'),command=back)
    back_btn.place(relx=0,rely=0)

    # Forget password ask for Account Number Label
    acnno_lbl=Label(frm,text='🔑 ACN',font=('Arial',13,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.3,rely=.2)
    
    # Forget password ask for Account number entry
    acnno_e=Entry(frm,font=('Arial',13),bd=5)
    acnno_e.place(relx=.40,rely=.2)
    #cursor automatically come to entry of the user
    acnno_e.focus()

    #Forget password Email Label
    email_lbl=Label(frm,text='📧 Email',font=('Arial',13,'bold'),bg='powder blue')
    email_lbl.place(relx=.3,rely=.3)
    
    #Forget password Email Entry 
    email_e=Entry(frm,font=('Arial',13),bd=5)
    email_e.place(relx=.40,rely=.3)

    #Forget Password Submit Button
    sub_btn=Button(frm,text='Submit',command=fp_pass,width=25,bg='yellow',bd=4,font=('Arial',13,'bold'))
    sub_btn.place(relx=.39,rely=.4)

#Admin screen Function  
def admin_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#00ffea")
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.76)

    # logout Function for destroy screen after logout in admin login
    def logout():
        frm.destroy()
        main_screen()

    #logout Button after user select admin login
    logout_btn=Button(frm,text='logout',bg='yellow',bd=5,font=('Arial',13,'bold'),command=logout)
    logout_btn.place(relx=.93,rely=0)


    #Open function when user click on admin and then open acn button 
    def open():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of text after click on opn acn button in admin login
        t_lbl=Label(ifrm,text='This open account screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        #To get the details of user to fill the open account entry in admin login
        def openac():
            uname=name_e.get()
            uemail=email_e.get()
            umob=mob_e.get()
            uadhar=adhar_e.get()
            uadr=adr_e.get()
            udob=dob_e.get()
            ugender=gender_e.get()
            upancard=pancard_e.get()
            upass=generate_captcha()
            upass=upass.replace(' ','')
            ubal=0
            uopendate=time.strftime("%A %d-%b-%Y")

            #field does not be entry(empty validation)
            if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadr)==0 or len(udob)==0 or len(upancard)==0 or len(ugender)==0:
                messagebox.showerror("Open Account","Empty field are not allowed")
                return
            
            #email validation
            match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+",uemail)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of email")
                return
            
            #mob validation
            match=re.fullmatch(r"[6-9][0-9]{9}",umob)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of mob")
                return
            
            #adhar validation
            match=re.fullmatch(r"[0-9]{12}",uadhar)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of adhar")
                return
            
            #dob validation  
            match=re.fullmatch(r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$",udob)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of date of birth")
                return
             
            #pancard validation
            match=re.fullmatch(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$",upancard)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of pancard")
                return
            
            #Gender validation
            match=re.fullmatch(r"^(Male|Female|None)$",ugender)
            if match==None:
                messagebox.showerror("Open Account","Kindly check format of gender")
                return
            

            #connect to database
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,uadr,udob,ugender,upancard,ubal,uopendate))
            conobj.commit()
            conobj.close()
            
            #connect with database to find acn no
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("select max(acn_acno) from accounts")
            uacn=curobj.fetchone()[0]
            conobj.close()

            #call the email function
            send_openacn_ack(uemail,uname,uacn,upass)
 
            #message box
            messagebox.showinfo("Account","Account Opened and details send to email")
            frm.destroy()
            admin_screen()
            

        #name Label after click on open acn button in admin login
        name_lbl=Label(ifrm,text='Name',width=10,font=('Arial',11,'bold'))
        name_lbl.place(relx=.04,rely=.17)
    
        #name entry after click on open acn button in admin login
        name_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        name_e.place(relx=.20,rely=.17)
        #cursor automatically come to entry of the user
        name_e.focus()


        #email Label after click on open acn button in admin login
        email_lbl=Label(ifrm,text='Email Id',width=10,font=('Arial',11,'bold'))
        email_lbl.place(relx=.04,rely=.32)
    
        #email entry after click on open acn button in admin login
        email_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        email_e.place(relx=.20,rely=.32)

        #mob no Label after click on open acn button in admin login
        mob_lbl=Label(ifrm,text='Mobile No',width=10,font=('Arial',11,'bold'))
        mob_lbl.place(relx=.04,rely=.47)
    
        #mob entry after click on open acn button in admin login
        mob_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        mob_e.place(relx=.20,rely=.47)

        #adhar no Label after click on open acn button in admin login
        adhar_lbl=Label(ifrm,text='Adhar No',width=10,font=('Arial',11,'bold'))
        adhar_lbl.place(relx=.04,rely=.62)
    
        #adhar entry after click on open acn button in admin login
        adhar_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        adhar_e.place(relx=.20,rely=.62)

        #address Label after click on open acn button in admin login
        adr_lbl=Label(ifrm,text='Address',width=10,font=('Arial',11,'bold'))
        adr_lbl.place(relx=.55,rely=.17)
    
        #address entry after click on open acn button in admin login
        adr_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        adr_e.place(relx=.70,rely=.17)

        #DOB Label after click on open acn button in admin login
        dob_lbl=Label(ifrm,text='DOB',width=10,font=('Arial',11,'bold'))
        dob_lbl.place(relx=.55,rely=.32)
    
        #DOB entry after click on open acn button in admin login
        dob_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        dob_e.place(relx=.70,rely=.32)

        #gender Label after click on open acn button in admin login
        gender_lbl=Label(ifrm,text='Gender',width=10,font=('Arial',11,'bold'))
        gender_lbl.place(relx=.55,rely=.47)
    
        #gender entry after click on open acn button in admin login
        gender_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        gender_e.place(relx=.70,rely=.47)

        #pancard Label after click on open acn button in admin login
        pancard_lbl=Label(ifrm,text='PanCard No',width=10,font=('Arial',11,'bold'))
        pancard_lbl.place(relx=.55,rely=.62)
    
        #pancard entry after click on open acn button in admin login
        pancard_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        pancard_e.place(relx=.70,rely=.62)



        #open acn button when user fill the entry in open acn admin login 
        open_btn=Button(ifrm,command=openac,width=10,text='Open ACN',fg='green',bd=4,font=('Arial',13,'bold'))
        open_btn.place(relx=.4,rely=.87)
    


    #close function when user click on admin and then close acn button 
    def close():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of text after click on close acn button 
        t_lbl=Label(ifrm,text='This close account screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        #close acn function through otp
        def send_close_otp():
            uacn=acnno_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(uacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Close Accounts","ACN does not exist")
            else:
                otp=random.randint(1000,9999)
                send_otp_4_pass(torow[3],otp)
                messagebox.showinfo("Close Accounts","Otp send to your registered email, Kindly verify")
                    
                #verify otp function for forgot pass
                def verify_otp():
                                                                      
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query='delete from accounts where acn_acno=?'                          
                            curobj.execute(query,(uacn,))                        
                            #conobj.commit()
                            #conobj.close()
                            messagebox.showinfo('Close Account',f"Account Closed")
                            conobj.commit()
                            conobj.close()
                            frm.destroy()
                            admin_screen()
                        else:
                            messagebox.showerror("Close Accounts","Invalid otp!")
                
                otp_e=Entry(frm,width=27,font=('Arial',11),bd=4)
                otp_e.place(relx=.4,rely=.6)
                otp_e.focus()
                    
                #verify Button after user select user login
                verify_btn=Button(frm,text='Verify',bg='yellow',bd=5,font=('Arial',11,'bold'),command=verify_otp)
                verify_btn.place(relx=.8,rely=.6)


        #Ask for acn no after close acn in admin login
        acnno_lbl=Label(ifrm,width=10,text='🔑 ACN No',font=('Arial',13,'bold'),bg='powder blue')
        acnno_lbl.place(relx=.3,rely=.2)
     
        # label for acn no after close acn in admin login
        acnno_e=Entry(ifrm,width=27,font=('Arial',13),bd=5)
        acnno_e.place(relx=.47,rely=.2)
        #cursor automatically come to entry of the user
        acnno_e.focus()

        #otp button when user fill the entry the acn no in close button in admin login 
        otp_btn=Button(ifrm,width=10,command=send_close_otp,text='Send OTP',fg='green',bd=4,font=('Arial',13,'bold'))
        otp_btn.place(relx=.70,rely=.3)
    


    #view function when user click on admin and then view acn button 
    def view():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of text after click on view acn button 
        t_lbl=Label(ifrm,text='This view account screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()
        from tktable import Table

        #inside view table
        table_headers=("ACNO.","NAME","EMAIL","MOB","OPEN DATE","BALANCE")
        mytable = Table(ifrm, table_headers,headings_bold=True)
        mytable.place(relx=.01,rely=.1,relwidth=.97,relheight=.8)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts'
        curobj.execute(query)
        for tup in curobj.fetchall():
            mytable.insert_row(tup)
        conobj.close()

    #open button when user select admin login 
    open_btn=Button(frm,width=10,text='Open ACN',command=open,fg='green',bd=4,font=('Arial',13,'bold'))
    open_btn.place(relx=.001,rely=.1)
    
    #close button when user select admin login 
    close_btn=Button(frm,width=10,text='Close ACN',command=close,fg='red',bd=4,font=('Arial',13,'bold'))
    close_btn.place(relx=.001,rely=.3)
    
    #view button when user select admin login  
    view_btn=Button(frm,width=10,text='View ACN',command=view,fg='blue',bd=4,font=('Arial',13,'bold'))
    view_btn.place(relx=.001,rely=.5)

#User screen Function  
def user_screen(uacn,uname):
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#00ffea")
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.76)

    #selection of user is acn no and password is not match to the database
    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    query='select * from accounts where acn_acno=?'
    curobj.execute(query,(uacn,))
    row=curobj.fetchone()
    conobj.close()

    # logout Function for destroy screen after logout in user login
    def logout():
        frm.destroy()
        main_screen()

     #check function when user click on user and then check acn button 
    def check():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of text after click on view acn button 
        t_lbl=Label(ifrm,text='This is check details screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()
        
        #acn info after click in check detail in user login
        acn_lbl=Label(ifrm,text=f"Account No\t=\t{row[0]}",font=('Arial',12,'bold'),bg='white',fg='black')
        acn_lbl.place(relx=.2,rely=.2)

        #balance info after click in check detail in user login
        bal_lbl=Label(ifrm,text=f"Account Balance\t=\t{row[10]}",font=('Arial',12,'bold'),bg='white',fg='black')
        bal_lbl.place(relx=.2,rely=.3)

        
        # open acn date info after click in check detail in user login
        open_lbl=Label(ifrm,text=f"Open Date\t=\t{row[11]}",font=('Arial',12,'bold'),bg='white',fg='black')
        open_lbl.place(relx=.2,rely=.4)

         #DOB info after click in check detail in user login
        dob_lbl=Label(ifrm,text=f"Date of Birth\t=\t{row[7]}",font=('Arial',12,'bold'),bg='white',fg='black')
        dob_lbl.place(relx=.2,rely=.5)

        #adhar info after click in check detail in user login
        adhar_lbl=Label(ifrm,text=f"Adhar No\t=\t{row[5]}",font=('Arial',12,'bold'),bg='white',fg='black')
        adhar_lbl.place(relx=.2,rely=.6)


    #update function when user click on user and then update button 
    def update():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of text after click on update button 
        t_lbl=Label(ifrm,text='This is update details screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()
         
        #update acn details nd direct connect to database 
        def update_details():
            uname=name_e.get()
            upass=pass_e.get()
            uemail=email_e.get()
            umob=mob_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Details Updated")
            frm.destroy()
            user_screen(uacn,None)


        #name Label after click on update acn button in user login
        name_lbl=Label(ifrm,text='Name',width=10,font=('Arial',11,'bold'))
        name_lbl.place(relx=.04,rely=.17)
    
        #name entry after click on update acn button in user login
        name_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        name_e.place(relx=.20,rely=.17)
        #cursor automatically come to entry of the user
        name_e.focus()
        #index forma first name fetch
        name_e.insert(0,row[1])


        #email entry after click on update acn button in user login
        email_lbl=Label(ifrm,text='Email Id',width=10,font=('Arial',11,'bold'))
        email_lbl.place(relx=.04,rely=.32)
    
        #email entry after click on update acn button in user login
        email_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        email_e.place(relx=.20,rely=.32)
        #index format for email fetch
        email_e.insert(0,row[3])

        #mob no Label after click on update acn button in user login
        mob_lbl=Label(ifrm,text='Mobile No',width=10,font=('Arial',11,'bold'))
        mob_lbl.place(relx=.04,rely=.47)
    
        #mob entry after click on update acn button in user login
        mob_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        mob_e.place(relx=.20,rely=.47)
        #index format for mob fetch
        mob_e.insert(0,row[4])

        #adhar no Label after click on update acn button in user login
        pass_lbl=Label(ifrm,text='Password ',width=10,font=('Arial',11,'bold'))
        pass_lbl.place(relx=.04,rely=.62)
    
        #adhar update after click on update acn button in user login
        pass_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        pass_e.place(relx=.20,rely=.62)
        pass_e.insert(0,row[2])

        #update Button after user select user login
        update_btn=Button(ifrm,text='update',bg='yellow',bd=5,font=('Arial',13,'bold'),command=update_details)
        update_btn.place(relx=.5,rely=.8)


     #deposite function when user click on user and then deposite button 
    def deposite():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of update after click on view acn button 
        t_lbl=Label(ifrm,text='This is deposite details screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        #deposite amount function
        def deposit_amt():
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_bal=acn_bal+? where acn_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Deposit',f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn,None)


        #amount Label after click on withdraw acn button in user login
        amt_lbl=Label(ifrm,text='Amount',width=10,font=('Arial',11,'bold'))
        amt_lbl.place(relx=.2,rely=.30)
    
        #amount entry after click on withdraw acn button in user login
        amt_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        amt_e.place(relx=.4,rely=.30)
        amt_e.focus()

        #deposite Button after user select user login
        deposit_btn=Button(ifrm,text='Deposite',bg='yellow',bd=5,font=('Arial',13,'bold'),command=deposit_amt)
        deposit_btn.place(relx=.5,rely=.8)


     #withdraw function when user click on user and then withdraw button 
    def withdraw():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of text after click on withdraw button 
        t_lbl=Label(ifrm,text='This is withdraw details screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        #withdraw amount function in user login
        def withdraw_amt():
            uamt=float(amt_e.get())
            if row[10]>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Withdraw',f"{uamt} Amount Withdraw")
                frm.destroy()
                user_screen(uacn,None)
            else:
                messagebox.showerror("Withdraw","Insufficient Balance")


        #amount Label after click on withdraw acn button in user login
        amt_lbl=Label(ifrm,text='Amount',width=10,font=('Arial',11,'bold'))
        amt_lbl.place(relx=.2,rely=.30)
    
        #amount entry after click on withdraw acn button in user login
        amt_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        amt_e.place(relx=.4,rely=.30)
        amt_e.focus()

        #withdraw Button after user select user login
        withdraw_btn=Button(ifrm,text='Withdraw',bg='yellow',bd=5,font=('Arial',13,'bold'),command=withdraw_amt)
        withdraw_btn.place(relx=.5,rely=.8)


    #transfer function when user click on user and then transfer button 
    def transfer():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.15,relwidth=.7,relheight=.83)
        
        #label of text after click on transfer button 
        t_lbl=Label(ifrm,text='This is transfer screen',font=('Arial',13,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        #Transfer acn function
        def transfer_amt():
            toacn=to_e.get()
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(toacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Transfer","To ACN does not exist")
            else:
                if row[10]>=uamt:
                    otp=random.randint(1000,9999)
                    send_otp(row[3],otp,uamt)
                    messagebox.showinfo("Transfer","Otp send to your registered email, Kindly verify")
                    
                    #verify otp function
                    def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query1='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                            query2='update accounts set acn_bal=acn_bal+? where acn_acno=?'

                            curobj.execute(query1,(uamt,uacn))
                            curobj.execute(query2,(uamt,toacn))

                            conobj.commit()
                            conobj.close()
                            messagebox.showinfo('Transfer',f"{uamt} Amount Transfered")
                            frm.destroy()
                            user_screen(uacn,None)
                        else:
                            messagebox.showerror("Transfer","Invalid otp!")


                    
                    otp_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
                    otp_e.place(relx=.4,rely=.6)
                    otp_e.focus()
                    
                    #verify Button after user select user login
                    verify_btn=Button(ifrm,text='Verify',bg='yellow',bd=5,font=('Arial',11,'bold'),command=verify_otp)
                    verify_btn.place(relx=.8,rely=.6)

                else:
                    messagebox.showerror("Transfer","Insufficient Bal")


        #amount Label after click on transfer acn button to which acn in user login
        to_lbl=Label(ifrm,text='To ACN',width=10,font=('Arial',11,'bold'))
        to_lbl.place(relx=.2,rely=.30)
    
        #amount entry after click on transfer acn button tp which acn in user login
        to_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        to_e.place(relx=.4,rely=.30)
        to_e.focus()

        #amount Label after click on transfer acn button in user login
        amt_lbl=Label(ifrm,text='Amount',width=10,font=('Arial',11,'bold'))
        amt_lbl.place(relx=.2,rely=.45)
    
        #amount entry after click on transfer acn button in user login
        amt_e=Entry(ifrm,width=27,font=('Arial',11),bd=4)
        amt_e.place(relx=.4,rely=.45)
        amt_e.focus()

        #transfer Button after user select user login
        transfer_btn=Button(ifrm,text='Transfer',bg='yellow',bd=5,font=('Arial',13,'bold'),command=transfer_amt)
        transfer_btn.place(relx=.5,rely=.8)


    #logout Button after user select user login
    logout_btn=Button(frm,text='logout',bg='yellow',bd=5,font=('Arial',13,'bold'),command=logout)
    logout_btn.place(relx=.93,rely=0)

    #Welcome label of text after select user login 
    wel_lbl=Label(frm,text=f'Welcome,{row[1]}',font=('Arial',13,'bold'),bg='white',fg='purple')
    wel_lbl.pack()

    #check button when user select user login 
    check_btn=Button(frm,width=15,text='Check Details',command=check,fg='green',bd=4,font=('Arial',13,'bold'))
    check_btn.place(relx=.001,rely=.15)
    
    #update button when user select user login 
    update_btn=Button(frm,width=15,text='Update Details',command=update,fg='red',bd=4,font=('Arial',13,'bold'))
    update_btn.place(relx=.001,rely=.3)
    
    #deposite button when user select user login  
    deposite_btn=Button(frm,width=15,text='Deposite',command=deposite,fg='blue',bd=4,font=('Arial',13,'bold'))
    deposite_btn.place(relx=.001,rely=.45)

    #withdraw button when user select user login  
    withdraw_btn=Button(frm,width=15,text='Withdraw',command=withdraw,fg='brown',bd=4,font=('Arial',13,'bold'))
    withdraw_btn.place(relx=.001,rely=.6)

    #transfer button when user select user login  
    transfer_btn=Button(frm,width=15,text='Transfer',command=transfer,fg='black',bd=4,font=('Arial',13,'bold'))
    transfer_btn.place(relx=.001,rely=.75)


#call the inner frame screen
main_screen()

#call the main screen/root window
root.mainloop()