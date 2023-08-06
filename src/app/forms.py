from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . models import Ticket, TicketUpdate


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'', 'placeholder':'email'}))
    first_name = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class':'', 'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class':'', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class UpdateForm(forms.ModelForm):
    comments = forms.CharField(label="", widget=forms.Textarea(attrs={"type":"text","id":"large-input", "class":"block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-md focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-6 mt-24"}))

    class Meta:
        model = TicketUpdate
        exclude = ['ticket', 'updated_by', 'status']


class CreateTicketForm(forms.ModelForm):
    status_choices = [
    ("In Progress", "In Progress"),
    ("Completed", "Completed")]

    intake_choices = [('Web', 'Web'),
                  ('Email', 'Email'),
                  ('Phone','Phone')]


    account_number = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"text", "id":"first_name", "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    company = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"text", "id":"company", "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    product = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"text", "id":"product", "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    incident_category = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"text", "id":"incident_category", "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    incident_subcategory = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"text", "id":"incident_category", "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    intake_channel = forms.ChoiceField(label="", choices=intake_choices, widget=forms.Select(attrs={"type":"text", "id":"intake_channel", "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    status= forms.ChoiceField(label="",choices=status_choices, widget=forms.Select(attrs={"type":"text", "id":"intake_channel", "class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    customer_zip = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"text", "id":"small-input", "class":"bg-gray-50 border border-gray-300 text-gray-200 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    customer_state = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"text", "id":"small-input", "class":"bg-gray-50 border border-gray-300 text-gray-200 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    
    complaint_detail = forms.CharField(label="", widget=forms.Textarea(attrs={"type":"text", "id":"large-input", "class":"block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-md focus:ring-blue-500 focus:border-blue-500"}))
    

    class Meta:
        model = Ticket
        exclude = ['agent_id', 'complaint_date']

class CloseForm(forms.ModelForm):
    status_choices = [
        ("In Progress", "In Progress"),
        ("Completed", "Completed")
    ]

    status = forms.ChoiceField(
        label="",
        choices=status_choices,
        widget=forms.Select(attrs={
            "type": "text",
            "id": "intake_channel",
            "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        })
    )

    comments = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            "type": "text",
            "id": "large-input",
            "class": "block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-md focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-6"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If In Progress, pre-populate the text area with <<CLOSED>>, else <<REOPEN>>
        initial_comments = "<< CLOSED >>" if self.initial.get('status') == "In Progress" else "<< REOPEN >>"
        self.fields['comments'].initial = initial_comments

        # If status is completeted set the default status to In Progress because it means the agent will reopen the ticket. Else, completed
        initial_status = "Completed" if self.initial.get('status') == "In Progress" else "In Progress"
        self.initial['status'] = initial_status
        
        if self.initial.get('status') == "In Progress":
            self.fields['files'] = forms.FileField()
            self.fields['files'].required = False

    class Meta:
        model = TicketUpdate
        fields = ['status', 'comments']





