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



class MailmanConfig(AppConfig):
    name = 'medunigraz.mailman'

    def ready(self):
        logger.info(' --- medunigraz.mailman Ready!!!')

        from django.core.signals import request_finished
        #request_finished.connect(self.request_callback)

    #@staticmethod
    #def request_callback(sender, **kwargs):
        #logger.info(' --- Request callback')
        #logger.info(" ---    sender %s" % (sender))
        #logger.info(" ---    kwargs %s" % str(kwargs))

    @staticmethod
    def known_user_login(user, email):
        logger.info(' --- user_logged_in common - username: ' + user)
        logger.info(' --- user_logged_in common - email: ' + email)

        from django.contrib.auth.models import User
        from allauth.account.models import EmailAddress

        currentUser = None
        try:
            currentUser = User.objects.get(username=user)
            logger.info('      --- User exists - Test EMail...')
        except User.DoesNotExist:
            currentUser = None
            logger.info('      --- User not exists! - exit...')

        if currentUser is not None:
            emailsForUser = EmailAddress.objects.filter(user=currentUser)
            logger.info('      --- email for user: ' + emailsForUser.__str__())
            logger.info('      --- email for user: ' + str(len(emailsForUser)))

            isPrimary = False
            if len(emailsForUser) <= 0:
                isPrimary = True

            currentEMail = None
            try:
                currentEMail = EmailAddress.objects.get(email=currentUser.email)
                logger.info('      --- E-Mail already exists...')
            except EmailAddress.DoesNotExist:
                currentEMail = None
                logger.info('      --- E-Mail not exists! - create new one')

            if currentEMail is None:
                newEMail = EmailAddress.objects.create(user=currentUser, email=currentUser.email, verified=True, primary=isPrimary)
                logger.info('      --- new EMail: ' + newEMail.__str__())
                newEMail.save()


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

        #from django.contrib.auth.models import User
        #from allauth.account.models import EmailAddress
        #emailsForUser = EmailAddress.objects.filter(user=user)
        #logger.info('      --- email for user: ' + emailsForUser.__str__())
        #logger.info('      --- email for user: ' + str(len(emailsForUser)))

        logger.info(' --- user_logged_in - user.username: ' + user.username)
        logger.info(' --- user_logged_in - user.email: ' + user.email)
        MailmanConfig.known_user_login(user = user.username, email = user.email)

    @receiver(pre_user_save) #saml2
    def pre_user_save_called(attributes, user_modified, **kwargs):
        logger.info(' --- pre_user_save_called - attributes: ' + attributes.__str__())
        logger.info(' --- pre_user_save_called - user_modified: ' + user_modified.__str__())

    @receiver(post_authenticated) #saml2
    def post_authenticated_called(session_info, **kwargs):
        logger.info(' --- post_authenticated_called: ' + session_info.__str__())
        avaobj = session_info["ava"]
        logger.info(' --- post_authenticated_called mail: ' + avaobj.__str__())
        logger.info(' --- post_authenticated_called user: ' + avaobj["uid"][0])
        logger.info(' --- post_authenticated_called user: ' + avaobj["mail"][0])
        MailmanConfig.known_user_login(user = avaobj["uid"][0], email = avaobj["mail"][0])
