from django.db import models
# from django.db.models.signals import pre_init, post_init, class_prepared
# from django.dispatch import receiver
# import pprint

class Channel(models.Model):
    identifier = models.CharField(max_length=45, blank=True, unique=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    topic = models.CharField(max_length=300, blank=True, null=True)
    server = models.ForeignKey('Server', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Channel"
        ordering = ['name']


class Link(models.Model):
    link_content = models.URLField(max_length=300, blank=True, null=True)
    links = models.ManyToManyField('Message', related_name='messages')

    class Meta:
        verbose_name = "Link"
        ordering = ['link_content']


class Message(models.Model):
    mentions = models.ManyToManyField('self', related_name='mentions')
    content = models.TextField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey('Channel', on_delete=models.SET_NULL, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        """
        IMPORTANT : This hook is a scrappy workaround
        for keeping original id author/user among attributes
        despite it will not persisted in Model instance
        :param args:
        :param kwargs: contains embeded parameters
        """
        if 'author_id' in kwargs:
             self.author_id = kwargs['author_id']
             del kwargs['author_id']
        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = "Message"
        ordering = ['date']


class ModelReference(models.Model):
    reference = models.IntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "ModelReference"
        ordering = ['reference']


class Server(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    identifiant = models.CharField(max_length=45, blank=True, null=True)


    class Meta:
        verbose_name = "Server"
        ordering = ['name']


class User(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    identifiant = models.CharField(max_length=45, unique=True, blank=True, null=True)
    channels = models.ManyToManyField(Channel, related_name='channels')

    class Meta:
        verbose_name = "User"
        ordering = ['name']

# Debug
# @receiver(pre_init, sender=Message)
# def hear_signal(sender, *args, **kwargs):
#
#     print("==> Pre")
#     pprint.pprint(kwargs)
#
#     return
#
# @receiver(post_init, sender=Message)
# def hear_signal2(sender, instance, *args, **kwargs):
#
#     print("==> Post")
#     pprint.pprint(instance)
#
#     return
#
# @receiver(class_prepared, sender=Message)
# def hear_signal3(sender, *args, **kwargs):
#
#     print("==> class_prepared")
#     pprint.pprint(sender)
#
#     return
#
