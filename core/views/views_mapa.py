from core.models import Mapa, MapaCampos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class MapaListView(LoginRequiredMixin,ListView):
    model = Mapa
    # queryset = Mapa.objects.all()
    template_name = "core/mapa_list.html"
    context_object_name = 'mapas'
    paginate_by = 10
    fields = ['nome', 'descricao','sistema_origem', 'sistema_destino']

class MapaDatailView(LoginRequiredMixin,DetailView):
    model = Mapa
    context_object_name = 'mapa'
    #query_set = Mapa.objects.all()
    template_name = "core/mapa_detail.html"
    # success_url = reverse_lazy('core:lista-mapa')



class MapaCreate(LoginRequiredMixin,CreateView):
    fields = '__all__'
    context_object_name = 'mapa'
    template_name = "core/mapa_novo.html"
    model = Mapa    
    success_url = reverse_lazy('core:lista-mapa')     

class MapaUpdate(LoginRequiredMixin,UpdateView):
    model = Mapa
    fields = '__all__'
    template_name = "core/mapa_atualiza.html"
    success_url = reverse_lazy('core:lista-mapa') 


class MapaDelete(LoginRequiredMixin,DeleteView):
    model = Mapa   
    context_object_name = 'mapa'
    template_name = "core/mapa_exclui.html" 
    success_url = reverse_lazy('core:lista-mapa')     


""" Seção de tratamento dos campos do mapa de carga  """

class CampoListView(LoginRequiredMixin,ListView):

    model = MapaCampos

    template_name = "core/campo_list.html"
    context_object_name = 'campos'
    paginate_by = 10
    fields = ['id','mapa', 'tabela_o','campo_o', 'campo_o_tipo','tabela_d','campo_d', 'campo_d_tipo']
    exclude = ('id')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(CampoListView, self).get_context_data(**kwargs)
        # Add the current category to the context.
        context['idmapa'] = self.kwargs['idmapa']
        return context    

    def get_queryset(self):

        queryset = super().get_queryset()

        try:
            new_queryset = MapaCampos.objects.filter(mapa_id=self.kwargs['idmapa']).order_by('mapa','tabela_o')
            if new_queryset:
                queryset = new_queryset
        except KeyError:
            pass
        print('retorno {}'.format(queryset))

        return queryset       



class CampoDatailView(LoginRequiredMixin,DetailView):
    model = MapaCampos
    context_object_name = 'campo'
    #query_set = Mapa.objects.all()
    template_name = "core/campo_detail.html"
    # success_url = reverse_lazy('core:lista-mapa')
    def get_queryset(self):
        query_set = MapaCampos.objects.filter(mapa=self.kwargs['idmapa'],id=self.kwargs['pk'])
        return query_set    

    def get_success_url(self):
        print('kwargs {}'.format(self.kwargs))
        return reverse_lazy('core:lista-campos', kwargs={'idmapa': self.kwargs['idmapa']})  

class CampoCreate(LoginRequiredMixin,CreateView):
    fields = '__all__'
    context_object_name = 'campo'
    template_name = "core/campo_novo.html"
    model = MapaCampos 

    def get_initial(self):
        super(CampoCreate,self).get_initial()
        mapa = Mapa.objects.get(pk=self.kwargs['idmapa'])
        self.initial = {'mapa':mapa.id}
        return self.initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(CampoCreate, self).get_context_data(**kwargs)
        # Add the current category to the context.
        context['idmapa'] = self.kwargs['idmapa']
        return context 

    def get_success_url(self):
        return reverse_lazy('core:lista-campos', kwargs={'idmapa': self.kwargs['idmapa']})  


class CampoUpdate(LoginRequiredMixin,UpdateView):
    model = MapaCampos
    fields = '__all__'
    template_name = "core/campo_atualiza.html"

    def get_initial(self):
        result = super().get_initial()
        result['mapa']=self.kwargs['idmapa']
        return result

    def get_queryset(self):
        #objeto = Mapa.objects.filter(id=self.kwargs['idmapa'])
        query_set = MapaCampos.objects.filter(id=self.kwargs['pk'])
        return query_set

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                print('erro de campo {} {}'.format(error, field.name))

        return super().form_invalid(form)

    def get_success_url(self):
        print('kwargs {}'.format(self.kwargs))
        return reverse_lazy('core:lista-campos', kwargs={'idmapa': self.kwargs['idmapa']})    

class CampoDelete(LoginRequiredMixin,DeleteView):
    model = MapaCampos   
    context_object_name = 'campo'
    template_name = "core/campo_exclui.html" 

    def get_queryset(self):
        query_set = MapaCampos.objects.filter(id=self.kwargs['pk'])
        return query_set

    def get_success_url(self):
        return reverse_lazy('core:lista-campos', kwargs={'idmapa': self.kwargs['idmapa']})
