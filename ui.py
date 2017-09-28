#calibre-customize -b .
#calibre-debug -g

# The class that all interface action plugins must inherit from
from calibre.gui2.actions import InterfaceAction
from datetime import datetime
import os, subprocess
#from calibre_plugins.read_with_comix.main import CRSA_Dialog

class RWC_GUI(InterfaceAction):
	name = 'Read With Comix'
	
	action_spec = ('Read selected with Comix', None, 'Read selected with Comix', None)
	
	def genesis(self):
		#print "This sets up plugin stuff."
		self.qaction.triggered.connect(self.do_a_thing)
		
	def is_library_view(self):
		# 0 = library, 1 = main, 2 = card_a, 3 = card_b
		return self.gui.stack.currentIndex() == 0
        
	def do_a_thing(self):
		if not self.gui.current_view().selectionModel().selectedRows() :
			self.gui.status_bar.show_message("No books selected", 3000)
		else:
			if self.is_library_view():
				api = self.gui.current_db.new_api
				book_ids = self.gui.library_view.get_selected_ids()
				tmp_dir_path = '/tmp/crsa-{}'.format(str(datetime.now().strftime("%Y%m%d%H%M%S")))
				os.mkdir(tmp_dir_path)
				books = []
				for book_id in book_ids:
					book_formats = api.formats(book_id,True)
					book_format = ''
					
					if 'CBR' in book_formats:
						book_format = 'CBR'
						book_path = api.format_abspath(book_id, book_format)
						#get cbr
					elif 'CBZ' in book_formats:
						book_format = 'CBZ'
						book_path = api.format_abspath(book_id, book_format)
						#get cbz
					
					if book_format != '':
						book_filename = book_path.split("/")[-1]
						books.append({
							'path':book_path,
							'extension':book_format,
							'filename':book_filename
						})
				
				book_count = len(books)
				if book_count <= 0:
					self.gui.status_bar.show_message("No cbr/cbz files to open.", 3000)
				else:
					self.gui.status_bar.show_message("Opening {} comics.".format(book_count), 3000)	
					print "book ids: {}".format(str(book_ids))		
					for count, book in enumerate(books):
						#print book
						link_path = "{}/{:03d}_{}".format(tmp_dir_path,count,book['filename'])
						book['symlink'] = link_path
						os.symlink(book['path'],link_path)
					
					try:
						#TODO add setting for custom external viewer
						subprocess.check_call(['comix',books[0]['symlink']])
					except (subprocess.CalledProcessError,OSError) as e:
						try:
							subprocess.check_call(['mcomix',books[0]['symlink']])
						except:
							self.gui.status_bar.show_message("Error: comix not found on system.", 3000)				
