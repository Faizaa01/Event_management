from django import forms
from events.models import Event, Category
from django.contrib.auth.models import User, Group


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_class = "border-2 border-gray-100 w-full m-2 font-semibold rounded-sm shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.TextInput):
                widget.attrs.update({
                    'class': self.default_class,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({
                    'class': f"{self.default_class} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 4
                })
            elif isinstance(widget, forms.SelectDateWidget):
                widget.attrs.update({
                    'class': "border-2 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs.update({
                    'class': "space-y-2"
                })
            elif isinstance(widget, forms.Select):
                widget.attrs.update({
                    'class': self.default_class
                })
            else:
                widget.attrs.update({
                    'class': self.default_class,
                    'placeholder': f"Enter {field.label.lower()}"
                })


class Eventform(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants', 'asset']
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea,
            'category': forms.Select,
            'participants': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            participant_group = Group.objects.get(name='Participant')
            self.fields['participants'].queryset = User.objects.filter(groups=participant_group)
        except Group.DoesNotExist:
            self.fields['participants'].queryset = User.objects.none()



class Categoryform(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {
            'description': forms.Textarea,
        }

