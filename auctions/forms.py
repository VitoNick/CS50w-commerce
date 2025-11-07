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
    
    def __init__(self, *args, listing=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = listing

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if self.listing.closed:
            raise forms.ValidationError("This auction is closed.")
        if amount is None:
            raise forms.ValidationError("Enter a bid amount.")
        if amount <= 0:
            raise forms.ValidationError("Bid must be greater than zero.")
        if self.listing.bid_count() == 0:
            if amount < self.listing.starting_bid:
                raise forms.ValidationError(f"First bid must be at least ${self.listing.starting_bid}.")
        else:
            if amount <= self.listing.current_bid():
                raise forms.ValidationError("Bid must be greater than current bid.")

        return amount





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


