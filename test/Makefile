# Created by Andre Anjos <andre.dos.anjos@cern.ch> 
# Thu  4 Mar 23:14:52 2010 

# a little make function to ease the administration task
admin=PYTHONPATH=$(2) ../sw/bin/django-admin.py $(1) --settings=settings
python=../sw/bin/python
project=flatties

all:
	@if [ ! -e db.sql3 ]; then $(MAKE) admin; fi
	@if [ ! -L $(project) ]; then ln -s ../$(project)/media $(project); fi
	$(call admin,runserver,..:.) 8080

admin:
	$(call admin,syncdb,.) --noinput
	$(python) ./initial_data.py
	@if [ -e test_data.json ]; then $(call admin,loaddata test_data.json,..:.); fi

shell:
	$(call admin,shell,.)

clean:
	@find . -name '*.pyc' -print0 | xargs -0 rm -f
	@find . -name '*~' -print0 | xargs -0 rm -f

smtp:
	$(python) -m smtpd -n -c DebuggingServer localhost:1025

mrproper: clean
	@rm -f $(project)
	@rm -rf packages
	@rm -f *.sql3
