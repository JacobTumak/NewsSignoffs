from django.forms import BooleanField
from signoffs.signoffs import RevokableSignoff, SignoffRenderer
from signoffs.models import Signet
from signoffs.forms import SignoffFormsManager, AbstractSignoffForm

class AgreeSignoffForm(AbstractSignoffForm):
    """ Require the user to signoff for the form to validate """
    signed_off = BooleanField(label='I agree', required=True)

publish_article_signoff = RevokableSignoff.register(id='publish_article_signoff',
                                                    signet=Signet,
                                                    label='I agree to the terms and conditions',
                                                    render=SignoffRenderer(form_context=dict(
                                                        submit_label='Publish Article',
                                                        help_text='<small>Publishing will make this article viewable to everyone.</small>',
                                                    )))
