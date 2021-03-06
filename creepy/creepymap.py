'''
Copyright 2010 Yiannis Kakavas

This file is part of creepy.

    creepy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    creepy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with creepy  If not, see <http://www.gnu.org/licenses/>.
    
'''



from threading import Thread
import cree
import helper
import gobject
import gtk.gdk
import os
import osmgpsmap
from tweepy import OAuthHandler as oauth
import webbrowser
from configobj import ConfigObj
import shutil
import pango


gobject.threads_init()
gtk.gdk.threads_init()


class CreepyUI(gtk.Window):
    """
    The main GUI class
    
    Provides all the GUI functionality for creepy. 
    """

    def __init__(self):
        self.CONF_DIR = os.path.join(os.path.expanduser('~'), '.creepy')
        self.locations = []
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        self.set_default_size(800, 600)
        self.connect('destroy', lambda x: gtk.main_quit())
        self.set_title('Cree.py location creeper')
        
        #If it is the first time creepy is run copy the config file and necessary images to .creepy
        if not os.path.exists(self.CONF_DIR):
            os.mkdir(self.CONF_DIR)
            #If creepy was installed through the .deb package in ubuntu , the files needed would be in /usr/share/pyshared/creepy
            if os.path.exists('/usr/share/pyshared/creepy'):
                try:
                    shutil.copy('/usr/share/pyshared/creepy/include/creepy.conf', os.path.join(self.CONF_DIR, 'creepy.conf'))
                    shutil.copy('/usr/share/pyshared/creepy/include/evil_twitter.png', os.path.join(self.CONF_DIR, 'evil_twitter.png'))
                    shutil.copy('/usr/share/pyshared/creepy/include/flickr.png', os.path.join(self.CONF_DIR, 'flickr.png'))
                    shutil.copy('/usr/share/pyshared/creepy/include/index.png', os.path.join(self.CONF_DIR, 'index.png'))
                    shutil.copy('/usr/share/pyshared/creepy/include/default.jpg', os.path.join(self.CONF_DIR, 'default.jpg'))
                except Exception, err:
                    print err
            #If creepy is run from source folder (i.e. in Backtrack) with 'python creepymap.py' , needed files are in current dir
            else:
                try:
                    shutil.copy('include/creepy.conf', os.path.join(self.CONF_DIR, 'creepy.conf'))
                    shutil.copy('include/evil_twitter.png', os.path.join(self.CONF_DIR, 'evil_twitter.png'))
                    shutil.copy('include/flickr.png', os.path.join(self.CONF_DIR, 'flickr.png'))
                    shutil.copy('include/index.png', os.path.join(self.CONF_DIR, 'index.png'))
                    shutil.copy('include/default.jpg', os.path.join(self.CONF_DIR, 'default.jpg'))
                except Exception, err:
                    print err	 
            #create the temp folders
            os.makedirs(os.path.join(self.CONF_DIR, 'cache'))
            os.makedirs(os.path.join(self.CONF_DIR, 'images'))
            os.makedirs(os.path.join(self.CONF_DIR, 'images', 'profilepics'))  
            #write to the initial configuration file
            config_file = os.path.join(self.CONF_DIR, 'creepy.conf')
            tmp_conf = ConfigObj(infile=config_file)
            tmp_conf.create_empty=True
            tmp_conf.write_empty_values=True 
            tmp_conf['directories']['img_dir'] = os.path.join(self.CONF_DIR, 'images')
            tmp_conf['directories']['cache_dir'] = os.path.join(self.CONF_DIR, 'cache')
            tmp_conf['directories']['profilepics_dir'] = os.path.join(self.CONF_DIR, 'images', 'profilepics')
            tmp_conf.write()
        
        #Fix only for version 0.1.73 to copy the creepy32.png to the config folder
        if os.path.exists('/usr/share/pyshared/creepy'):
            try:
                shutil.copy('/usr/share/pyshared/creepy/include/creepy32.png', os.path.join(self.CONF_DIR, 'creepy32.png'))
            except  Exception, err:
                print err
        else:
            try:
                shutil.copy('include/creepy32.png', os.path.join(self.CONF_DIR, 'creepy32.png'))
            except Exception, err:
                print err
                
                
        #Try to load the options file
        try:
            config_file = os.path.join(self.CONF_DIR, 'creepy.conf')
            self.config = ConfigObj(infile=config_file)
            self.config.create_empty=True
            self.config.write_empty_values=True
            self.set_auth(self.config)
            self.profilepics_dir = self.config['directories']['profilepics_dir']
            
        except Exception, err:
            text = 'Error parsing configuration file : %s' % err
            self.create_dialog('Error', text)
            
            
        #check if dirs for temp data exist and if not try to create them
        if not os.path.exists(self.config['directories']['img_dir']):
            self.create_directory(self.config['directories']['img_dir'])
        if not os.path.exists(self.config['directories']['profilepics_dir']):
            self.create_directory(self.config['directories']['profilepics_dir'])
        if not os.path.exists(self.config['directories']['cache_dir']):
            self.create_directory(self.config['directories']['cache_dir'])
        
        #Create an outer Vbox to include everything
        outer_box = gtk.VBox(False, 0)
        self.add(outer_box)
        #Create a menu bar
        mb = gtk.MenuBar()
        filemenu = gtk.Menu()
        file = gtk.MenuItem("Creepy")
        file.set_submenu(filemenu)
        
        
        select_source_menu = gtk.Menu()
        select_source = gtk.MenuItem("Map Source")
        select_source.set_submenu(select_source_menu)
        google_sat = gtk.MenuItem('Google Satellite')
        google_sat.connect('activate', self.reload_map, osmgpsmap.SOURCE_GOOGLE_SATELLITE)
        select_source_menu.append(google_sat)
        google_str = gtk.MenuItem('Google Street')
        google_str.connect('activate', self.reload_map, osmgpsmap.SOURCE_GOOGLE_STREET)
        select_source_menu.append(google_str)
        google_hyb = gtk.MenuItem('Google Hybrid')
        google_hyb.connect('activate', self.reload_map, osmgpsmap.SOURCE_GOOGLE_HYBRID)
        select_source_menu.append(google_hyb)
        openstreet = gtk.MenuItem('OpenStreetMap')
        openstreet.connect('activate', self.reload_map, osmgpsmap.SOURCE_OPENSTREETMAP)
        select_source_menu.append(openstreet)
        mapsforfree = gtk.MenuItem('Maps For Free')
        mapsforfree.connect('activate', self.reload_map, osmgpsmap.SOURCE_MAPS_FOR_FREE)
        select_source_menu.append(mapsforfree)
        virtualearth_sat = gtk.MenuItem('Virtual Earth Satellite ')
        virtualearth_sat.connect('activate', self.reload_map, osmgpsmap.SOURCE_VIRTUAL_EARTH_SATELLITE)
        select_source_menu.append(virtualearth_sat)
        virtualearth_str = gtk.MenuItem('Virtual Earth Street')
        virtualearth_str.connect('activate', self.reload_map, osmgpsmap.SOURCE_VIRTUAL_EARTH_STREET)
        select_source_menu.append(virtualearth_str)
        virtualearth_hyb = gtk.MenuItem('Virtual Earth Hybrid ( Default )')
        virtualearth_hyb.connect('activate', self.reload_map, osmgpsmap.SOURCE_VIRTUAL_EARTH_HYBRID)
        select_source_menu.append(virtualearth_hyb)
        openaerial = gtk.MenuItem('OpenAerialMap')
        openaerial.connect('activate', self.reload_map, osmgpsmap.SOURCE_OPENAERIALMAP)
        select_source_menu.append(openaerial)
        filemenu.append(select_source)
        
        export_menu = gtk.Menu()
        export = gtk.MenuItem("Export as..")
        export.set_submenu(export_menu)
        export_kml = gtk.MenuItem("Export as kml")
        export_kml.connect('activate', self.export_locations, 'kml')
        export_menu.append(export_kml)
        export_csv = gtk.MenuItem("Export as csv")
        export_csv.connect('activate', self.export_locations, 'csv')
        export_menu.append(export_csv)
        filemenu.append(export)
        
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", gtk.main_quit)
        filemenu.append(exit)
        
        editmenu = gtk.Menu()
        edit = gtk.MenuItem("Edit")
        edit.set_submenu(editmenu)
        
        settings = gtk.MenuItem('Settings')
        settings.connect('activate', self.settings_dialog)
        editmenu.append(settings)
        
        helpmenu = gtk.Menu()
        help = gtk.MenuItem("Help")
        help.set_submenu(helpmenu)
        
        report = gtk.MenuItem('Report a bug/problem')
        report.connect('activate', self.open_url, 'https://github.com/ilektrojohn/creepy/issues')
        helpmenu.append(report)
        
        sep = gtk.SeparatorMenuItem()
        helpmenu.append(sep)
        
        about = gtk.MenuItem('About')
        about.connect('activate', self.show_about_dialog)
        helpmenu.append(about)
                
        mb.append(file)
        mb.append(edit)
        mb.append(help)
        menubox = gtk.VBox(False, 2)
        menubox.pack_start(mb, False, False, 0)
        outer_box.pack_start(menubox, False, False, 0)
        
        # Creates the notebook layout
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        outer_box.pack_start(self.notebook)
        
        #Creates the Map overview tab and adds it to the notebook
        tab1 = gtk.VBox(False, 0)
        label1 = gtk.Label("Map View")
        self.notebook.append_page(tab1, label1)
        
        #Load the map
        self.osm = osmgpsmap.GpsMap(map_source=osmgpsmap.SOURCE_VIRTUAL_EARTH_HYBRID)
        self.osm.layer_add(
                    osmgpsmap.GpsMapOsd(
                        show_dpad=True,
                        show_zoom=True))
        #Added because default zoom level in google maps shows a white screen
        self.osm.set_zoom(self.osm.props.zoom + 1)
        #connect keyboard shortcuts for the map
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_FULLSCREEN, gtk.gdk.keyval_from_name("F11"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_UP, gtk.gdk.keyval_from_name("Up"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_DOWN, gtk.gdk.keyval_from_name("Down"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_LEFT, gtk.gdk.keyval_from_name("Left"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_RIGHT, gtk.gdk.keyval_from_name("Right"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_ZOOMIN , gtk.gdk.keyval_from_name("KP_Add"))
        self.osm.set_keyboard_shortcut(osmgpsmap.KEY_ZOOMOUT, gtk.gdk.keyval_from_name("KP_Subtract"))
        
        self.osm.connect('button_release_event', self.map_clicked)

        #Create a table for map and locations list
        maploc = gtk.Table(5, 5, True)
        tab1.pack_start(maploc)
        loclist_label = gtk.Label("Locations List")   
        self.loc_list = gtk.VBox(False, 8)
        self.loc_list.add(loclist_label)
    
        maploc.attach(self.loc_list, 0, 2, 0, 5)
        self.update_location_list([])
        self.mapVBox = gtk.VBox(False, 0)
        self.mapVBox.pack_start(self.osm)
        maploc.attach(self.mapVBox, 2, 5, 0, 5)
        
        #

        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textview.connect("button-release-event", self.on_mouseovertextview_motion)
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        info = gtk.ScrolledWindow()
        info.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        info.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        info.add(self.textview)
        
        #Create the horizontal box that holds progressbar
        progressbox = gtk.HBox(False, 0)
        # Create the ProgressBar
        self.pbar = gtk.ProgressBar()
        self.pbar.show()
        progressbox.pack_start(self.pbar, True, True, 40)
       
        
        

        tab1.pack_end(info, False)
        tab1.pack_end(progressbox, False)

        
        #Create the targets tab
        tab2 = gtk.VBox(False, 0)
        label2 = gtk.Label('Targets')
        self.notebook.prepend_page(tab2, label2)
        
        
        #Create a table to hold all stuff here
        search_table = gtk.Table(20, 10, True)
        targets_instructions = gtk.Label('Fill in the details for your targets or use the search function below')
        twitter_target_label = gtk.Label()
        twitter_target_label.set_markup('<b><i>Twitter Username</i></b>')
        self.twitter_target = gtk.Entry()
        flickr_target_label = gtk.Label()
        flickr_target_label.set_markup('<b><i>Flickr UserID</i></b>')
        flickr_example_label = gtk.Label()
        flickr_example_label.set_markup('<i>( XXXXXXXX@XXX )</i>')
        showbuttontext = '<b>Geolocate \n    Target</b>'
        self.show_button = gtk.Button(showbuttontext)
        self.show_button.child.set_use_markup(True)
        self.show_button.connect('clicked', self.thread_show_clicked)
        separator = gtk.HSeparator()
        self.flickr_target = gtk.Entry()
        self.twitter_username = gtk.Entry()
        tsearchtext = gtk.Label()
        stext = "<i>Use the form below to search for twitter users if necessary</i>"
        tsearchtext.set_markup(stext)
        fsearchtext = gtk.Label()
        ftext = "<i>Use the form below to search for flickr users if necessary</i>"
        fsearchtext.set_markup(ftext)
        t_label1 = gtk.Label('Search for:')
        search_twitter_button = gtk.Button('Search')
        search_twitter_button.connect('clicked', self.thread_search_twitter)
        clear_twitter_button = gtk.Button('Clear')
        clear_twitter_button.connect('clicked', self.clear_twitter_list)
        twitter_im = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(self.CONF_DIR, 'evil_twitter.png'))
        scaled_buf = pixbuf.scale_simple(50,50,gtk.gdk.INTERP_BILINEAR)
        twitter_im.set_from_pixbuf(scaled_buf)
        

        self.twitter_list = gtk.VBox(False, 0)
        search_table.attach(targets_instructions, 0, 6, 0, 1)
        search_table.attach(twitter_target_label, 0, 2, 1, 2)
        search_table.attach(self.twitter_target, 2, 4 , 1, 2)
        search_table.attach(flickr_target_label, 0, 2, 2, 3)
        search_table.attach(self.flickr_target, 2, 4, 2, 3)
        search_table.attach(flickr_example_label, 4, 6, 2, 3)
        search_table.attach(self.show_button, 8, 10, 1, 3)
        search_table.attach(separator, 0, 10, 3, 4)
        search_table.attach(tsearchtext, 2, 8, 5, 6)
        search_table.attach(twitter_im, 0, 1, 4, 6)
        search_table.attach(t_label1, 0, 1, 6, 7)
        search_table.attach(self.twitter_username, 1, 4, 6, 7)
        search_table.attach(search_twitter_button, 5, 7, 6, 7)
        search_table.attach(clear_twitter_button, 8, 10, 6, 7)
        search_table.attach(self.twitter_list, 0, 10, 7, 12)
        self.update_twitterusername_list([])
        
        #add flickr search
        flickr_im = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(self.CONF_DIR, 'flickr.png'))
        scaled_buf = pixbuf.scale_simple(50,50,gtk.gdk.INTERP_BILINEAR)
        flickr_im.set_from_pixbuf(scaled_buf)
        

        self.flickr_list = gtk.VBox(False, 0)
        t_label2 = gtk.Label('Search for:')
        self.flickr_username = gtk.Entry()
        search_flickr_button = gtk.Button('Search')
        search_flickr_button.connect('clicked', self.thread_search_flickr)
        search_flickrreal_button = gtk.Button('Search for real name')
        search_flickrreal_button.connect('clicked', self.thread_search_flickr_realname)
        clear_flickr_button = gtk.Button('Clear')
        clear_flickr_button.connect('clicked', self.clear_flickr_list)
        search_table.attach(fsearchtext, 2, 8, 13, 14)
        search_table.attach(flickr_im, 0, 1, 12, 14)
        search_table.attach(t_label2, 0, 1, 14, 15)
        search_table.attach(self.flickr_username, 1, 4, 14, 15)
        search_table.attach(search_flickr_button, 4, 5, 14, 15)
        search_table.attach(search_flickrreal_button, 5, 8, 14, 15)
        search_table.attach(clear_flickr_button, 8, 10, 14, 15)

        
        search_table.attach(self.flickr_list, 0, 10, 15, 20)
        self.update_flickrusername_list([])
        
        tab2.pack_start(search_table)
        self.notebook.set_current_page(0)
    def settings_dialog(self, button):
        settings = gtk.Dialog('Creepy Settings', None, 0, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        settings.set_default_size(400, 200)
        self.settings_notebook = gtk.Notebook()
        self.twitbox = gtk.VBox(False, 0)
      
        #If creepy is already authorized, hide the option
        if self.config['twitter_auth']['access_key'] !='' and self.config['twitter_auth']['access_secret'] != '':
            self.set_twit_options(authorized=True)
        else:
            self.set_twit_options(authorized=False)
            
        flickr_options = gtk.VBox(False, 0)
        flabel = gtk.Label('Flickr')
        flickr_key_label = gtk.Label('Flickr API key')
        flickr_key_label.set_alignment(0,0.5)
        self.flickr_key = gtk.Entry()
        if self.config['flickr']['api_key'] != '':
            self.flickr_key.set_text(self.config['flickr']['api_key'])
        flickr_options.pack_start(flickr_key_label)
        flickr_options.pack_start(self.flickr_key)
        
        
        dir_label = gtk.Label('Photo locations')
        img_options = gtk.VBox(False, 0)
        img_options_label = gtk.Label('Saved images')
        img_options_label.set_alignment(0,1)
        prof_options_label = gtk.Label('Saved profile pictures')
        prof_options_label.set_alignment(0,1)
        self.img_options_entry = gtk.Entry()
        self.prof_options_entry = gtk.Entry()
        self.img_options_entry.set_text(self.config['directories']['img_dir'])
        self.prof_options_entry.set_text(self.config['directories']['profilepics_dir'])
        img_options.pack_start(img_options_label)
        img_options.pack_start(self.img_options_entry)
        img_options.pack_start(prof_options_label)
        img_options.pack_start(self.prof_options_entry)
        clear_cache_button = gtk.Button('Clear photos cache')
        clear_cache_button.connect('clicked', self.clear_photo_cache)
        img_options.pack_start(clear_cache_button)
        self.settings_notebook.append_page(flickr_options, flabel)
        self.settings_notebook.append_page(img_options, dir_label)
        settings.vbox.pack_start(self.settings_notebook)
        
        settings.show_all()
        response = settings.run()
        if response == gtk.RESPONSE_OK:
            self.save_img_options()
            self.save_prof_options()
            self.save_flickr_config()
        settings.destroy()
        
    
    def startprogressbox(self):
        # Add a timer callback to update the value of the progress bar
        self.timer = gobject.timeout_add (100, self.progress_timeout, self.pbar)
    def stopprogressbox(self):
        gobject.source_remove(self.timer)
        self.pbar.set_fraction(0)
    # Update the value of the progress bar so that we get
    # some movement
    def progress_timeout(self, pbobj):
        pbobj.pulse()
        return True    
    def clear_photo_cache(self, button):
        folders = (self.config['directories']['img_dir'], self.config['directories']['profilepics_dir'])
        for folder in folders:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception, err:
                    error_text = 'Error deleting folders, please do it manually. Error was : %s' % err
                    self.create_dialog('Error ', error_text)
        text = 'Contents of folder were successfully deleted' 
        self.create_dialog('Success', text)
        
    def save_img_options(self):
        self.config['directories']['img_dir'] = self.img_options_entry.get_text()
        self.config.write()
    def save_prof_options(self):
        self.config['directories']['profilepics_dir'] = self.prof_options_entry.get_text()
        self.config.write()
    def save_flickr_config(self):
        self.config['flickr']['api_key'] = self.flickr_key.get_text()
        self.config.write()
    def set_twit_options(self, authorized):
        twit_label = gtk.Label('Twitter')
        if self.twitbox:
            for i in self.twitbox.get_children():
                self.twitbox.remove(i)
        else:
            self.twitbox = gtk.HBox(False, 0)
        
        if authorized == False :   
            auth_button = gtk.Button('Authorize Creepy')
            auth_button.set_tooltip_text('Clicking this will open your browser to access twitter and get an authorization pin. Copy paste \
the pin to the box below, and hit OK')
            auth_button.connect('clicked', self.button_authorize_twitter)
            self.auth_pin = gtk.Entry()
            auth_pin_label = gtk.Label('Pin :')
            auth_pin_label.set_alignment(0,1)
            self.auth_finalize_button = gtk.Button('OK')
            self.auth_finalize_button.set_sensitive(0)
            self.auth_pin.connect('changed', self.set_button_active)
            self.auth_finalize_button.connect('clicked', self.fin_authorize_twitter)
        
            self.twitbox.pack_start(auth_button, False, False, 15)
            self.twitbox.pack_end(self.auth_finalize_button, False, False, 5)
            self.twitbox.pack_end(self.auth_pin, False, False, 0)
            self.twitbox.pack_end(auth_pin_label, False, False, 5)
            self.settings_notebook.prepend_page(self.twitbox, twit_label)
            self.settings_notebook.set_current_page(0)
            self.settings_notebook.show_all()

        else:
            authorized_label = gtk.Label('Creepy is already authorized for Twitter.')
            reset_button = gtk.Button('reset auth settings')
            reset_button.connect('clicked', self.reset_auth_settings)
            self.twitbox.pack_start(authorized_label, False, False, 0)
            self.twitbox.pack_end(reset_button, False, False, 0)
            self.settings_notebook.prepend_page(self.twitbox, twit_label)
            self.settings_notebook.set_current_page(0)
            self.settings_notebook.show_all()
            
    def set_auth(self, conf_file):    
        self.creepy = cree.Cree(conf_file)   
        
    def reset_auth_settings(self, button):
        self.config['twitter_auth']['access_key'] = ''
        self.config['twitter_auth']['access_secret'] = ''
        self.config.write()
        self.settings_notebook.remove_page(0)    
        #self.settings_table.remove(self.twitbox)
        self.set_twit_options(authorized=False)
      
    def set_button_active(self, button):
        self.auth_finalize_button.set_sensitive(1)
        
    def button_authorize_twitter(self, button):
        self.oauth = oauth(self.config['twitter_auth']['consumer_key'], self.config['twitter_auth']['consumer_secret'])
        url = self.oauth.get_authorization_url(True)
        webbrowser.open(url)
    
    def fin_authorize_twitter(self, button):
        verif = self.auth_pin.get_text().strip()
        try:
            self.oauth.get_access_token(verif)
            message = 'Authentication successful'
            key = self.oauth.access_token.key
            secret = self.oauth.access_token.secret
            self.config['twitter_auth']['access_key'] = key
            self.config['twitter_auth']['access_secret'] = secret
            self.config.write()
            self.settings_notebook.remove_page(0)
            #self.settings_table.remove(self.twitbox)
            self.set_twit_options(authorized=True)
            self.set_auth(self.config)
        except Exception, err:
            message = "Authentication failed with error %s" % (err)
        dialog = gtk.MessageDialog(
                                   parent         = None,
                                   flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
                                   type           = gtk.MESSAGE_INFO,
                                   buttons        = gtk.BUTTONS_OK,
                                   message_format = message)
        dialog.set_title('Twitter authentication')
        dialog.run()
        dialog.destroy()
        
        
    def search_twitter(self, username):
        users = self.creepy.search_for_users('twitter', username)
        if not users or len(users) == 0 :
            self.create_nonmodal_dialog('Error', 'No results for the search query')
        elif users[0] == 'auth_error':
            self.create_nonmodal_dialog('Error', 'Only authenticated users can search for users. Go to Edit->Settings->Twitter to authorize creepy to use your account')
        else:
            gobject.idle_add(self.update_twitterusername_list, users)
    
    def thread_search_twitter(self, button):
        username = self.twitter_username.get_text()
        if username:
            Thread(target=lambda : self.search_twitter(username)).start()
        else :
            self.create_dialog('error', 'You didn\'t specify a search query')
    def search_flickr(self, username):
        users = self.creepy.search_for_users('flickr', username, 'username')
        if not users or len(users) == 0 :
            self.create_nonmodal_dialog('Error', 'No results for the search query')
        else:
            gobject.idle_add(self.update_flickrusername_list, users)
    
    def thread_search_flickr(self, button):   
        name = self.flickr_username.get_text()
        if name:
            Thread(target=lambda : self.search_flickr(name)).start()
        else :
            self.create_dialog('error', 'You didn\'t specify a search query')
    def search_flickr_realname(self, name):
        users = self.creepy.search_for_users('flickr', name, 'realname')
        if not users or len(users) == 0 :
            self.create_nonmodal_dialog('Error', 'No results for the search query')
        else:
            gobject.idle_add(self.update_flickrusername_list, users)
       
        
    def thread_search_flickr_realname(self, button):
        name = self.flickr_username.get_text()
        if name:
            Thread(target=lambda : self.search_flickr_realname(name)).start()
        else :
            self.create_dialog('error', 'You didn\'t specify a search query')
        
    def clear_flickr_list(self, button):    
        self.update_flickrusername_list([])
        
    def clear_twitter_list(self, button):
        self.update_twitterusername_list([])
    def update_twitterusername_list(self,  users):
        for child in self.twitter_list.get_children():
            self.twitter_list.remove(child)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.twitter_list.pack_start(sw, True, True, 0)
        store = self.twitterusername_list_model(users)
        
        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.twitter_set_target)
        treeView.set_rules_hint(True)
        sw.add(treeView)
        
        self.twitterusername_columns(treeView)
        self.show_all()
    
    def twitterusername_list_model(self, users):
        store = gtk.ListStore(str, str, str, gtk.gdk.Pixbuf)
        if users:
            for user in users:
                filename = 'profile_pic_%s' % user.screen_name
                file = os.path.join(self.profilepics_dir, filename)
                try:
                    profile_pic = gtk.gdk.pixbuf_new_from_file(file)
                except Exception:
                    default_file = os.path.join(self.CONF_DIR, 'default.jpg')
                    profile_pic = gtk.gdk.pixbuf_new_from_file(default_file)
                store.append([str(user.id), str(user.screen_name), str(user.name), profile_pic])
        return store
    
    def twitterusername_columns(self, treeView):
        
        rendererText1 = gtk.CellRendererText()
        col0 = gtk.TreeViewColumn("Screen Name")
        col0.pack_start(rendererText1, True)
        col0.set_attributes(rendererText1, text=1)
        col0.set_sort_column_id(0)
        treeView.append_column(col0)
        
        rendererText2 = gtk.CellRendererText()
        col1 = gtk.TreeViewColumn("Full Name")
        col1.pack_start(rendererText2, True)
        col1.set_attributes(rendererText2, text=2)
        col1.set_sort_column_id(1)
        treeView.append_column(col1)
        
        rendererImage = gtk.CellRendererPixbuf()
        col2 = gtk.TreeViewColumn("Photo")
        col2.pack_start(rendererImage, True)
        col2.set_attributes(rendererImage, pixbuf=3)
        treeView.append_column(col2)
    
    def twitter_set_target(self, widget, row, col):
        model = widget.get_model()  
        self.twitter_target.set_text(model[row][1])
        
        
    def update_flickrusername_list(self,  users):
        for child in self.flickr_list.get_children():
            self.flickr_list.remove(child)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.flickr_list.pack_start(sw, True, True, 0)
        store = self.flickrusername_list_model(users)
        
        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.flickr_set_target)
        treeView.set_rules_hint(True)
        sw.add(treeView)
        
        self.flickrusername_columns(treeView)
        self.show_all()
    
    def flickrusername_list_model(self, users):
        store = gtk.ListStore( str, str, str, str, gtk.gdk.Pixbuf)
        if users:
            for user in users:
                try:
                    file = '%sprofile_pic_%s' % (self.profilepics_dir, user['id'])
                    profile_pic = gtk.gdk.pixbuf_new_from_file(file)
                except Exception:
                    file = os.path.join(self.CONF_DIR, 'default.jpg')
                    profile_pic = gtk.gdk.pixbuf_new_from_file(file)
                store.append([str(user['id']), str(user['username']), str(user['realname']), str(user['location']), profile_pic])
        return store
    
    def flickrusername_columns(self, treeView):
        
        rendererText1 = gtk.CellRendererText()
        col0 = gtk.TreeViewColumn("Username")
        col0.pack_start(rendererText1, True)
        col0.set_attributes(rendererText1, text=1)
        col0.set_sort_column_id(1)
        treeView.append_column(col0)
        
        rendererText2 = gtk.CellRendererText()
        col1 = gtk.TreeViewColumn("Full Name")
        col1.pack_start(rendererText2, True)
        col1.set_attributes(rendererText2, text=2)
        col1.set_sort_column_id(2)
        treeView.append_column(col1)
        
        rendererText3 = gtk.CellRendererText()
        col2 = gtk.TreeViewColumn("Location")
        col2.pack_start(rendererText3, True)
        col2.set_attributes(rendererText3, text=3)
        col2.set_sort_column_id(3)
        treeView.append_column(col2)
        
        rendererImage = gtk.CellRendererPixbuf()
        col3 = gtk.TreeViewColumn("Photo")
        col3.pack_start(rendererImage, True)
        col3.set_attributes(rendererImage, pixbuf=4)
        treeView.append_column(col3)
        
    def flickr_set_target(self, widget, row, col):
        
        model = widget.get_model()  
        self.flickr_target.set_text(model[row][0])
        
        
        
    def update_location_list(self,  locations):
        for child in self.loc_list.get_children():
            self.loc_list.remove(child)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.loc_list.pack_start(sw, True, True, 0)
        store = self.location_list_model(locations)
        
        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.location_activated)
        treeView.connect('button-press-event' , self.on_button_press_event)
        treeView.set_rules_hint(True)
        sw.add(treeView)
        
        self.location_columns(treeView)
        self.show_all()
    
    def location_list_model(self, locations):
        store = gtk.ListStore(str, str, str, str, str)
        if locations:
            for loc in locations:
                store.append([loc['context'][0], loc['context'][1], loc['latitude'], loc['longitude'], loc['time']])
            
        return store
    
    def location_columns(self, treeView):
       
        rendererText = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Latitude", rendererText, text=2)
        treeView.append_column(col)
        
        rendererText = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Longitude", rendererText, text=3)
        treeView.append_column(col)
        
        rendererText = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Time", rendererText, text=4)
        col.set_sort_column_id(4)
        treeView.append_column(col)
        
    def copy_to_clipboard(self, obj, coord):
        string = '%s, %s' % (float(coord[0]), float(coord[1]))
        clipboard = gtk.Clipboard(gtk.gdk.display_manager_get().get_default_display(), "CLIPBOARD")
        clipboard.set_text(string)
    
    def open_googlemaps(self, button, coord):
        url = 'http://maps.google.com/maps?q=%s,%s' % (float(coord[0]), float(coord[1]))
        webbrowser.open(url)
    def open_url(self, button, url):
        webbrowser.open_new_tab(url)
           
    def on_mouseovertextview_motion(self, widget, event, data = None):
        def check_if_link(iter):
            tags = iter.get_tags()
            for tag in tags:
                page = tag.get_data("page")
                if page != 0:
                    self.open_url(False, page)
                    break
            
            
        if event.button == 1:
            try:
                start, end = self.textbuffer.get_selection_bounds()
            except ValueError:
                # If there is nothing selected, None is return
                pass
            else:
                if start.get_offset() != end.get_offset():
                    return False
            x, y = widget.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,int(event.x), int(event.y))
            iter = widget.get_iter_at_location(x, y)
            check_if_link(iter)
            
    def on_button_press_event(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                
                model = treeview.get_model()
                
                location_popup = gtk.Menu()
                copy_clipboard = gtk.MenuItem("Copy to clipboard")
                open_googlemap = gtk.MenuItem("Open in browser (google maps)")
                location_popup.append(copy_clipboard)
                location_popup.append(open_googlemap)
                copy_clipboard.connect('activate', self.copy_to_clipboard, (model[path[0]][2], model[path[0]][3]))
                open_googlemap.connect('activate', self.open_googlemaps, (model[path[0]][2], model[path[0]][3]))
                copy_clipboard.show()
                open_googlemap.show()
                location_popup.popup( None, None, None, event.button, time)
            return True
    
        
        
    
    def location_activated(self, widget, row, col):
        
        model = widget.get_model()
        self.osm.set_center_and_zoom(float(model[row][2]), float(model[row][3]), 12)
        self.osm.set_zoom(self.osm.props.zoom + 3)
        self.textbuffer.set_text(model[row][1])
        
        tag = self.textbuffer.create_tag(None,
            foreground="blue", underline=pango.UNDERLINE_SINGLE)
        tag.set_data("page", model[row][0])
        it = self.textbuffer.get_end_iter()
        self.textbuffer.insert_with_tags(it, model[row][0], tag)
    
    def reload_map(self, button, source):
        #remove old map 
        if self.osm:
            self.mapVBox.remove(self.osm)
        try:
            self.osm = osmgpsmap.GpsMap(map_source=source)
        except Exception, e:
            print "ERROR:", e
            self.osm = osmgpsmap.GpsMap()
        self.osm.layer_add(
                    osmgpsmap.GpsMapOsd(
                        show_dpad=True,
                        show_zoom=True))
        #Added because default zoom level in google maps shows a white screen
        self.osm.set_zoom(self.osm.props.zoom + 1)
        self.mapVBox.pack_start(self.osm)
        self.osm.show()
        if self.locations:
            self.draw_locations(self.locations)
    
    def draw_locations(self, locations):
        self.stopprogressbox()
        pb = gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(self.CONF_DIR, 'index.png'), 24,24)
        if locations:
            for l in locations:
                self.osm.image_add(float(l['latitude']), float(l['longitude']), pb)
            self.osm.set_center_and_zoom(float(locations[0]['latitude']), float(locations[0]['longitude']), 12)
        self.notebook.set_current_page(-1)

    def print_tiles(self):
        if self.osm.props.tiles_queued != 0:
            return True


    def search_for_locations(self, twit, flickr):
        
        self.startprogressbox()
        #the username of the twitter target for the specific search
        self.twitter_target_username = self.twitter_target.get_text()
        #the username of the flickr target for the specific search
        self.flickr_target_username = self.flickr_target.get_text()
        self.locations, params = self.creepy.get_locations(self.twitter_target_username, self.flickr_target_username)
        #gobject.idle_add(self.textbuffer.set_text, 'DONE !')
        if params:
            if 'flickr_errors' in params:
                for err in params['flickr_errors']:
                    if err['from'] == 'flickr_photos':
                        textfl = 'Error was %s' % err['error']
                        self.create_nonmodal_dialog('Error connecting to flickr', textfl)
            if 'twitter_errors' in params:
                text = ''
                for err in params['twitter_errors']:
                    if err['from'] == 'twitter_connection':
                        if err['error'] == 'Not found':
                            self.create_nonmodal_dialog('Wrong username', 'The selected target does not correspond to a twitter username. Please \
try the search function if you are unsure ')
                        elif err['error'] == 'Failed to send request: [Errno -2] Name or service not known':
                            self.create_nonmodal_dialog('Connection Error', 'Could not connect to twitter, please check your connection settings and try again')
                        elif err['error'] == 'Not authorized':
                            self.create_nonmodal_dialog('Authentication Error', 'Target\'s timeline is protected and you are not following him/her')
                        else:
                            self.create_nonmodal_dialog('Twitter error', 'We experienced some problems connecting to twitter. We were not able to retrieve all \
of the users tweets. \n ')
                    text += 'Error while accessing %s .The problem was : %s \n ' % (err['url'], err['error'])
      
                text += ' \n %s tweets have been retrieved out of a total of %s. \n From them, we were able to extract %s locations. \n \
                We encountered %s errors in total accessing various services. \n '                                     % (params['tweets'], 
                                                                                                                              params['tweets_count'], 
                                                                                                                              params['locations'], 
                                                                                                                              len(params['twitter_errors']))
                gobject.idle_add(self.textbuffer.insert, self.textbuffer.get_end_iter(), text)     
        gobject.idle_add(self.update_location_list, self.locations)
        gobject.idle_add(self.draw_locations, self.locations)
        gobject.idle_add(self.activate_search_button)
        
    def thread_show_clicked(self, button):
        if not self.twitter_target.get_text() and not self.flickr_target.get_text():
            self.create_dialog('error', 'No targets selected. Please select at least one in targets tab')
        else:
            self.notebook.set_current_page(-1)
            #clear locations from previous search and reload map
            self.locations = []
            self.reload_map(None, osmgpsmap.SOURCE_VIRTUAL_EARTH_HYBRID)
            self.update_location_list([])
            self.textbuffer.set_text('Searching for locations .. Be patient, I am doing my best. \n This can take a while, please hold ... \n')
            Thread(target=lambda : self.search_for_locations(self.twitter_target.get_text(),  self.flickr_target.get_text())).start()
            self.show_button.set_sensitive(0)
    def activate_search_button(self):
        self.show_button.set_sensitive(1)
    
    def create_directory(self, dir):
        try:
            os.makedirs(dir)
        except Exception, err:
            text = 'Could not create the directories for temporary data. Please check your settings. \
            Error was ' % err
            self.create_dialog('Error', text)
    def export_locations(self, button, format):
        if self.locations:
            filesel = gtk.FileChooserDialog('Save as...',
                                            None, 
                                            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            filesel.set_default_response(gtk.RESPONSE_OK)
            response = filesel.run()
            if response == gtk.RESPONSE_OK:
                dir = filesel.get_filename()
            elif response == gtk.RESPONSE_CANCEL:
                dir = None
            filesel.destroy()
            
            if dir:
                if self.twitter_target_username:
                    export_id = self.twitter_target_username
                elif self.flickr_target_username:
                    export_id = self.flickr_target_username
                else:
                    self.create_nonmodal_dialog('Error', 'There are no results to export')
                hel = helper.Helper()
                if format == 'kml':
                    result = hel.create_kml(export_id, dir, self.locations)
                elif format == 'csv':
                    result = hel.create_csv(export_id, dir, self.locations)
                    
                if result == 'Success':
                    self.create_nonmodal_dialog('Success', 'File created successfully and saved at %s' % dir)
                else:
                    self.create_nonmodal_dialog('Error', 'We were unable to export locations . Error was : %s' % result[1] )
        else:
            self.create_nonmodal_dialog('Error', 'There are no results to export')   
    def map_clicked(self, osm, event):
        lat,lon = self.osm.get_event_location(event).get_degrees()
        if event.button == 1:
            pass
        elif event.button == 2:
            pass
        elif event.button == 3:
            pass
    
    def create_dialog (self, title, text):
        dialog = gtk.MessageDialog(
                                   parent         = None,
                                   flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
                                   type           = gtk.MESSAGE_INFO,
                                   buttons        = gtk.BUTTONS_OK,
                                   message_format = text)
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()
    
    def create_nonmodal_dialog (self, title, text):
        dialog = gtk.MessageDialog(
                                   parent         = None,
                                   flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
                                   type           = gtk.MESSAGE_INFO,
                                   buttons        = gtk.BUTTONS_OK,
                                   message_format = text)
        dialog.set_title(title)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()
        
    def show_about_dialog(self, button):
        about = gtk.AboutDialog()
        about.set_program_name("Creepy")
        about.set_version("0.1.9")
        about.set_copyright("(c) Yiannis Kakavas")
        about.set_comments("Creepy is a geolocation information gatherer")
        about.set_website("http://ilektrojohn.github.com/creepy")
        about.set_logo(gtk.gdk.pixbuf_new_from_file(os.path.join(self.CONF_DIR, "creepy32.png")))
        about.run()
        about.destroy()
        
    def main(self):
        self.show_all()
        if os.name == "nt": gtk.gdk.threads_enter()
        gtk.main()
        if os.name == "nt": gtk.gdk.threads_leave()

if __name__ == '__main__':
    u = CreepyUI()
    u.main()

