from signoffs.signoffs import SimpleSignoff, RevokableSignoff, IrrevokableSignoff, SignoffRenderer, SignoffUrlsManager

from article.models.signets import RevokedNewsletterSignet


terms_signoff = IrrevokableSignoff.register(id='terms_signoff')

newsletter_signoff = RevokableSignoff.register(id='newsletter_signoff',
                                               revokeModel=RevokedNewsletterSignet,
                                               urls=SignoffUrlsManager(revoke_url_name='revoke_newsletter'))

publish_article_signoff = SimpleSignoff.register(id='publish_article_signoff',
                                                    sigil_label='Published by',
                                                    label='I agree to the terms and conditions',
                                                    render=SignoffRenderer(signet_template='signoffs/publish_signet.html',
                                                                           signoff_form_template='signoffs/simple_signoff_form.html',
                                                                           form_context=dict(submit_label='Publish Article',
                                                                                             help_text='Publishing will make this article viewable to everyone.')))
