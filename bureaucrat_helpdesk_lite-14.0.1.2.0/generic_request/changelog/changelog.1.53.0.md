- Automatically move created stage to the end of list of stages.
  This is required to avoid case when new stage become first one and
  thus it become starting stage for requests.
- Better support for handling mails received from unknown contacts.
  In this case `email_from` will be saved on request
- Save `email_cc` on request (if first email contains `cc`)
- Automatically subscribe partners mentioned in ``CC`` header of incoming mail
- Implement partner suggestions for mailing for requests.
  Odoo will automatically suggest to subscribe partner and / or author of request
  if that is not following request yet
