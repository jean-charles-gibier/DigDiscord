from django.db import models

# import pprint


# from django.db.models.signals import pre_init, post_init, class_prepared
# from django.dispatch import receiver


class Channel(models.Model):
    identifier = models.CharField(max_length=45, primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    topic = models.CharField(max_length=300, blank=True, null=True)
    first_id_message = models.CharField(
        max_length=45, blank=True, null=True, default="0"
    )
    last_id_message = models.CharField(
        max_length=45, blank=True, null=True, default="0"
    )
    server = models.ForeignKey(
        "Server", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Channel"
        ordering = ["name"]


class Link(models.Model):
    link_md5 = models.CharField(
        max_length=32, editable=False, primary_key=True
    )
    link_content = models.URLField(max_length=400, blank=True, null=True)
    links = models.ManyToManyField("Message", related_name="messages")

    def __init__(self, *args, **kwargs):
        """
        IMPORTANT : This hook is a scrappy workaround
        for keeping original id author/user among attributes
        despite it will not persisted in Model instance
        :param args:
        :param kwargs: contains embeded parameters
        """
        if "message_id" in kwargs:
            self.message_id = kwargs["message_id"]
            del kwargs["message_id"]
        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = "Link"
        ordering = ["link_content"]


class Message(models.Model):
    identifier = models.CharField(max_length=45, primary_key=True)
    references = models.ManyToManyField("self", related_name="references")
    content = models.TextField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    user = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True
    )
    channel = models.ForeignKey(
        "Channel", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __init__(self, *args, **kwargs):
        """
        IMPORTANT : This hook is a scrappy workaround
        for keeping original id author/user among attributes
        despite it will not persisted in Model instance
        :param args:
        :param kwargs: contains embeded parameters
        """
        if "references_id" in kwargs:
            self.references_id = kwargs["references_id"]
            del kwargs["references_id"]
        if "author_id" in kwargs:
            self.author_id = kwargs["author_id"]
            del kwargs["author_id"]
        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = "Message"
        ordering = ["date"]


class ModelReference(models.Model):
    reference = models.IntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "ModelReference"
        ordering = ["reference"]


class Server(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    identifier = models.CharField(max_length=45, primary_key=True)

    class Meta:
        verbose_name = "Server"
        ordering = ["name"]


class User(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    identifier = models.CharField(max_length=45, primary_key=True)

    class Meta:
        verbose_name = "User"
        ordering = ["name"]


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
