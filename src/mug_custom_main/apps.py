import logging

from django.apps import AppConfig
#from django_mailman3.models import Address
from django.db.models.signals import post_save
from django.dispatch import receiver

#from django.db.models import get_app, get_models

#from allauth.account.models import EmailAddress
from allauth.account.signals import email_added
from allauth.account.signals import email_changed
from allauth.account.signals import user_signed_up
from allauth.account.signals import user_logged_in

from djangosaml2.signals import pre_user_save
from djangosaml2.signals import post_authenticated

from django.utils import translation

logger = logging.getLogger(__name__)

class MugCustomMainConfig(AppConfig):
    name = 'mug_custom_main'

    def ready(self):
        logger.info(' --- mug_custom_main Ready!!!')

        from django.core.signals import request_finished
        #request_finished.connect(self.request_callback)



    #@staticmethod
    #def request_callback(sender, **kwargs):
        #logger.info(' --- Request callback')
        #logger.info(" ---    sender %s" % (sender))
        #logger.info(" ---    kwargs %s" % str(kwargs))


    @receiver(email_added)
    def email_added_called(request, user, email_address, **kwargs):
        logger.info(' --- email_added: ' + email_address.__str__())


    @receiver(email_changed)
    def email_changed_called(request, user, email_address, **kwargs):
        logger.info(' --- email_changed: ' + email_address.__str__())


    @receiver(user_signed_up)
    def user_signed_up_called(request, user, **kwargs):
        logger.info(' --- user_signed_up: ' + user.__str__())
        from django.contrib.auth.models import User
        from allauth.account.models import EmailAddress

        emails = EmailAddress.objects.filter(user=user)
        for email in emails:
            logger.info('      --- email: ' + email.__str__())


    @receiver(user_logged_in)
    def user_logged_in_called(request, user, **kwargs):
        logger.info(' --- user_logged_in: ' + user.__str__())
        from django.contrib.auth.models import User
        from allauth.account.models import EmailAddress

        logger.info(' --- user_logged_in - user.username: ' + user.username)
        logger.info(' --- user_logged_in - user.email: ' + user.email)

        emailsForUser = EmailAddress.objects.filter(user=user)
        logger.info('      --- email for user: ' + emailsForUser.__str__())
        logger.info('      --- email for user: ' + str(len(emailsForUser)))

        isPrimary = False
        if len(emailsForUser) <= 0:
            isPrimary = True

        currentEMail = None
        try:
            currentEMail = EmailAddress.objects.get(email=user.email)
            logger.info('      --- E-Mail already exists...')
        except EmailAddress.DoesNotExist:
            currentEMail = None
            logger.info('      --- E-Mail not exists! - create new one')

        if currentEMail is None:
            newEMail = EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=isPrimary)
            logger.info('      --- new EMail: ' + newEMail.__str__())
            newEMail.save()


    @receiver(pre_user_save) #saml2
    def pre_user_save_called(attributes, user_modified, **kwargs):
        logger.info(' --- pre_user_save_called - attributes: ' + attributes.__str__())
        logger.info(' --- pre_user_save_called - user_modified: ' + user_modified.__str__())


    @receiver(post_authenticated) #saml2
    def post_authenticated_called(session_info, **kwargs):
        logger.info(' --- post_authenticated_called: ' + session_info.__str__())
        logger.info(' --- post_authenticated_called user: ' + session_info.ava.uid)
        logger.info(' --- post_authenticated_called user: ' + session_info.ava.mail)

