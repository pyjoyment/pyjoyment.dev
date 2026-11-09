import Pyjoyment.Controller


class MyApp_Controller_Notes(Pyjoyment.Controller.object):
    # Renders templates/notes/index.html.ep, of the controller and the action
    def index(self):
        self.render(notes=self.notes())

    def show(self):
        id = int(self.param('id'))
        if (note := self.notes().get(id)) is None:
            return self.reply.not_found()
        self.render(note=note)

    def create(self):
        notes = self.notes()
        id = max(notes, default=0) + 1
        notes[id] = self.req.json('/text')
        self.res.headers.location = self.url_for('note', id=id).to_abs()
        self.render(json={'id': id}, status=201)


object = MyApp_Controller_Notes
