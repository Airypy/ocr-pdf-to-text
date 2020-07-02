import pdfplumber
import re
from crop_pdf import making_pdf
from extract import questions_extr,answers_extr
with pdfplumber.open('GEOGRAPHY_QUIZ.pdf') as pdf:
    count=1 #Counting questions and options
    ans_count=0 # Counting Answers
    f=open('Questions.txt','a')
    f.write("                  QUESTION PAGE                 "+'\n'+"Question 1.----------------"+'\n')
    f.close()
    f=open('Options.txt','a')
    f.write('                  OPTIONS PAGE                   '+'\n'+"Options 1.------------")
    f.close()
    start_page=3
    i=3   #starting from page No.
    e=211  #ending to page No.
    while(i<=e):
        page=pdf.pages[i]
        text=page.extract_text()
        if "Maximum Marks:" in text or "TEST" in text: #Checking First Occurence of Questions
            j=i+4
            while(i<=j): #Looping through 5 more pages till we get page which contains answer
                if(i==j):
                    page2=pdf.pages[i]
                    text2=page2.extract_text()
                    if "Explanation:" in text2 or "Explanation" in text2: #If it contains answer than write on answer.txt
                        making_pdf(i)
                        ans_count=answers_extr('New.pdf',ans_count)
                        i+=1
                        break
                making_pdf(i)
                count=questions_extr('New.pdf',count)
                i+=1
        else: #If it contains answer than write on answer.txt
            making_pdf(i)
            ans_count=answers_extr('New.pdf',ans_count)
            i+=1
