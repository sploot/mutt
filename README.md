mutt
====

muttContacts.py allows OSX users to utilize their OSX Address book with mutt 
email clients.

## Usage ##
Place muttContacts.py in your $PATH

To open a new email to a contact (interactive selection of contact):

    ./muttContacts.py query_term

To use muttContacts.py as your mutt external query command:

    set query_command = '~/bin/muttContacts.py -m %s'

# address-search.vim #

Install ftdetect plugin. Begin typing contact name followed by ^x^c and 
it will give a dropdown list of matching contact names.

Can be installed using pathogen.

