def importe_total_cesta(request):
    total = 0
    #if request.user.is_authenticated:
    for key, value in request.session["cesta"].items():
        total += float(value["precio"])
    return {"importe_total_cesta":total}