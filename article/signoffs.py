from signoffs.signoffs import (
    SimpleSignoff,
    RevokableSignoff,
    IrrevokableSignoff,
    SignoffRenderer,
    SignoffUrlsManager,
)
from signoffs.core.signing_order import SigningOrder

from article.models.signets import RevokedNewsletterSignet, ArticleSignet

terms_signoff = IrrevokableSignoff.register(id="terms_signoff")

newsletter_signoff = RevokableSignoff.register(
    id="newsletter_signoff",
    revokeModel=RevokedNewsletterSignet,
    urls=SignoffUrlsManager(revoke_url_name="revoke_newsletter"),
)

publication_request_signoff = RevokableSignoff.register(
    id="publication_request_signoff",
    signetModel=ArticleSignet,
    label="Submit for Publication",
    urls=SignoffUrlsManager(
        revoke_url_name="revoke_publication_request",
    ), # TODO: toggle between this line and the one below to produce error with save_url_name
    # save_url_name='request_publication',),
    render=SignoffRenderer(
        form_context=dict(
            help_text="Publication Request",
            submit_label="Save",
        )
    ),
)

publication_approval_signoff = RevokableSignoff.register(
    id="publication_approval_signoff",
    signetModel=ArticleSignet,
    label="Publish Article",
    urls=SignoffUrlsManager(
        revoke_url_name="revoke_publication_approval",
    ),
    render=SignoffRenderer(
        form_context=dict(
            help_text="Publication Approval",
        )
    ),
)

publication_signing_order = SigningOrder(
    publication_request_signoff, publication_approval_signoff
)
