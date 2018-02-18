```
def patient_login(request):
    if request.method == "POST":
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "OK"})
        else:
            return JsonResponse({"status": "FAIL"})
    else:
        url = 'hospitalapp:patient_login'
        return render(request, 'hospitalapp/login.html', {'target_url': reverse(url)})
```