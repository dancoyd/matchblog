from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "subtitle", "category", "content", "image", "is_published"]
        labels = {
            "title": "Título",
            "subtitle": "Subtítulo",
            "category": "Categoría",
            "content": "Contenido",
            "image": "Imagen",
            "is_published": "Publicado",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Consejos para mejorar tu saque"
            }),
            "subtitle": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Breve resumen de la publicación"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Escribí el contenido de la publicación..."
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "checkbox-input"
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")

        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")

        if len(content) < 20:
            raise forms.ValidationError("El contenido debe tener al menos 20 caracteres.")

        return content