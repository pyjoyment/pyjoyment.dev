import Pyjoyment


class MyApp(Pyjoyment.object):
    # Runs once, when the application starts
    def startup(self):
        config = self.plugin('YAMLConfig')
        self.secrets = config['secrets']

        # The model, which every controller reaches with the helper notes()
        notes = {1: 'Buy milk'}
        self.helper('notes', lambda c: notes)

        r = self.routes
        r.get('/').to('notes#index')
        r.get('/notes/<id:num>', 'note').to('notes#show')
        r.post('/notes').to('notes#create')


new = MyApp.new
object = MyApp
