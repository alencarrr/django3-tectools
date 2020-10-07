from core.forms import LoginForm
from core.models import Recurso
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import request
from django.shortcuts import redirect, render


def home(request):

    form = LoginForm()

    if not request.user.is_authenticated:
        return redirect('login/', form=form)

    user = User.objects.get(username=request.user.username)

    

    if not user.is_superuser:
        # Só executa se o usuario logado não for administrador do django.
        recurso = Recurso.objects.get(user_id=user.id)

        print('recurso = {}  trocar_senha = {}'.format(recurso.user_id,recurso.trocar_senha))

        if recurso.trocar_senha == True:
            return render(request,'core/trocar_senha.html')

    return render(request,'core/index.html')


def trocasenha(request):

    if request.method == "POST":

        senha1 = request.POST.get("InputPassword1",'')
        senha2 = request.POST.get("InputPassword2",'')

        if not senha1:
            messages.add_message(request,messages.ERROR,"Precisa informar a senha!. Tente novamente.", extra_tags=settings.MSG_TAGS[messages.ERROR])
            return redirect('/novasenha/')

        elif not senha2:
            messages.add_message(request,messages.ERROR,"Precisa Confirmar a senha!. Tente novamente.", extra_tags=settings.MSG_TAGS[messages.ERROR])
            #return redirect(request.META.get('HTTP_REFERER'))
            return redirect('/novasenha/')

        elif senha1 != senha2:
            messages.add_message(request,messages.ERROR,"As senhas são diferentes!. Tente novamente.", extra_tags=settings.MSG_TAGS[messages.ERROR])
            return redirect('/novasenha/')
        else:
            try:
                validate_password(senha1,user=request.user)
            except ValidationError as errorlist:
                for erro in errorlist:
                    messages.add_message(request,messages.ERROR,erro, extra_tags=settings.MSG_TAGS[messages.ERROR])
                return redirect('/novasenha/')   

        user = User.objects.get(id=request.user.id)
        user.set_password(senha1)
        user.save()
        recurso = Recurso.objects.get(user_id=user.id)
        recurso.trocar_senha = False
        recurso.save()
        messages.add_message(request,messages.SUCCESS,"Senha alterada com sucesso!. Acesse novamente.", extra_tags=settings.MSG_TAGS[messages.SUCCESS])

        return redirect('/logout/')

    return render(request,'core/trocar_senha.html')

def meulogin(request):

    username = request.POST.get('username','admin')
    password = request.POST.get('password','')
    user = authenticate(request, username=username, password=password)

    if request.method == "POST":

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            #messages.error(request, "Usuário ou Senha inválido!") 
            messages.add_message(request,messages.ERROR,"Usuário ou Senha inválido!", extra_tags=settings.MSG_TAGS[messages.ERROR])

    form = LoginForm()

    return render(request,'core/login.html', {'form':form})


def meupassword_reset(request):
    pass


def meulogout(request):
    if request.user.is_authenticated:
        logout(request)

    form = LoginForm()

    return render(request,'core/login.html', {'form':form})

def handler404(request, *args, **kwargs):
    context = {}
    response = render(request, "core/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request, *args, **kwargs):
    context = {}
    response = render(request, "core/500.html", context=context)
    response.status_code = 500
    return response      
