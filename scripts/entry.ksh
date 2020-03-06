#
#
#

# a quirk of the application
if [ ! -L static/submitted_images ]; then
   cd static
   ln -s data/bestsellers/images submitted_images
   cd ..
fi

# move to root and start the application server
cd ..
gunicorn -w 4 -b 0.0.0.0:8080 bestsellers:app

#
# end of file
#
