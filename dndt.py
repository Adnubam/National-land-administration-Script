#----------------------------------------------------------------#
#Given a PDF, join each pair of consecutive pages into one page  #
#Script By Ronaldo Mabunda                                       #
#Feb - 2024, Python 3.11.4, PyPDF2 version=3.0.0                 #
#----------------------------------------------------------------#

import os
from PyPDF2 import PdfWriter, PdfReader, PageObject, Transformation

def header():
    print("#Given a PDF, join each pair of consecutive pages into one page \n#Script By Ronaldo Mabunda. \n#Feb - 2024, Python 3.11.4, PyPDF2 version=3.0.0 \n \n")

#Transform a text format like xxx-xxx-xxxxxxxxxx-xx-xxx.pdf to xxxxxxxxxx-xx-xxx.pdf
def block_name_formatted (nome):
    partes = nome.split("-")

    if len(partes) == 5:
        re = partes[2] + "-" + partes[3] + "-" + partes[4]
    else:
        re = nome
    return re

#Rename all the files in a directory, removing the DNDT system generated prefix
def apply_formatted_names(directory):
    
    for dirr in os.listdir(directory):
        if ".pdf" in dirr:
            os.rename(os.path.join(directory, dirr), os.path.join(directory, block_name_formatted (dirr)))

#Given a Directory, converts every block inside
def convert(directory):
    counter = 0     #For Converted blocks count
    non_converted = []      #To Store every non converted blocks
    path_to_save = os.path.join(directory, "PDFs Convertidos")      #Path where converted blocks are stored
    
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)

    #Looping through the given directory files
    for block in os.listdir(directory):
        if ".pdf" in block:
            try:
                with open(os.path.join(directory, block), "rb") as file:
                    pdf_reader = PdfReader(file)
                    pdf_writer = PdfWriter()

                    for index in range(0, int(len(pdf_reader.pages)/2),1):
                        page1 = pdf_reader.pages[2*index]
                        page2 = pdf_reader.pages[2*index + 1]
                        
                        #MERGE THE PAGES
                        
                        merger = PageObject.create_blank_page(width = 2* page1.mediabox.width, height = page1.mediabox.height)      #Creates an A3 landscape blank page

                        move_transformation = Transformation().translate(tx = page2.mediabox.width, ty = 0)       #Horizontal content stream move Transformation
                        size_transformation = Transformation().scale(sx = 0.70665, sy = 0.70665)     #Scales A3 height and width content stream to A4
                        
                        new_page = PageObject().create_blank_page(width = 842, height = 595) #Creates an A4 landscape blank page

                        #Add the Page2, move it to right, then add the Page1
                        merger.merge_page(page2, True)
                        merger.add_transformation(move_transformation)
                        merger.merge_page(page1, True)

                        merger.add_transformation(size_transformation)
                        new_page.merge_page(merger)

                        pdf_writer.add_page(new_page)

                        print(f'{block} Processing...{round(index/int(len(pdf_reader.pages)/2)*100, 3)}%') #Prints the progress

                #Saves the Converted Block
                with open(os.path.join(directory, "PDFs Convertidos", block_name_formatted (block)), "wb") as output:
                    pdf_writer.write(output)
                    pdf_writer.close()

                counter += 1
                print(f'{counter} Terminado!')
            
            except:
                non_converted.append(block)
    print("Blocos não convertidos: ", non_converted)

#EXECUTION STARTS HERE
header()

try:
    directory = input(f"{os.getlogin()}, Introduza o directorio: ")
    convert(directory)
    print("Execução Terminada!")
except:
    print("Directorio não válido ou falha na conclusao da tarefa!")
