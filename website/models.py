from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)
    email = models.EmailField(_("email"),blank=True, null=True, max_length=254)
    subject = models.CharField(_("subject"), max_length=100)  
    message = models.TextField(_("text user")) 
    created_at = models.DateTimeField(_("create at"), auto_now_add=True)  

    def __str__(self):
        return f'{self.subject} from  {self.user}'
   