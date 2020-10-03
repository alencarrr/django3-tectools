from django.db import models
from django.contrib.auth.models import User

# Create your models here.

FIELD_TYPE_CHOOSE = [
    ('C','Caractere'),
    ('N','Numerico'),
    ('D','Data'),
    ('H','Hora'),
    ('DT', 'Data e Hora'),
    ('B', 'Boleano'),
    ('I', 'Imagem'),
    ('T', 'Texto'),
] 

FIELD_STATUS_PERIODO = [
    ('O', 'Aberto'),
    ('F', 'Fechado'),
]

FIELD_STATUS_PROJETO = [
    ('A', 'Ativo'),
    ('I', 'Inativo'),
    ('C', 'Cancelado'),
]


class Mapa(models.Model):
    nome = models.CharField('Nome do Mapa', max_length=30, unique=True)
    descricao = models.CharField('Descrição', max_length=50)
    sistema_origem = models.CharField('Sistema Origem', max_length=30)
    sistema_destino = models.CharField('Sistema Destino', max_length=30)
    
    class Meta:
        db_table = 'mapa'
        verbose_name_plural = 'mapas'
        indexes = [models.Index(fields=['nome'], name='mapa_name_idx')]
        
    def __str__(self):
        return '{}'.format(self.id)
    
class MapaCampos(models.Model):
    mapa = models.ForeignKey(Mapa, on_delete=models.CASCADE)
    tabela_o = models.CharField('Tabela Origem', max_length=30)
    campo_o = models.CharField('Campo Origem', max_length=40)
    campo_o_tipo = models.CharField('Tipo de dados', max_length=2, 
                                    choices=FIELD_TYPE_CHOOSE,
                                    default='C')
    campo_o_tam = models.CharField('Tamanho', max_length=10)
    campo_o_dec = models.CharField('Decimais',max_length=2,blank=True,null=True)
    campo_o_validos = models.TextField('Valores Válidos') 
    campo_o_formato = models.TextField('Formato') 
    regra_conversao = models.TextField('Regra de Conversão',blank=True,null=True)  
    tabela_d = models.CharField('Tabela Destino', max_length=30)
    campo_d = models.CharField('Campo Destino', max_length=40)
    campo_d_tipo = models.CharField('Tipo de dados', max_length=2, 
                                    choices=FIELD_TYPE_CHOOSE,
                                    default='C')
    campo_d_tam = models.CharField('Tamanho', max_length=10)
    campo_d_dec = models.CharField('Decimais',max_length=2,blank=True,null=True)
    campo_d_validos = models.TextField('Valores Válidos') 
    campo_d_formato = models.TextField('Formato')       
    
    class Meta:
        db_table = 'mapacampo'
        verbose_name_plural = 'mapcampos'
        indexes = [models.Index(fields=['tabela_o','campo_o'], name='mapa_campo_idx')]
        
    def __str__(self):
        return '{}'.format(self.id)    

class Cliente(models.Model):
    nome = models.CharField('Nome do Cliente', max_length=50, unique=True)

    class Meta:
        db_table = 'cliente'
        verbose_name_plural = 'clientes'
        indexes = [models.Index(fields=['nome'], name='cliente_nome_idx')]    

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome = models.CharField('Nome do Projeto', max_length=100)
    descricao = models.TextField('Descrição do Projeto')
    status = models.CharField('Status', max_length=1, choices=FIELD_STATUS_PROJETO, default='I')


    class Meta:
        db_table = 'projeto'
        verbose_name_plural = 'projetos'
        indexes = [models.Index(fields=['nome'], name='projeto_nome_idx')]   

    def __str__(self):
        return self.nome

class Periodo(models.Model):
    nome = models.CharField('Nome do Período', max_length=30, unique=True)
    hora_inicial = models.DateTimeField('Início')   
    hora_final = models.DateTimeField('Fim')
    status = models.CharField('Status', max_length=1, choices=FIELD_STATUS_PERIODO, default='F')

    def __str__(self):
        return self.nome    

class Meta:
    db_table = 'periodo'
    verbose_name_plural = 'periodos'
    indexes = [models.Index(fields=['nome'], name='periodo_nome_idx')]   

def __str__(self):
    return self.nome

class Fornecedor(models.Model):
    nome = models.CharField('Nome do Fornecedor', max_length=50, unique=True)

    class Meta:
        db_table = 'fornecedor'
        verbose_name_plural = 'fornecedores'
        indexes = [models.Index(fields=['nome'], name='fornecedor_nome_idx')]  

    def __str__(self):
        return self.nome

class Recurso(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.PROTECT)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    nome = models.CharField('Nome', max_length=50)
    trocar_senha = models.BooleanField('Trocar Senha?', max_length=1, default=True)

    class Meta:
        db_table = 'recurso'
        verbose_name_plural = 'recursos'
        indexes = [models.Index(fields=['nome'], name='recurso_nome_idx')]  

    def __str__(self):
        return self.nome

class Apontamento(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT)
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    recurso = models.ForeignKey(Recurso, on_delete=models.PROTECT)
    data_apontamento = models.DateField('Data do Apontamento')
    hora_inicial = models.TimeField('Hora inicial')
    hora_final = models.TimeField('Hora Final')
    descricao = models.CharField('Atividade', max_length=255)
    data_criacao = models.DateTimeField('Stamp de criação', auto_now_add=True)
    data_alteracao = models.DateTimeField('Stamp de alteração', auto_now=True)

    class Meta:
        db_table = 'apontamento'
        verbose_name_plural = 'apontamentos'   
        indexes = [models.Index(fields=['-data_apontamento','-hora_inicial'], name='apontamento_idx')]   

    def __str__(self):
        return '{} - {}'.format(self.data_apontamento,self.descricao)
