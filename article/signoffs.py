from django.forms import BooleanField
from signoffs.signoffs import SimpleSignoff, RevokableSignoff, SignoffRenderer
from signoffs.contrib.signets.signoffs import IrrevokableSignoff  # Add IrrevokableSignoff to signoffs.signoffs
from signoffs.core.signoffs import DefaultSignoffBusinessLogic
from signoffs.models import Signet


terms_signoff = IrrevokableSignoff.register(id='terms_signoff',
                                            logic=DefaultSignoffBusinessLogic(revoke_perm=False))  # Shouldn't have to override the default logic

marketing_signoff = RevokableSignoff.register(id='marketing_signoff')

publish_article_signoff = RevokableSignoff.register(id='publish_article_signoff',
                                                    signet=Signet,
                                                    sigil_label='Published by',
                                                    label='I agree to the terms and conditions',
                                                    render=SignoffRenderer(signet_template='signoffs/publish_signet.html',
                                                                           signoff_form_template='signoffs/simple_signoff_form.html',
                                                                           form_context=dict(submit_label='Publish Article',
                                                                                             help_text='Publishing will make this article viewable to everyone.',
                                                    )))


# from signoffs.forms import SignoffFormsManager, AbstractSignoffForm

# class AgreeSignoffForm(AbstractSignoffForm):
#     """ Require the user to signoff for the form to validate """
#     signed_off = BooleanField(label='I agree', required=True)
