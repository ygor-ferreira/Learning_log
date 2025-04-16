from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    """ Um assunto sobre o qual o usuário está aprendendo """
    text = models.CharField(max_length=200)
    data_added = models.DateTimeField(auto_now_add=True)
    # owner é o usuario
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        """"devolve uma representação em string do modelo."""
        return self.text
    
class Entry(models.Model):
    """Algo especifico aprendido sobre um assunto
    ele ira vincular esse banco de dados entry com o banco de dados entry
    o topic daqui ira vincular com o banco de dados Topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    """ essa verbose_name_plural serve para caso o django use o plural de entry 
    não ficar entrys e sim entries"""
    class Meta:
        verbose_name_plural = "entries"
        
    def __str__(self):
        "devolve uma representação em string do modelo"
        """so ira retorna os 50 primeiras caracteres
        e ira mostrar que tem mais coisa com '...' """
        return self.text[:50] + '...'