import Pyjo.YAML

from Pyjo.File import curfile
from Pyjoyment.Lite import *

import platform


EXAMPLES = curfile().dirname().child('examples')

# The function gets the requests with the host of its Function URL, so the canonical URL names the host of the site
HOME = 'https://pyjoyment.dev'

# The files of the examples on GitHub, of main, which the site is deployed from
SOURCE = 'https://github.com/pyjoyment/pyjoyment.dev/blob/main/site/examples'

# The badges of the footer, of shields.io, which renders them for each view: their link, their image and its text
SHIELDS = 'https://img.shields.io'
BADGES = [
    (
        'https://github.com/pyjoyment/Pyjoyment',
        f'{SHIELDS}/github/stars/pyjoyment/Pyjoyment?style=for-the-badge&logo=github&label=stars',
        'Stars of Pyjoyment on GitHub',
    ),
    (
        'https://pyjoyment.readthedocs.io/',
        f'{SHIELDS}/badge/read-docs-8ca1af?style=for-the-badge&logo=readthedocs&logoColor=white',
        'The documentation of Pyjoyment on Read the Docs',
    ),
    (
        'https://github.com/pyjoyment/Pyjoyment/releases/latest',
        f'{SHIELDS}/github/v/release/pyjoyment/Pyjoyment?sort=semver&display_name=tag&style=for-the-badge&label=github&logo=github',
        'The latest release of Pyjoyment on GitHub',
    ),
    (
        'https://pypi.org/project/Pyjoyment/',
        f'{SHIELDS}/pypi/v/Pyjoyment?style=for-the-badge&logo=pypi&logoColor=white&label=pypi',
        'The version of Pyjoyment on PyPI',
    ),
    (
        'https://github.com/pyjoyment/pyjoyment.dev',
        f'{SHIELDS}/badge/source-pyjoyment.dev-02a7a0?style=for-the-badge&logo=github',
        'The source of this site on GitHub',
    ),
]

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
    'tf': 'hcl',
    'toml': 'ini',
    'yaml': 'yaml',
    'yml': 'yaml',
}

catalog = Pyjo.YAML.load(EXAMPLES.child('catalog.yaml').slurp())
FEATURES = {feature['id']: feature for feature in catalog['features']}
ROLES = {role['id']: role for role in catalog['roles']}


def tabs(directory, files: list[dict]) -> list[dict]:
    source = f'{SOURCE}/{directory.to_rel(EXAMPLES).to_str()}'
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
            'source': f'{source}/{file["name"]}',
        }
        for file in named
    ]


# The scenarios by their feature and role, with the files of their directories
SCENARIOS: dict[tuple[str, str], list[dict]] = {}
for feature, by_role in catalog['scenarios'].items():
    for role, scenarios in by_role.items():
        if feature not in FEATURES or role not in ROLES:
            raise ValueError(f'Unknown feature or role {feature}/{role} in examples/catalog.yaml')
        for scenario in scenarios:
            scenario['tabs'] = tabs(EXAMPLES.child(feature, role, scenario['id']), scenario.get('files') or [])
        SCENARIOS[feature, role] = scenarios


def path(*parts: str | None) -> str:
    return '/' + '/'.join(part for part in parts if part)


def page(c, feature: str | None = None, role: str | None = None, scenario: str | None = None) -> None:
    scenarios = SCENARIOS.get((feature, role), []) if feature and role else []
    current = next((item for item in scenarios if item['id'] == scenario), None)
    if scenario and current is None:
        return c.reply.not_found()

    # A button selects its feature or role, in place of the one selected, and the one selected unselects it
    features = [
        {
            **item,
            'selected': item['id'] == feature,
            'href': c.url_for(path(None if item['id'] == feature else item['id'], role)),
            'empty': bool(role) and item['id'] != feature and (item['id'], role) not in SCENARIOS,
        }
        for item in FEATURES.values()
    ]
    roles = [
        {
            **item,
            'selected': item['id'] == role,
            'href': c.url_for(path(feature, None if item['id'] == role else item['id'])),
            'empty': bool(feature) and item['id'] != role and (feature, item['id']) not in SCENARIOS,
        }
        for item in ROLES.values()
    ]
    choices = [
        {**item, 'selected': item is current, 'href': c.url_for(path(feature, role, item['id']))} for item in scenarios
    ]

    heading = ' '.join(
        title for title in (FEATURES.get(feature, {}).get('title'), ROLES.get(role, {}).get('title')) if title
    )
    if current:
        heading = f'{heading}: {current["title"]}'
    c.title(f'{heading} | Pyjoyment' if heading else 'Pyjoyment')

    c.render(
        'index',
        feature=feature,
        role=role,
        features=features,
        roles=roles,
        choices=choices,
        current=current,
        canonical=HOME + path(feature, role, scenario),
    )
    # After the rendering, so that the page of an exception of a template is not cached
    cache(c)


@helper('badges')
def badges(c):
    return BADGES


# The pages and the files of public/ change only with a deployment, which invalidates the distribution, so CloudFront
# keeps them for a week, and the browsers, which the invalidation does not reach, for an hour; in another mode than
# production nothing is kept, so that a change is seen at once, and a response of an action without Cache-Control, as
# /hello, is not cached in any mode
CACHE_CONTROL = 'public, max-age=3600, s-maxage=604800'


def cache(c):
    c.res.headers.cache_control = CACHE_CONTROL if c.app.mode == 'production' else 'no-cache'


@hook('after_static')
def cache_static(c):
    cache(c)


@get('/')
def index(c):
    page(c)


# /hello and /hello/Sara, rendered by the function on each request
@get('/hello/:name', {'name': 'World'}, 'hello')
def hello(c):
    c.render(json={'hello': c.param('name'), 'python': platform.python_version()})


# /http or /server, a feature or a role alone
@get('/:selection', selection=[*FEATURES, *ROLES])
def selection(c):
    value = c.param('selection')
    if value in FEATURES:
        page(c, feature=value)
    else:
        page(c, role=value)


@get('/:feature/:role', feature=list(FEATURES), role=list(ROLES))
def pair(c):
    page(c, c.param('feature'), c.param('role'))


@get('/:feature/:role/:scenario', feature=list(FEATURES), role=list(ROLES))
def scenario(c):
    page(c, c.param('feature'), c.param('role'), c.param('scenario'))


# The handler "app.handler" of the event function, and the command of the arguments otherwise
handler = app.start()
