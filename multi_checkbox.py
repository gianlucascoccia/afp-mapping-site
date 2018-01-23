from wtforms import SelectMultipleField, widgets
from wtforms.compat import text_type
from wtforms.widgets import TableWidget, html_params, HTMLString


class TableColWidget(TableWidget):
    """
    Renders a list of fields as a set of table rows with th/td pairs.

    Hidden fields will not be displayed with a row, instead the field will be
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.
    """
    def __init__(self, with_table_tag=True):
        super().__init__(with_table_tag)

    def __call__(self, field, **kwargs):
        html = []
        hidden = ''
        for subfield in field:
            if subfield.type in ('HiddenField', 'CSRFTokenField'):
                hidden += text_type(subfield)
            else:
                html.append('<td %s ><div class="table-cell">%s</span></td>' % (html_params(**kwargs), text_type(subfield)))
                hidden = ''
        if hidden:
            html.append(hidden)
        return HTMLString(''.join(html))


class MultiCheckboxField(SelectMultipleField):
    widget = TableColWidget(with_table_tag=False)
    option_widget = widgets.CheckboxInput()

