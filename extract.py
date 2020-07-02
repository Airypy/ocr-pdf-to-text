import io
import re
from PIL import Image
import pytesseract
from wand.image import Image as wi

#Function to print questions and options of the pdf
def questions_extr(page_name,count):
    pdf = wi(filename =page_name, resolution = 500)
    pdfImage = pdf.convert('jpeg')

    imageBlobs=[]

    for img in pdfImage.sequence:
	       imgPage = wi(image = img)
	       imageBlobs.append(imgPage.make_blob('jpeg'))

    recognized_text = []
    pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract'

    q = open('Questions.txt','a')
    o = open('Options.txt','a')
    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang = 'eng')
        quest=re.compile('(?!.*(\(|Time|TARGET|TEST|DAY|Maximum))[0-9]?[a-zA-z]?.*[^SCORE]$')#Pattern to select answers
        non_waste=re.compile('(?!.*(Time|TARGET|TEST|DAY|Maximum|\d{2}\.)).*[^SCORE]$')
        options=re.compile('[(][a-c][)].*')#Pattern to select options
        lines=text.split('\n')
        length=len(lines)
        i=0
        while(i<length):

            if lines[i]=='' or len(lines[i])<=3 and lines[i][0].isdigit():
                i+=1
                continue
            if options.match(lines[i]):
                while(i<length and lines[i][1]!='d'):
                    if non_waste.match(lines[i]):
                        o.write('\n'+lines[i])
                    i+=1
                    while(i<length and lines[i]==''):
                        i+=1
                if len(lines[i])==3:
                    o.write('\n'+lines[i])
                    i+=1
                    while(i<length and lines[i]==''):
                        i+=1
                while(i<length and lines[i]!=''):
                    o.write('\n'+lines[i])
                    i+=1
                count+=1
                o.write('\n'+'Options {}.------------'.format(count))
                q.write('\n'+"Question {}.----------------".format(count)+'\n')
                continue
            if quest.match(lines[i]):
                text=re.sub('\d{2}\.|,','',lines[i])
                q.write(' '+text)
            i+=1
    q.close()
    o.close()
    return count

#Function to print answers of the pdf
def answers_extr(page_name,ans_count):
    pdf = wi(filename =page_name, resolution = 300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs=[]

    for img in pdfImage.sequence:
	       imgPage = wi(image = img)
	       imageBlobs.append(imgPage.make_blob('jpeg'))

    recognized_text = []
    pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract'

    a = open('Answers.txt','a')

    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang = 'eng')
        ans=re.compile('(?!.*(Time|TARGET|ANSWER|DAY)).*[^SCORE]$') #REMOVING TEXTS STARTING FROM WORDS INSIDE THE BRACKETS
        for line in text.split('\n'):
            if "Correct Option:" in line or "Correct Option" in line or "Correct Answer" in line:
                ans_count+=1
                a.write('\n'+"For Question {}.---------------".format(ans_count))
            if ans.match(line):
                text=re.sub('[\d{1}|\d{2}]\.|,','',line) #Replacing 1. or 12. with blank value
                a.write('\n' + text)

    a.close()
    return ans_count
