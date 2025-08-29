from django import forms
import decimal
from .models import BuyProductTransaction

cash_top_up_choices = [(i, str(i)) for i in range(10, 101, 10)]

class TopUpBalanceForm(forms.Form):
    amount = forms.TypedChoiceField(choices=cash_top_up_choices,
                                      coerce=decimal.Decimal)
    
class BuyProductTransactionForm(forms.ModelForm):
    class Meta:
        model = BuyProductTransaction
        fields = '__all__'
        exclude = ['user', 'product', 'created', 'updated', 'paid', 'stripe_id']

    def __init__(self, *args, quantity_max=0, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(i, str(i)) for i in range(1, quantity_max + 1)] 
        self.fields['quantity'] = forms.TypedChoiceField(choices=choices,
                                            coerce=int)