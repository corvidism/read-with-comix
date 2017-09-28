import os
# The class that all Interface Action plugin wrappers must inherit from
from calibre.customize import InterfaceActionBase

class ReadWithComix(InterfaceActionBase):

	name                = 'Read With Comix' # Name of the plugin
	description         = 'Creates a folder of symlinks of selected comics so it can be read in sequence by Comix (or possibly other comic readers - untested).'
	supported_platforms = ['linux'] # Platforms this plugin will run on
	author              = 'Corvidism' # The author of this plugin
	version             = (1, 0, 0)   # The version number of this plugin
	minimum_calibre_version = (1, 48, 0)
	actual_plugin		= 'calibre_plugins.read_with_comix.ui:RWC_GUI'
	
	def is_customizable(self):
		return False
