import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFrame, \
    QDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QWidget, QMainWindow
from functools import reduce
from pydux import create_store


class Container(QWidget):
    def __init__(self, store, label, help_text):
        super(Container, self).__init__(None)
        self._store = store
        self._store.subscribe(self.sub)
        self.label = QLabel('<b>{}</b>'.format(label))
        self.help_text = QLabel(help_text, wordWrap=True, alignment=Qt.AlignTop)
        self.layout = self.arrange(self.label, self.help_text)

    def arrange(self, label, text):
        layout = QVBoxLayout()
        layout.addWidget(label, alignment=Qt.AlignTop)
        if text:
            layout.addWidget(text)
        else:
            layout.addStretch(1)
        layout.addLayout(self.get_sublayout())
        return layout

    def get_sublayout(self, *args, **kwargs):
        raise NotImplemented

    def sub(self, *args, **kwargs):
        print('Container subscirber called with', args, kwargs)
        print('store::::', self._store.get_state()[0]['value'])
        self.widget.setText(self._store.get_state()[0]['value'])
        # self._store.dispatch({'type': 'UPDATE_WIDGET', 'id': 0, 'value': 'poop'})



class TextField(Container):

    def get_sublayout(self, *args, **kwargs):
        self.widget = QLineEdit(*args, **kwargs)
        self.widget.textChanged.connect(self.foo)
        layout = QHBoxLayout()
        layout.addWidget(self.widget)
        return layout

    def foo(self, value, **kwargs):
        print(hash(self), value, kwargs)
        self._store.dispatch({
            'type': 'UPDATE_WIDGET',
            'value': value,
            'id': 0
        })





class Form(QMainWindow):

    def __init__(self, store, parent=None):
        super(Form, self).__init__(parent)

        self.t = TextField(store, 'Schloop', 'Schadoop')
        # self.t2 = TextField(store, 'Schloop', 'Schadoop')
        self.setCentralWidget(page(self.t))
        self.setWindowTitle('FOOBAR')
        # self.setContentsMargins(0,0,0,0)
        # self.setStyleSheet('padding: 0; margin: 0')


def page(t):
    layout = QVBoxLayout()
    layout.setContentsMargins(0,0,0,0)
    layout.addWidget(header(), alignment=Qt.AlignTop, stretch=0)
    layout.setSpacing(0)

    layout.addWidget(hline(), alignment=Qt.AlignTop, stretch=0)
    layout.addWidget(body(t), stretch=1)
    layout.addWidget(hline(), alignment=Qt.AlignTop, stretch=0)
    layout.addWidget(footer())

    qwidget = QFrame()
    qwidget.setLayout(layout)
    qwidget.setFrameShape(QFrame.NoFrame)
    return qwidget




def header():
    layout = QHBoxLayout()
    layout.addLayout(header_text('Settings', 'Enter blah'), stretch=1)
    # layout.setContentsMargins(0,0,0,0)
    qwidget = QFrame()
    qwidget.setLayout(layout)
    qwidget.setMaximumHeight(80)
    qwidget.setMinimumWidth(130)
    qwidget.setFrameShape(QFrame.NoFrame)
    qwidget.setLineWidth(0)
    qwidget.setStyleSheet('background: white; margin: 0; padding: 0')
    return qwidget


def header_text(label, text):
    layout = QVBoxLayout()
    layout.addStretch(1)
    layout.addWidget(QLabel('<b>Settings</b>'))
    layout.addWidget(QLabel('Enter your settings, bruh'))
    layout.addStretch(1)
    return layout


def body(t):
    layout = QVBoxLayout()
    layout.addWidget(QLabel('<h2>Required Arguments</h2>'))
    layout.addLayout(t.layout)
    layout.addWidget(QLabel('<h2>Optional Arguments</h2>'))

    for i in range(8):
        layout.addWidget(QLabel('Howdy!'))

    w = QFrame()
    w.setFrameShape(QFrame.NoFrame)
    w.setLineWidth(0)
    w.setLayout(layout)
    w.setContentsMargins(0,0,0,0)
    scrollem = QScrollArea()
    # scrollem.setBackgroundRole(QPalette.Dark)
    scrollem.setWidget(w)
    return scrollem


def footer():
    btn_layout = QHBoxLayout()
    btn_layout.addStretch(1)
    btn1 = QPushButton('Cancel')
    btn2 = QPushButton('Start')
    btn_layout.addWidget(btn1)
    btn_layout.addWidget(btn2)

    qwidget = QWidget()
    qwidget.setLayout(btn_layout)
    qwidget.setMinimumHeight(60)
    qwidget.setMaximumHeight(60)
    # qwidget.setStyleSheet('background: green')
    return qwidget


def hline():
    frame = QFrame()
    frame.setFrameShape(QFrame.HLine)
    frame.setFrameShadow(QFrame.Sunken)
    frame.setLineWidth(2)
    return frame

class TestForm(QDialog):

    def __init__(self):
        super(TestForm, self).__init__(parent=None)
        layout = QVBoxLayout()
        self.widget = QLineEdit()
        layout.addWidget(self.widget)
        self.setLayout(layout)
        self.widget.textChanged.connect(self.foo)

    def foo(self, *args, **kwargs):
        print('foo', args, kwargs)


def assign(*args):
    return reduce(lambda acc, x: acc.update(x) or acc, args, {})


def todo_reducer(state, action):
    if not state:
        return {'todos': []}
    if action['type'] == 'ADD_TODO':
        return assign(state, {
            'foo': 'bar'
        })
    else:
        return state


initial_state = {
    "language_dir": "/Users/ckiehl/Documents/Gooey/gooey/languages",
    "auto_start": False,
    "progress_expr": None,
    "target": "'/Users/ckiehl/Documents/Gooey/venv/bin/python' -u '/Users/ckiehl/Documents/Gooey/gooey/examples/demo.py'",
    "num_optional_cols": 2,
    "disable_progress_bar_animation": False,
    "layout_type": "standard",
    "program_name": "Widget Demo",
    "show_advanced": True,
    "manual_start": False,
    "image_dir": "default",
    "progress_regex": None,
    "group_by_type": True,
    "num_required_cols": 2,
    "language": "english",
    "monospace_display": False,
    "disable_stop_button": False,
    "program_description": "Example application to show Gooey's various widgets",
    "default_size": [
    610,
    530
    ],
    "required_args": {},
    "optional_args": {},
}

widget_state = {
    0: {
        "value": '',
        "required": True,
        # other junk
    },
    'n': {
        'value': 'foo',
        'required': False,
        'other': 'foo'
    },
    'categories': {
        'curl': [0,1,2],
        'ffmpeg': [3,4,5]
    }
}


def settings_reducer(state, action):
    if state is None:
        return initial_state

def app_reducer(state, action):
    if action['type'] == 'pass':
        pass

def widgetstate_reducer(state, action):
    print('widgetstate_reducer:', state, action)
    if state == None:
        return widget_state
    if action['type'] == 'UPDATE_WIDGET':
        return assign({}, state, {
            action['id']: assign({}, state[action['id']], {
                "value": action['value'],
            })
        })
    else:
        return state


# need to put buildspec defaults in here before passing down to Form object
store = create_store(widgetstate_reducer)



# ----------------------------
# Qt ordering
# 1. Create QApp
app = QApplication(sys.argv)
# 2. initialize all our forum junk
form = Form(store)
# 3. Now that the form objects actually exist, dispatch any initial junk that's
# required

store.dispatch({'type': 'UPDATE_WIDGET', 'id': 0, 'value': 'initialize!'})
# show
form.show()

app.exec_()
