'''
Copyright 2016 Sean Beck
MIT license

A simple script that provides a function to send an email via Mailgun.
This requires obtaining an API key from Mailgun.
You must also supply the function with the domain name associated with your account.
Mailgun will generate one for you, so just use that if you do not have your own domain.
'''
import requests


def mailgun_notify(**kwargs):
    """
    :param kwargs: Pass in a dictionary like so containing your args - mailgun_notify(**d)
    :return: None

    param api_key: Your Mailgun API key
    param domain: The domain associated with your Mailgun account
    param from: A string representing the sending email address. This usually
                 looks something like "Mailgun <mailgun@mydomain.com>"
    param to: Can be a single string or a list of strings representing email addresses
               of your intended recipients
    param subject: A string to be used as your email's subject
    param text: A string representing the body of your email in text.

    Those are basic parameters to the Mailgun API. This function requires you specify all
    of these parameters except for "text". All other possible parameters that can be sent
    via the API can be found here: https://documentation.mailgun.com/api-sending.html#sending.
    If you want an HTML email instead of a text-based email, use the "html" parameter instead.
    """
    params = ['api_key', 'domain', 'from', 'to', 'subject']
    if any(param not in kwargs for param in params):
        raise Exception('Please specify all params: {}'.format(params))
    data = {param: kwargs[param] for param in kwargs if param not in ['api_key', 'domain']}
    req = requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(kwargs['domain']),
        auth=('api', kwargs['api_key']),
        data=data
    )
    if req.status_code != 200:
        raise Exception('Request was not successful. Status code: {}'.format(req.status_code))
