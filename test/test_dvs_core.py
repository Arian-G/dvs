import unittest
import sys
import os
sys.path.append( "../src" )
from dvs_core import dvs_core, router

class test_router( unittest.TestCase ):
    def setUp( self ):
        self.router = router( 1 )
        self.router.update_dv_table( router( 2 ), 10 )

    def test_update_dv_table( self ):
        # Check connection and cost
        self.assertIn( 2, self.router.dv_table )
        self.assertEqual( 10, self.router.dv_table[ 2 ] )

class test_dvs_core( unittest.TestCase ):
    def setUp( self ):
        self.dvs_core = dvs_core( )
        self.filename = "test_input.txt"
        with open( self.filename, "w" ) as file:
            file.write( "1 2 7\n2 3 1\n1 5 1\n4 5 2\n2 5 8\n4 3 2" )
        loc = "../test/"
        self.dvs_core.load( loc + self.filename )

    def test_initialization( self ):
        # Check routers dict.
        self.assertIn( 1, self.dvs_core.routers )
        self.assertIn( 5, self.dvs_core.routers )
        # Check dv_table dicts.
        self.assertEqual( self.dvs_core.routers[ 1 ].dv_table[ 2 ], 7 )
        self.assertEqual( self.dvs_core.routers[ 2 ].dv_table[ 5 ], 8 )
        self.assertEqual( self.dvs_core.routers[ 5 ].dv_table[ 2 ], 8 ) # Check bi-directional.

    def tearDown( self ):
        os.remove( self.filename )

class test_network( unittest.TestCase ):
    def setUp( self ):
        self.dvs_core = dvs_core( )
        self.filename = "test_input.txt"
        with open( self.filename, "w" ) as file:
            file.write( "1 2 7\n2 3 1\n1 5 1\n4 5 2\n2 5 8\n4 3 2" )
        loc = "../test/"
        self.dvs_core.load( loc + self.filename )

    def test_dv_propogation( self ):
        pass

    def tearDown( self ):
        os.remove( self.filename )

if __name__ == "__main__":
    unittest.main( )