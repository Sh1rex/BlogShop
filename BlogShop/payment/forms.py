from django import forms
import decimal

cash_top_up_choices = [(i, str(i)) for i in range(10, 101, 10)]

class TopUpBalanceForm(forms.Form):
    amount = forms.TypedChoiceField(choices=cash_top_up_choices,
                                      coerce=decimal.Decimal)