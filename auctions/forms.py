from django import forms
from django.forms import ModelForm
from .models import Bid

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        labels = {
            "amount": "Your Bid Amount",
        }
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
        }






# class BidForm(forms.ModelForm):
#     """Form for placing a bid."""
#     class Meta:
#         model = Bid
#         fields = ["amount"]
#         widgets = {
#             "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
#         }

#     def clean_amount(self):
#         amount = self.cleaned_data.get("amount")
#         if amount is None:
#             raise forms.ValidationError("Enter a bid amount.")
#         if amount <= 0:
#             raise forms.ValidationError("Bid must be greater than zero.")
#         return amount







# class CommentForm(forms.ModelForm):
#     """Form to add a comment to a listing."""
#     class Meta:
#         model = Comment
#         fields = ["content"]
#         widgets = {
#             "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Leave a comment"}),
#         }


