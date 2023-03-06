from django.shortcuts import redirect, render
from contacto.forms import FormularioContacto
from django.core.mail import EmailMessage

def contacto(requests):
    formulario = FormularioContacto()

    if requests.method == "POST":
        formulario = FormularioContacto(data=requests.POST)
        if formulario.is_valid():
            nombre = requests.POST.get("nombre")
            email = requests.POST.get("email")
            contenido = requests.POST.get("contenido")

            print("NOMBRE: "+nombre)
            print("EMAIL: "+email)

            #email = EmailMessage(
            #   "Mensaje desde App Django",
            #   "El usuario con nombre: {} con mail: {}, escribe:\n\n{}"
            #       .format(nombre, email, contenido),
            #   "", # Se puede ignorar
            #   ["prueba@gmail.com"],
            #   reply_to=[email]
            #)
            #try:
            #   email.send()
            #   return redirect("/contacto/?valido")
            #except:
            #   return redirect("/contacto/?novalido")

            

    return render(
        requests, 
        "contacto/contacto.html",
        {"formulario":formulario}
    )
