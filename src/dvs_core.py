import socket as s
import threading as th
import time as t
import json as js

class router:
    def __init__( self, router_id ):
        self.router_id = router_id
        self.dv_table = { }
        self.neighbors = set( )

    def update_dv_table( self, router, cost ):
        self.dv_table[ router ] = cost

    def update_neighbors( self, router ):
        self.neighbors.add( router )

    def propogate_dv( self, conn ):
        # TODO: add Bellman-Ford algorithm
        for neighbor in self.neighbors:
            message = js.dumps({ self.router_id, self.dv_table })
            conn.sendall( message.encode( ))

class dvs_core:
    def __init__( self ):
        self.routers = { }      # router_id -> router( )
        self.connections = { }  # router_id -> socket connection

    def start_server( self, host = "localhost", port = 8080 ):
        server_socket = s.socket( s.AF_INET, s.SOCK_STREAM )
        server_socket.bind( host, port )
        server_socket.listen( 7 )

        try:
            while True:
                conn, addr = server_socket.accept( )
                th.Thread( target = self.router_handler, args = ( conn, addr )).start( )
        except Exception:
            s = "core_start_server: Unexpected error encountered."
            return False, s
        finally:
            server_socket.close( )

    def router_handler( self, conn, addr ):
        try:
            while True:
                data = conn.recv( 1024 )
                if not data: break
                dv_data = js.loads( data.decode( ))
                for router_id, dv in dv_data.items( ):
                    self.routers[ router_id ].dv_table.update( dv )

                self.routers[ router_id ].propogate_dv( conn )
        except Exception:
            pass
        finally:
            conn.close( )

    def load( self, filename ):
        try:
            with open( filename, "r" ) as file:
                for line in file:
                    a_id, b_id, cost = map( int, line.split( ))

                    if a_id not in self.routers:
                        a = router( a_id )
                        self.routers[ a_id ] = a
                    if b_id not in self.routers:
                        b = router( b_id )
                        self.routers[ b_id ] = b

                    a.update_dv_table( b, cost )
                    a.update_neighbors( b )
                    b.update_dv_table( a, cost )
                    b.update_neighbors( a )
        except FileNotFoundError:
            s = "core_load: File not found."
            return False, s
        except Exception:
            s = "core_load: Unexpected error encountered."
            return False, s
    
    def save( self ):
        pass




