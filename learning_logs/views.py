from django.shortcuts import render
#importando o banco de dados de models
from .models import Topic, Entry

from .forms import TopicForm, EntryForm
#esta puxando o TopicForm

from django.http import HttpResponseRedirect, Http404
#aqui esta puxando a função redirect(redirecionar)
#Porem precisa passar a url toda, Mas como não podemos colocar localhost etc
#ja que vai mudar essa url usaremos reverve

from django.urls import reverse
#a funçao para retornar

# O decorator é uma forma simples de alterar o comportamento de uma função sem ter a necessidade de modificar seu código.
# no caso do login_required ele ira restringir a pagina que deseja, 
# so deixando você passar caso esteja logado te redirecionando para pagina de login
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    """Página principal do learning_Log"""
    # return vai retorna para essa funçao
    #render vai renderizar tudo que esta sendo passado na função
    #request esta passando uma requisição
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Mostra todos os assuntos"""
    # estou pegando no banco de dados o topicos
    #e ordenando pela data
    #lembrando que data_added é um campo que existe na model topic
    #esta pegando todos os objetos que tem como owner o usuario
    topics = Topic.objects.filter(owner=request.user).order_by('data_added')
    #agora crio a variavel chamada context e vai passar os topics como dicionario para ela
    context = {"topics": topics}
    # nesse caso temos que passar o context para poder exibir os topics cadastrados
    # no html
    return render (request,'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """"Mostra um único assunto e todas as suas entradas."""
    #vai passar na url o id, depois isso vai vir para minha view
    #topic.objects.get (vai pesquisar no banco de dados se existe algum registro do banco de dados com esse id)
    #so vai da certo se o id existir
    topic = Topic.objects.get(id = topic_id)
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    # vai ordenar as entradas do mais recente
    entries = topic.entry_set.order_by('-date_added')
    #agora crio a variavel chamada context e vai passar os 
    # topic e os entries como dicionario para ela
    context = {'topic': topic, 'entries': entries}
    return render (request,'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """adiciona um novo assunto."""
    #caso no formulario eu envie algum metodo get
    #significa que não estou enviando dado nenhum para ele
    if request.method != 'POST':
        # nenhum dado submetido; cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos; processa os dados
        #ele ira redirecionar para o topico criado
        form = TopicForm(request.POST)
        #uma forma de fazer validação para o formulario
        if form.is_valid():
            
            #O parâmetro commit=False instrui o Django a criar a instância do modelo, 
            #mas sem gravá-la no banco imediatamente. Isso permite que façamos modificações antes de salvar.
            new_topic = form.save(commit=False)
            #aqui, o código define o campo owner do novo Topic para o usuário autenticado atualmente (request.user).
            #Isso garante que cada tópico criado seja vinculado ao usuário que o criou.
            new_topic.owner = request.user
            # aqui salva
            new_topic.save()
            


            # ele ira retorna para pagina com o name topic
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """acrescenta uma nova entrada para um assunto em particular."""
    #preciso fazer para saber a qual topico a entrada ira corresponder
    topic = Topic.objects.get(id=topic_id)
    
        # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    # se o metodo for diferente de POST
    if request.method != 'POST':
        # Se o método NÃO for POST, significa que o usuário apenas abriu a página, então:
        #criamos um formulário vazio para que ele possa preencher.
        form = EntryForm()
    else:
        # Dados de POST submetidos; processa os dados
        #Se o método for POST, significa que o usuário enviou dados.
        #Criamos um formulário com os dados enviados (request.POST).
        form = EntryForm(data=request.POST)
        if form.is_valid():
            #criar uma variavel pode ser qualquer nome porem nesse caso vamo chamar de new_entry
            #aqui ele vai criar um pre-salvamento e cria um objeto e não vai salvar no banco
            # de dados
            #agora o new_entry viro meio que um objeto com os dados do formularios
            #O Django cria um objeto, mas ainda não salva no banco.
            #Isso permite modificar o objeto antes de salvá-lo.
            new_entry = form.save(commit=False)
            #aqui vamos puxar o topic que pegamos do começo da função.
            #e vamos colocar em new_entry.topic
            #🔹 Por que isso é necessário?
            #No formulário, o campo topic pode não estar presente.
            #Precisamos definir manualmente qual topic essa entrada pertence.
            new_entry.topic = topic
            
            #aqui ele ira salvar
            #Aqui, associamos a nova entrada ao tópico correto.
            new_entry = form.save()
            #eu quero redirecionar para pagina topic e quero passar tambem como argumento o id
            return HttpResponseRedirect(reverse('topic',args=[topic_id]))
    #Se entrar no if que tem dentro do else, ele não chega nesse context
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)
        
@login_required        
def edit_entry(request, entry_id):
    """Edita uma entrada existente"""
    #estou indo la em entry e buscando os objetos salvos, 
    #estou fazendo um get pegando esses objetos pelo id
    #entry_id é pego passando nas urls 
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Requisição inicial; preenche previamente o formulário com a entrada atual
        # com isso no campo de formulario ele vai esta preenchido com o entry que escrevemos
        form = EntryForm(instance=entry)
    else:
        # Dados de Post submetidos; processa os dados
        # Depois de clicar para atualizar eu quero que o formulario
        # preenche o que tiver com o objeto entry, so que agora eu quero 
        # que atualize o que ta no entry com os dados relevantes do request.POST
        form = EntryForm(instance=entry, data=request.POST)
        # valida se os formularios estao ok
        if form.is_valid():
            form.save()
            #depois que eu salvar esses dados no banco de dados ele ira redirecionar para topic
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    # contexté o que podemos trabalhar dentro da pagina
    context = {'entry': entry, 'topic': topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)