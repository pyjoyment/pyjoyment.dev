# The plugin of the skills of Pyjoyment, from the marketplace of its repository, in Claude Code
/plugin install pyjoyment --marketplace pyjoyment/Pyjoyment

# Or from the shell, as the extensions of the editors have no /plugin
claude plugin install pyjoyment --marketplace pyjoyment/Pyjoyment

# Its skills, as pyjoyment:lite, pyjoyment:tests or pyjoyment:migration, and what they cost of the context
claude plugin details pyjoyment

# A skill comes by its description, as for "Port app.py from Flask to Pyjoyment", or by its name
/pyjoyment:tests Write the tests of the routes of app.py

# The plugin has no version, so an update takes the skills of the last commit
claude plugin marketplace update pyjoyment
claude plugin update pyjoyment@pyjoyment
