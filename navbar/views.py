from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
import csv
from django.shortcuts import get_object_or_404, redirect, render
from collections import defaultdict
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes ,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from navigationbar.settings import EMAIL_HOST_USER
from django.contrib.auth.tokens import default_token_generator
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import EmailBase
def MainPageView(request, message=None):
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            emails = []

            # Check if the file is a CSV file
            if csv_file.name.endswith('.csv'):
                decoded_file = csv_file.read().decode('utf-8')
                csv_reader = csv.reader(decoded_file.splitlines())
                for row in csv_reader:
                    for item in row:
                        if  EmailBase.objects.filter(email=item).exists():
                            continue
                        else:
                            email=EmailBase.objects.create(email=item)
                        email.save()
                msg = ["success_message", "Send Email Page"]
                emails=EmailBase.objects.all()
                return render(request, 'navbar/sendemails.html', {'emails': emails})
            else:
                msg = ["error_message", "Invalid file format. Please upload a CSV file."]
                return MainPageView(request, msg)
        except UnicodeDecodeError:
            msg = ["error_message", "UnicodeDecodeError: Please upload a valid CSV file"]
            return MainPageView(request, msg)
    else:
        context = {'segment': 'index'}
        if message is not None:
            context[message[0]] = message[1]
        html_template = loader.get_template('navbar/mainpage.html')
        return HttpResponse(html_template.render(context, request))

def sendemails(request, message=None):
    if request.method == 'POST':
        emails = EmailBase.objects.all()
        print ("*************************************")
        print (emails)
        current_site = get_current_site(request)
        title = 'Qbit Labs - Qbit'  
        message = render_to_string('navbar/email_template.html', {
            'domain': current_site.domain,
        })
        email = EmailMultiAlternatives(title, strip_tags(message), EMAIL_HOST_USER, bcc=emails, cc=['hrtech@qbitlabs.co.in'])
        email.attach_alternative(message, 'text/html')
        email.send()
        
        EmailBase.objects.all().delete()
        
        emailsave=EmailBase.objects.create(email="shahaasrar1@gmail.com")
        emailsave.save()
        return HttpResponse('Emails have been sent to the recipients.')
    else:
        emails = EmailBase.objects.all()
        context = {'segment': 'index', 'emails': emails}
        if message is not None:
            context[message[0]] = message[1]
        return render(request, 'navbar/sendemails.html', context)

class ContactPageView(TemplateView):
    template_name = 'navbar/contactus.html'

class DocumentationPageView(TemplateView):
    template_name = 'navbar/documentation.html'