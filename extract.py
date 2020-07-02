import io
import re
from PIL import Image
import pytesseract
from wand.image import Image as wi

#Function to print questions and options of the pdf
def questions_extr(page_name,count):
    pdf = wi(filename =page_name, resolution = 300)
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
        quest=re.compile('(?!.*(\(|Time|TARGET|TEST|DAY|crJSCORE|ceEJSCORE|Maximum))[0-9]?[a-zA-z]?.*')#Pattern to select answers
        options=re.compile('[(][a-c][)].*')#Pattern to select options
        for line in text.split('\n'):
            if line=='' or len(line)<=3 and line[0].isdigit():
                continue
            if options.match(line):
                o.write('\n'+line)
            if(line!='' and line[0]=='(' and line[1]=='d'):
                count+=1
                q.write('\n'+"Question {}.----------------".format(count)+'\n')
                o.write('\n'+line+'\n'+'Options {}.------------'.format(count))
            if quest.match(line):
                text=re.sub('\d{2}\.|,','',line)
                q.write(' '+text)
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
        ans=re.compile('(?!.*(Time|TARGET|ANSWER|crSCORE|DAY|crJSCORE|ceEJSCORE)).*') #REMOVING TEXTS STARTING FROM WORDS INSIDE THE BRACKETS
        for line in text.split('\n'):
            if "Explanation:" in line or "Explanation" in line or "Correct Option" in line:
                ans_count+=1
                a.write('\n'+"For Question {}.---------------".format(ans_count))
            if ans.match(line):
                text=re.sub('[\d{1}|\d{2}]\.|,','',line) #Replacing 1. or 12. with blank value
                a.write('\n' + text)

    a.close()
    return ans_count
