from django.utils.deprecation import MiddlewareMixin

SUPPORTED_LANGS = ("en", "fr", "rw", "sw")   # English, French, Kinyarwanda, Kiswahili

class LanguageSessionMiddleware(MiddlewareMixin):
    """
    Guarantees every request carries a valid `session['lang']`.
    Falls back to English if the user shows up without one or with nonsense.
    """
    def process_request(self, request):
        if request.session.get("lang") not in SUPPORTED_LANGS:
            request.session["lang"] = "en"
