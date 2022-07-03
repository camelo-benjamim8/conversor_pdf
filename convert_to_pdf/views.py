from datetime import datetime
from msilib.schema import Directory
from tkinter import E
from django.http import FileResponse
from django.shortcuts import render
import datetime
from PIL import Image
import os
from string import ascii_letters, digits
import random
import datetime
from PyPDF2 import PdfFileReader, PdfFileMerger
from django.conf import settings
from convert_to_pdf.models import FileDelete
import pypandoc
from docx2pdf import convert
from django.core.files.storage import default_storage

# Create your views here.
def converter_pdf(request):
    current_year = datetime.datetime.now().year
    ##delete all files:
    all_files = FileDelete.objects.all()
    for i in all_files:
        try:
            filename_deletation_before_execution = i.filename
            ##deleting file from media root
            os.remove(os.path.join(settings.MEDIA_ROOT, filename_deletation_before_execution))
            ##deleting instruction for delete in database
            FileDelete.objects.delete(filename=filename_deletation_before_execution)
        except:
            pass
    if request.method == 'GET':
        context = {'year': str(current_year)}
    else:
         context = {'year': str(current_year)}
         files = request.FILES.getlist('upload')
         n_files = 0
         for i in files:
            n_files += 1
         ## try if is image
         try:
            if n_files == 1:
                case = 0
                img = Image.open(files[0])
                img = img.convert('RGB')
                pseudorandomic_strings = ascii_letters + digits
                pseudorandomic_random = ''
                for i in range(12):
                    pseudorandomic_random += random.choice(pseudorandomic_strings)
                pseudorandomic_random += str(datetime.date.today())
                directory_and_filename = 'media/{}.pdf'.format(pseudorandomic_random)
                img.save(directory_and_filename, format="PDF")
                request.session['pseudorandomic_pdf_name'] = pseudorandomic_random
            else:
                ## first_image
                case = 1
                array_imgs = []
                files_delete_after_operation = []
                for i in range(0,n_files):
                    img_file = Image.open(files[i])
                    img_file = img_file.convert('RGB')
                    pseudorandomic_strings = ascii_letters + digits
                    pseudorandomic_random = ''
                    for i in range(12):
                        pseudorandomic_random += random.choice(pseudorandomic_strings)
                    pseudorandomic_random += str(datetime.date.today())
                    directory_and_filename = 'media/{}.pdf'.format(pseudorandomic_random)
                    ##
                    directory_and_filename_delete = '{}.pdf'.format(pseudorandomic_random)
                    files_delete_after_operation.append(directory_and_filename_delete)
                    ##
                    array_imgs.append(directory_and_filename)
                    img_file.save(directory_and_filename, format="PDF")
                    files_dir = 'media/'
                    array2 = []
                    for f in os.listdir(files_dir):
                        if f in array_imgs:
                            array2.append(f)
                    
                    pdf_files = [f for f in os.listdir(files_dir) if array_imgs.__contains__('media/'+f)]
                    merger = PdfFileMerger()

                for filename in pdf_files:
                    merger.append(PdfFileReader(os.path.join(files_dir, filename), "rb"))
                pseudorandomic_string = ''
                for i in range(random.randint(20,35)):
                    pseudorandomic_string += (random.choice(ascii_letters + digits))
                merger.write(os.path.join(files_dir, "merged_{}.pdf".format(pseudorandomic_string)))
                request.session['pseudorandomic_pdf_name'] = pseudorandomic_string
               
                    ##
                    ##removing files reaming
                for i in files_delete_after_operation:
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(i)))
            if case == 0:
                response = os.path.join(settings.MEDIA_ROOT, str(request.session['pseudorandomic_pdf_name']) +'.pdf')
                filename_query = str(request.session['pseudorandomic_pdf_name']) +'.pdf'
                obj = FileDelete.objects.create(filename=filename_query)
                obj.save()
                return FileResponse(open(response,'rb'),content_type='application/pdf')
                
            else:
                response = os.path.join(settings.MEDIA_ROOT,'merged_' + str(request.session['pseudorandomic_pdf_name']) +'.pdf')
                filename_query = 'merged_' + str(request.session['pseudorandomic_pdf_name']) +'.pdf'
                obj = FileDelete.objects.create(filename=filename_query)
                obj.save()
                return FileResponse(open(response,'rb'),content_type='application/pdf')

         except:
         ## convert .doc .docx and anothers to pdf
            pass
   
    return render(request,'conversor_pdf/convert_pdf.html',context=context) 