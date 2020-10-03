from core.forms import ApontamentoForm
from core.models import Apontamento, Recurso
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class ApontamentoListView(LoginRequiredMixin,ListView):
    model = Apontamento
    # queryset = Mapa.objects.all()
    template_name = "core/apontamento_list.html"
    # context_object_name = 'mapas'
    # paginate_by = 10
    fields = '__all__'
    exclude = ('data_criacao','data_alteracao')
    ordering = ['-data_apontamento','-hora_inicial']


class ApontamentoCriarView(LoginRequiredMixin,CreateView):
    model = Apontamento
    form_class = ApontamentoForm
    #fields = '__all__'
    #exclude = ('data_criacao','data_alteracao')    
    # queryset = Mapa.objects.all()
    template_name = "core/apontamento_criar.html"      
    context_object_name = 'apontamento'
    success_url = reverse_lazy('core:lista-apontamento') 

    def get_initial(self):
        super(ApontamentoCriarView,self).get_initial()
        if not self.request.user.is_superuser:
            recurso = Recurso.objects.get(user_id=self.request.user.id)
            self.initial = {'recurso':recurso}

        return self.initial             

    def form_valid(self, form):

        if not self.request.user.is_superuser:
            c = {'form': form, }
            user = form.save(commit=False)
            # Cleaned(normalized) data
            recurso_form = form.cleaned_data['recurso']
            recurso_obj = Recurso.objects.get(user_id=self.request.user.id)
            recurso_form_str = recurso_form.__str__()
            recurso_valido_str = recurso_obj.__str__()

            if recurso_form_str != recurso_valido_str and not self.request.user.is_superuser:
                messages.error(self.request, 'Informe o recurso '+recurso_valido_str, extra_tags='alert alert-danger')
                return render(self.request, self.template_name, c)

            user.save()
 
        return super(ApontamentoCriarView, self).form_valid(form)

class ApontamentoAlterarView(LoginRequiredMixin,UpdateView):
    model = Apontamento
    form_class = ApontamentoForm
    #fields = '__all__'
    #exclude = ('data_criacao','data_alteracao')      
    # queryset = Mapa.objects.all()
    template_name = "core/apontamento_alterar.html"   
    success_url = reverse_lazy('core:lista-apontamento')    

    def form_valid(self, form):

        if not self.request.user.is_superuser:
            c = {'form': form, }
            user = form.save(commit=False)
            # Cleaned(normalized) data
            recurso_form = form.cleaned_data['recurso']
            recurso_obj = Recurso.objects.get(user_id=self.request.user.id)
            recurso_form_str = recurso_form.__str__()
            recurso_valido_str = recurso_obj.__str__()

            if recurso_form_str != recurso_valido_str and not self.request.user.is_superuser:
                messages.error(self.request, 'Informe o recurso '+recurso_valido_str, extra_tags='alert alert-danger')
                return render(self.request, self.template_name, c)

            user.save()
 
        return super(ApontamentoAlterarView, self).form_valid(form)    
   

class ApontamentoExcluirView(LoginRequiredMixin,DeleteView):
    model = Apontamento
    fields = '__all__'
    exclude = ('data_criacao','data_alteracao')     
    context_object_name = 'apontamento'     
    # queryset = Mapa.objects.all()
    template_name = "core/apontamento_excluir.html"      
        