from django import forms
from item.models import Item
CLASS_VAR = 'px-4 py-2 rounded-xl w-full border border-black'

class EditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'quantity', 'item_image1', 'item_image2', 'item_image3', 'is_sold']
        
        
        widgets = {
            
            "category": forms.Select(attrs={
                "id":"category",
                "class":CLASS_VAR
            }),
            
            
            "name": forms.TextInput(attrs={
                "placeholder":"name of item",
                "id":"name",
                "class":CLASS_VAR
            }),
            
            "description": forms.Textarea(attrs={
                "placeholder":"description...",
                "id":"description",
                "class": f"{CLASS_VAR} h-12 resize-none align-top"
            }),
            
            "price": forms.NumberInput(attrs={
                "placeholder":"$ price",
                "id":"price",
                "class":CLASS_VAR
            }),
            
            "quantity": forms.NumberInput(attrs={
                "placeholder":"Quantity",
                "id":"quantity",
                "class":CLASS_VAR
            }),
            
            "item_image1": forms.ClearableFileInput(attrs={
                "id":"image1",
                "class":CLASS_VAR
            }),
            
            "item_image2": forms.ClearableFileInput(attrs={
                "id":"image2",
                "class":CLASS_VAR
            }),
            
            "item_image3": forms.ClearableFileInput(attrs={
                "id":"image3",
                "class":CLASS_VAR
            }),
        }

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'quantity', 'item_image1', 'item_image2', 'item_image3']
        
        widgets = {
            
            "category": forms.Select(attrs={
                "id":"category",
                "class":CLASS_VAR
            }),
            
            
            "name": forms.TextInput(attrs={
                "placeholder":"name of item",
                "id":"name",
                "class":CLASS_VAR
            }),
            
            "description": forms.Textarea(attrs={
                "placeholder":"description...",
                "id":"description",
                "class": f"{CLASS_VAR} h-12 resize-none align-top"
            }),
            
            "price": forms.NumberInput(attrs={
                "placeholder":"$ price",
                "id":"price",
                "class":CLASS_VAR
            }),
            
            "quantity": forms.NumberInput(attrs={
                "placeholder":"Quantity",
                "id":"quantity",
                "class":CLASS_VAR
            }),
            
            "item_image1": forms.ClearableFileInput(attrs={
                "id":"image1",
                "class":CLASS_VAR
            }),
            "item_image2": forms.ClearableFileInput(attrs={
                "id":"image2",
                "class":CLASS_VAR
            }),
            "item_image3": forms.ClearableFileInput(attrs={
                "id":"image3",
                "class":CLASS_VAR
            }),
        }
