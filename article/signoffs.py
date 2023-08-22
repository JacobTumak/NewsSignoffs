from signoffs.signoffs import SimpleSignoff, RevokableSignoff, IrrevokableSignoff, SignoffRenderer, SignoffUrlsManager
from signoffs.core.signing_order import SigningOrder

from article.models.signets import RevokedNewsletterSignet, PublicationApprovalSignet, PublicationRequestSignet, \
    ArticleSignet

terms_signoff = IrrevokableSignoff.register(id='terms_signoff')

newsletter_signoff = RevokableSignoff.register(id='newsletter_signoff',
                                               revokeModel=RevokedNewsletterSignet,
                                               urls=SignoffUrlsManager(revoke_url_name='revoke_newsletter'))

# publish_article_signoff = SimpleSignoff.register(id='publish_article_signoff',
#                                                     sigil_label='Published by',
#                                                     label='I agree to the terms and conditions',)
                                                    # render=SignoffRenderer(signet_template='signoffs/publish_signet.html',
                                                    #                        signoff_form_template='signoffs/custom_publish_signoff.html',
                                                    #                        form_context=dict(submit_label='Publish Article',
                                                    #                                          help_text='Publishing will make this article viewable to everyone.')))


publication_request_signoff = RevokableSignoff.register(id='publication_request_signoff',
                                                        signetModel=ArticleSignet,
                                                            label='Submit for Publication',
                                                                render=SignoffRenderer(
                                                                    form_context=dict(
                                                                       help_text=
                                                                       'Publication Request')))

publication_approval_signoff = IrrevokableSignoff.register(id='publication_approval_signoff',
                                                           signetModel=ArticleSignet,
                                                               label='Publish Article',
                                                                    render=SignoffRenderer(
                                                                        form_context=dict(
                                                                            help_text=
                                                                            'Publication Approval')))


# class ArticlePublicationSignoffs:
#
#     publication_request_signoff = RevokableSignoff.register(id='publication_request_signoff',
#                                                             signetModel=PublicationSignet,
#                                                             label='Submit for Publication',
#                                                                 render=SignoffRenderer(
#                                                                     form_context=dict(
#                                                                        help_text=
#                                                                        'Publication Request')))
#
#     publication_approval_signoff = IrrevokableSignoff.register(id='publication_approval_signoff',
#                                                                signetModel=PublicationSignet,
#                                                                label='Publish Article',
#                                                                     render=SignoffRenderer(
#                                                                         form_context=dict(
#                                                                             help_text=
#                                                                             'Publication Approval')))
    #
    # publication_signing_order = SigningOrder(
    #     publication_request_signoff,
    #     publication_approval_signoff)

