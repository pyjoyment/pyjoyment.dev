import Pyjo.YAML

from Pyjo.File import curfile
from Pyjoyment.Lite import *

import platform


EXAMPLES = curfile().dirname().child('examples')

# The function gets the requests with the host of its Function URL, so the canonical URL names the host of the site
HOME = 'https://pyjoyment.dev'

# The classes of highlight.js, by the name or the extension of a file, unless the catalog names the language of the file,
# and plaintext otherwise; the layout loads the languages that the common build of highlight.js does not have
LANGUAGES = {
    'Dockerfile': 'dockerfile',
    'css': 'css',
    'ep': 'xml',
    'html': 'xml',
    'ini': 'ini',
    'js': 'javascript',
    'json': 'json',
    'ps1': 'powershell',
    'py': 'python',
    'sh': 'bash',
    'toml': 'ini',
    'yaml': 'yaml',
    'yml': 'yaml',
}

catalog = Pyjo.YAML.load(EXAMPLES.child('catalog.yaml').slurp())
FEATURES = {feature['id']: feature for feature in catalog['features']}
ROLES = {role['id']: role for role in catalog['roles']}

# A role, or a pair of roles in the order of their selection, as "tester+server", the URL of the page keeps it, so the
# third role replaces the first one
SELECTIONS = [*ROLES, *(f'{a}+{b}' for a in ROLES for b in ROLES if a != b)]


def roles_key(roles: list[str]) -> str:
    return '+'.join(sorted(roles, key=list(ROLES).index))


def tabs(directory, files: list[dict]) -> list[dict]:
    if not directory.is_dir:
        return []
    paths = {
        path.to_rel(directory).to_str(): path
        for path in directory.list_tree()
        if '__pycache__' not in path.to_str() and path.extname != 'pyc'
    }
    named = [{'title': file['name'], **file} for file in files]
    listed = {file['name'] for file in named}
    named += [{'name': name, 'title': name} for name in sorted(paths) if name not in listed]
    return [
        {
            'title': file['title'],
            'language': file.get('language')
            or LANGUAGES.get(paths[file['name']].basename())
            or LANGUAGES.get(paths[file['name']].extname, 'plaintext'),
            'code': paths[file['name']].slurp('UTF-8'),
        }
        for file in named
    ]


# The scenarios by their feature and the key of their roles, with the files of their directories
SCENARIOS: dict[tuple[str, str], list[dict]] = {}
for feature, by_roles in catalog['scenarios'].items():
    for key, scenarios in by_roles.items():
        if feature not in FEATURES or key != roles_key(key.split('+')) or key not in SELECTIONS:
            raise ValueError(f'Unknown or unordered scenarios {feature}/{key} in examples/catalog.yaml')
        for scenario in scenarios:
            scenario['tabs'] = tabs(EXAMPLES.child(feature, key, scenario['id']), scenario.get('files') or [])
        SCENARIOS[feature, key] = scenarios


def path(feature: str | None = None, roles: list[str] | None = None, scenario: str | None = None) -> str:
    return '/' + '/'.join(part for part in (feature, '+'.join(roles or []), scenario) if part)


def page(c, feature: str | None = None, roles: list[str] | None = None, scenario: str | None = None) -> None:
    roles = roles or []
    key = roles_key(roles)
    scenarios = SCENARIOS.get((feature, key), []) if feature and roles else []
    current = next((item for item in scenarios if item['id'] == scenario), None)
    if scenario and current is None:
        return c.reply.not_found()

    features = [
        {
            **item,
            'selected': item['id'] == feature,
            'href': c.url_for(path(None if item['id'] == feature else item['id'], roles)),
            'empty': bool(roles) and item['id'] != feature and (item['id'], key) not in SCENARIOS,
        }
        for item in FEATURES.values()
    ]
    buttons = []
    for item in ROLES.values():
        selected = item['id'] in roles
        after = [role for role in roles if role != item['id']] if selected else [*roles, item['id']][-2:]
        buttons.append(
            {
                **item,
                'selected': selected,
                'href': c.url_for(path(feature, after)),
                'empty': bool(feature) and not selected and (feature, roles_key(after)) not in SCENARIOS,
            }
        )
    choices = [
        {**item, 'selected': item is current, 'href': c.url_for(path(feature, roles, item['id']))} for item in scenarios
    ]

    heading = ' + '.join(ROLES[role]['title'] for role in sorted(roles, key=list(ROLES).index))
    if feature:
        heading = f'{FEATURES[feature]["title"]} {heading}'.strip()
    if current:
        heading = f'{heading}: {current["title"]}'
    c.title(f'{heading} | Pyjoyment' if heading else 'Pyjoyment')

    c.render(
        'index',
        feature=feature,
        selected_roles=roles,
        features=features,
        buttons=buttons,
        choices=choices,
        current=current,
        canonical=HOME + path(feature, sorted(roles, key=list(ROLES).index), scenario),
    )
    # The pages change only with a deployment, which invalidates the distribution, as the files of public/; after the
    # rendering, so that the page of an exception of a template is not cached
    c.res.headers.cache_control = 'public, max-age=3600'


# The files of public/ change only with a deployment, so CloudFront and the browsers keep them for an hour, where a
# response of an action has no Cache-Control and is not cached
@hook('after_static')
def cache_static(c):
    c.res.headers.cache_control = 'public, max-age=3600'


@get('/')
def index(c):
    page(c)


# /hello and /hello/Sara, rendered by the function on each request
@get('/hello/:name', {'name': 'World'}, 'hello')
def hello(c):
    c.render(json={'hello': c.param('name'), 'python': platform.python_version()})


# /http or /server+client, a feature or roles alone
@get('/:selection', selection=[*FEATURES, *SELECTIONS])
def selection(c):
    value = c.param('selection')
    if value in FEATURES:
        page(c, feature=value)
    else:
        page(c, roles=value.split('+'))


@get('/:feature/:roles', feature=list(FEATURES), roles=SELECTIONS)
def pair(c):
    page(c, c.param('feature'), c.param('roles').split('+'))


@get('/:feature/:roles/:scenario', feature=list(FEATURES), roles=SELECTIONS)
def scenario(c):
    page(c, c.param('feature'), c.param('roles').split('+'), c.param('scenario'))


# The handler "app.handler" of the event function, and the command of the arguments otherwise
handler = app.start()
