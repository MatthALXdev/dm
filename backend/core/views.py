from django.http import JsonResponse, HttpResponse  

def health(request):
    return JsonResponse({"status": "ok"})


def hello(request):
    return HttpResponse("Hello World 🚀")