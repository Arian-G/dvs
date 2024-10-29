import unittest
import sys
import os
sys.path.append( "../src" )
from dvs_core import dvs_core, router

class test_router( unittest.TestCase ):
    def setUp( self ):
        self.router = router( 1 )

    def test_update_dv_table( self ):
        self.router.update_dv_table( router( 2 ), 10 )
        # Check connection and cost
        self.assertIn( 2, self.router.dv_table )
        self.assertEqual( 10, self.router.dv_table[ 2 ] )

class test_dvs_core( unittest.TestCase ):
    def setUp( self ):
        self.dvs_core = dvs_core( )

    def test_initialization( self ):
        # Check file load.
        self.filename = "text_input.txt"
        with open( self.filename, "w" ) as file:
            file.write( "1 2 5\n3 2 10" )
        loc = "../test/"
        self.dvs_core.load( loc + self.filename )
        # Check routers dict.
        self.assertIn( 1, self.dvs_core.routers )
        self.assertIn( 2, self.dvs_core.routers )
        # Check dv_table dicts.
        self.assertEqual( self.dvs_core.routers[ 1 ].dv_table[ 1 ], 0 )
        self.assertEqual( self.dvs_core.routers[ 1 ].dv_table[ 2 ], 5 )
        self.assertEqual( self.dvs_core.routers[ 2 ].dv_table[ 3 ], 10 )

    def tearDown( self ):
        os.remove( self.filename )

if __name__ == "__main__":
    unittest.main( )