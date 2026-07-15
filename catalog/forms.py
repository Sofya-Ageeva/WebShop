from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена',
        }

    def __init__(self, *args, **kwargs):
        """Добавляем стили Bootstrap ко всем полям"""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = ''
                if 'form-control' not in field.widget.attrs['class']:
                    field.widget.attrs['class'] += ' form-control'

    def clean_name(self):
        """Валидация названия продукта на запрещённые слова"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for forbidden in FORBIDDEN_WORDS:
                if forbidden in name_lower:
                    raise ValidationError(
                        f'"{forbidden}" не может быть использовано для наименования. '
                        f'Пожалуйста, введите новое слово.'
                    )
        return name

    def clean_description(self):
        """Валидация описания продукта на запрещённые слова"""
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            for forbidden in FORBIDDEN_WORDS:
                if forbidden in desc_lower:
                    raise ValidationError(
                        f'"{forbidden}" не может быть использовано в описании. '
                        f'Пожалуйста, замените его.'
                    )
        return description

    def clean_price(self):
        """Валидация цены"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. '
                'Пожалуйста, введите корректную цену.'
            )
        return price

    def clean_image(self):
        """Валидация изображения"""
        image = self.cleaned_data.get('image')

        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError(
                    'Размер изображения не должен превышать 5 МБ. '
                    f'Текущий размер: {image.size / 1024 / 1024:.2f} МБ'
                )

            valid_extensions = ['image/jpeg', 'image/png']
            if image.content_type not in valid_extensions:
                raise ValidationError(
                    'Поддерживаются только форматы JPEG и PNG. '
                    f'Загружен: {image.content_type}'
                )

        return image
