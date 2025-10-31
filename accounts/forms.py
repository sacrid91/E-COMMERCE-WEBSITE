from django import forms
from .models import Account

#Borrow the fields defined in  account models
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name','phone_number','email','password']
        
    #Loops through the fields in {{forms}} to override custom & give them proper form css styling 
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder']='Enter Email Address'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'   
        
    #super() class modifies what the django gives as default to match specific needs    
    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords Don't Match!")