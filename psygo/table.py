
import logging; log = logging.getLogger("psygo.table")
DEBUG=log.debug; INFO=log.info; WARN=log.warning; ERROR=log.error

import psycopg2

from pyramid.decorator import reify
from pyramid.view import view_config
from pyramid.renderers import get_renderer

class Browser(object):

    def __init__(self, context, req):

        self.context = context
        self.req = req

    @reify
    def main(self):
        return get_renderer('templates/main.pt').implementation()

    @reify
    def cursor(self):
        p = "dbname=template1 user=postgres"
        INFO("openning connection %s" % p)
        self._connection = psycopg2.connect(p)
        return self._connection.cursor()

    @reify
    def psycopg_info(self):
        INFO("rendering info")
        return { 
            'apilevel': psycopg2.apilevel,
            'threadsafety': psycopg2.threadsafety,
            'paramstyle': psycopg2.paramstyle,
        }

    @reify
    def column_info(self):

        if not self.cursor.description:
            WARN("bad pre-execute call to column_info")
            return {}

        def f(col):
            return { 'name': col.name, 'type': col.type_code }

        return [ f(x) for x in self.cursor.description ]

    @reify
    def rows(self):
        return self.cursor.fetchall()
    
    @view_config(route_name='table_j', renderer='json')
    def table_j(self):

        q = "select * from %(table)s"
        h = { 
            'table': self.req.matchdict["table"],
        }
        self.cursor.execute(q % h)

        def c(ci):
            return { 'sTitle': ci.get("name") } 

        h = {}

        h["aoColumns"] = [ c(x) for x in self.column_info ]
        h["aaData"] = self.rows

        return h

        
    @view_config(route_name='table', renderer='templates/table.pt')
    def table(self):
        h = { 
            'table': self.req.matchdict["table"],
        }
        return h

