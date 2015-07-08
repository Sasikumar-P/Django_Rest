from django.shortcuts import render
from .models import Contact
from simple_rest.forms import ModelForm
from django.http import HttpResponse
from django.core import serializers
from simple_rest.auth.decorators import signature_required
from simple_rest import Resource
from simple_rest.response import RESTfulResponse
from .models import Contact

def secret_key(request, *args, **kwargs):
    return 'test'


json_or_xml = RESTfulResponse({'application/xml': 'phonebook.xml'})
# Since RESTfulResponse inherits from collections.MutableMapping, we could
# have also done the following instead of passing a dict to the constructor
# json_or_xml = RESTfulResponse()
# json_or_xml['application/xml'] = 'phonebook.xml'


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields=['title', 'fname','lname','phone_number']

@signature_required(secret_key)
class Contacts(Resource):
    
    def get(self, request, contact_id=None, **kwargs):
        json_serializer = serializers.get_serializer('json')()
        if contact_id:
            contacts = json_serializer.serialize(Contact.objects.filter(pk=contact_id))
        else:
            contacts = json_serializer.serialize(Contact.objects.all())
        return HttpResponse(contacts, content_type='application/json', status=200)
    
    def post(self, request, *args, **kwargs):
        Contact.objects.create(
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            phone_number=request.POST.get('phone_number'))
        return HttpResponse(status=201)
    
    def delete(self, request, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        contact.delete()
        return HttpResponse(status=200)
