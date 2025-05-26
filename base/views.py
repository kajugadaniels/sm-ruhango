from django.shortcuts import render, redirect

def change_language(request, lang_code):
    """
    Sets the session language. Defaults to French if no language is chosen.
    """
    # Save the selected language in session (e.g. 'en' or 'fr')
    request.session['lang'] = lang_code
    # Redirect back to the referring page, or home if not available.
    return redirect(request.META.get('HTTP_REFERER', '/'))

def home(request):
    return render(request, 'pages/index.html')