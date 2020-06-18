from django import forms
from django.forms import ModelForm
from secureX_site.models import RequestService,JobApplication,Order,DeliveryAdd
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RequestForm(ModelForm):
    class Meta:
        model=RequestService
        fields=['fname','lname','email','contactnumber','purpose','service']
        labels ={
            "fname" : 'FIRST NAME',
            "lname" : 'LAST NAME',
            "email" : 'E-Mail ID',
            "contactnumber" : 'CONTACT NUMBER',
            "purpose" : 'PURPOSE FOR REQUEST',
            "service" : 'SERVICES PROVIDED',
        }
        widgets={
            'purpose': forms.Textarea(attrs={'style': 'width:500px'}),
            'service': forms.Select(attrs={'style': 'width:500px'})
            }

MALE = 'M'
FEMALE = 'F'
OTHERS = 'OTH'

GENDER_CHOICES=[(MALE,'Male'),
               (FEMALE,'Female'),
               (OTHERS,'Others')]

DEBIT ='DEBIT'
CREDIT ='CREDIT'

CARD_CHOICES=[(DEBIT,'DEBIT CARD'),
              (CREDIT,'CREDIT CARD')]


class UserRegisterForm(UserCreationForm):
    
    #Age=forms.IntegerField()
    #Gender=forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.Select(attrs={'style': 'width:300px'}))
    
    


    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

        labels ={
            "first_name" : 'First Name',
            "last_name" : 'Last Name',
            "email" : 'E-Mail ID',
        }

class JobApplicationForm(ModelForm):
    gender=forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.Select(attrs={'style': 'width:300px'}))
    

    class Meta:  
      model = JobApplication
      fields = ['fname','lname','email','gender','dateofbirth','contactnumber','address','city','state','pincode','education','workexperience','jobpost','expectedsalary']

      labels={
        'fname' : 'First Name',
        'lname' : 'Last Name',
        'email' : 'E-mail',
        'gender': 'Gender',
        'dateofbirth' : 'Date Of Birth',
        'contactnumber' : 'Contact Number',
        'address' : 'Address',
        'city' : 'City',
        'state': 'State',
        'pincode':'Pincode',
        'education':'Education',
        'workexperience':'Work Experience (In Years)',
        'jobpost' : 'Job Applying For',
        'expectedsalary':'Expected Salary',
       }       

      widgets={
          'jobpost': forms.Select(attrs={'style': 'width:500px'})

       } 




class CheckoutForm(ModelForm):
    Card_Type=forms.ChoiceField(choices=CARD_CHOICES,widget=forms.Select(attrs={'style': 'width:300px'}),label='Card Type')
    Card_Number=forms.IntegerField(label='Card Number')
    Expiration_Date=forms.DateField(label='Expiration Date')
    Cvv=forms.IntegerField(label='CVV')

    class Meta:
     model=Order
     fields = ['Card_Type','Card_Number','Expiration_Date','Cvv']


class AddressForm(ModelForm):
    
    class Meta:
        model=DeliveryAdd
        fields = ['address','city','state','pincode']
        labels={
        'address' : 'Address',
        'city' : 'City',
        'state': 'State',
        'pincode':'Pincode',
       }       

      
        