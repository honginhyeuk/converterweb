from django.shortcuts import render
from django.http import JsonResponse
import re

def index(request):
    return render(request, 'converter/index.html')

def convert(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        convert_to = request.POST.get('convert_to', '')

        if is_camel_case(text):
            original_format = 'camel'
        elif is_pascal_case(text):
            original_format = 'pascal'
        elif is_snake_case(text):
            original_format = 'snake'
        else:
            return JsonResponse({'error': 'Invalid input format'}, status=400)

        if convert_to == 'camel':
            converted_text = to_camel_case(text, original_format)
        elif convert_to == 'pascal':
            converted_text = to_pascal_case(text, original_format)
        elif convert_to == 'snake':
            converted_text = to_snake_case(text, original_format)
        else:
            return JsonResponse({'error': 'Invalid target format'}, status=400)

        return JsonResponse({'converted_text': converted_text})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s and s[0].islower()

def is_pascal_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s and s[0].isupper()

def is_snake_case(s):
    return "_" in s

def to_camel_case(text, original_format):
    if original_format == 'camel':
        return text
    elif original_format == 'pascal':
        return text[0].lower() + text[1:]
    elif original_format == 'snake':
        words = text.split('_')
        return words[0] + ''.join(word.capitalize() for word in words[1:])

def to_pascal_case(text, original_format):
    if original_format == 'pascal':
        return text
    elif original_format == 'camel':
        return text[0].upper() + text[1:]
    elif original_format == 'snake':
        return ''.join(word.capitalize() for word in text.split('_'))

def to_snake_case(text, original_format):
    if original_format == 'snake':
        return text
    elif original_format in ['camel', 'pascal']:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
