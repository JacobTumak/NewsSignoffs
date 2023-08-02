from django.forms import BooleanField
from signoffs.signoffs import SimpleSignoff, RevokableSignoff, SignoffRenderer, BaseSignoff
from signoffs.contrib.signets.signoffs import IrrevokableSignoff # TODO: Why isn't this importable from the main signoffs file?
from signoffs.models import Signet
from signoffs.forms import AbstractSignoffForm


class AgreeSignoffForm(AbstractSignoffForm):
    """ Require the user to signoff for the form to validate """
    signed_off = BooleanField(label='I agree', required=True)


tos_signoff = IrrevokableSignoff.register(id='tos_signoff')

publish_article_signoff = RevokableSignoff.register(id='publish_article_signoff',
                                                    signet=Signet,
                                                    sigil_label='Published by',
                                                    label='I agree to the terms and conditions',
                                                    render=SignoffRenderer(signet_template='signoffs/publish_signet.html',
                                                                           signoff_form_template='signoffs/simple_signoff_form.html',
                                                                           form_context=dict(submit_label='Publish Article',
                                                                                             help_text='Publishing will make this article viewable to everyone.',
                                                    )))
