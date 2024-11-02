import dearpygui.dearpygui as dpg
import os
from dvs_core import dvs_core, router

class dvs_gui:
    def __init__( self ):
        dpg.create_context( )
        self.root = dpg.add_window( tag = "Primary Window" )
        dpg.create_viewport( title = "Distance Vector Simulation", width = 800, height = 600 )
        dpg.setup_dearpygui( )
        dpg.show_viewport( )
        dpg.set_primary_window( "Primary Window", True )
        self.create_node_editor( )
        self.create_menu_bar( )
        self.main_loop( )

    def main_loop( self ):
        # dpg.start_dearpygui( )
        while dpg.is_dearpygui_running( ):
            dpg.render_dearpygui_frame( )
        dpg.destroy_context( )

    def create_menu_bar( self ):
        ##### Menu Bar
        menu_bar = dpg.add_menu_bar( parent = self.root )
        file_menu = dpg.add_menu( label = "File", parent = menu_bar )
        dpg.add_menu_item( label = "Load", parent = file_menu, callback = lambda : self.select_file( "load" ) )
        dpg.add_menu_item( label = "Save", parent = file_menu, callback = lambda : self.select_file( "save" ))
        dpg.add_menu_item( label = "Save As", parent = file_menu, callback = lambda : self.select_file( "save_as" ))

        ##### Settings Menu
        settings_menu = dpg.add_menu( label = "Settings", parent = menu_bar )
        settings_table = dpg.add_table( header_row = False, parent = settings_menu )
        dpg.add_table_column( parent = settings_table, init_width_or_weight = 1 )
        dpg.add_table_column( parent = settings_table, init_width_or_weight = 3 )

        s_row = dpg.add_table_row( parent = settings_table )
        mode_label = dpg.add_text( "Mode: ", parent = s_row )
        mode_tooltip = dpg.add_tooltip( mode_label )
        dpg.add_text \
        (
            "Determines the update mode for the simulation.\
            \nDiscrete pauses at each routing table update.\
            \nContinuous runs until the system reaches a stable state.",
            parent = mode_tooltip 
        )
        dpg.add_radio_button( label = "Mode", parent = s_row, tag = "time_mode", items = [ "Discrete", "Continuous" ])

        ##### About Menu
        about_menu = dpg.add_menu( label = "About", parent = menu_bar )
        dpg.add_text \
        (
            "This program simulates distance vector routing using\
            \nthe Bellman-Ford algorithm to showcase how routers\
            \nexchange their distance vector tables. Each node represents\
            \na router and each link represents a network connection.",
            parent = about_menu
        )

    def select_file( self, option ):
        f_dialog = dpg.add_file_dialog( show = True, default_path = os.getcwd( ), height = 300 )
        dpg.add_file_extension( ".txt", parent = f_dialog )
        if option == "load":
            dpg.set_item_callback( f_dialog, self.load )
        elif option == "save":
            dpg.set_item_callback( f_dialog, self.save )
        else:
            dpg.set_item_callback( f_dialog, self.save_as )

    def load( self, _, app_data ):
        filename = app_data[ "file_name" ]
        res, s = dvs_core( ).load( filename )
        if not res:
            print( s )

    def save( self, _, app_data ):
        pass
    
    def save_as( self, _, app_data ):
        pass

    def create_node_editor( self ):
        # node_editor = dpg.add_node_editor( callback = self.link_node, delink_callback = self.delink_node, parent = self.root )
        # n_1 = dpg.add_node( label = "Router 1", tag = "router_1", parent = node_editor )
        # a_1 = dpg.add_node_attribute( label = "Link Cost", parent = n_1 )
        # i_1 = dpg.add_input_float( label = "Cost", default_value = 7.0, parent = a_1 )
        pass

    def link_node( self ):
        pass

    def delink_node( self ):
        pass

dvs_gui( )