# Dear emacs, this is -*- Makefile -*-
# Created by Andre Anjos <Andre.dos.Anjos@gmail.com>, 20-Mar-2007

# These are variables you can configure for your application
python=python2.6
LANGUAGES=en pt_BR fr es

# These are helpers
admin=sw/bin/django-admin.py
project=$(shell basename `pwd`)
MAKE_MESSAGE=$(admin) makemessages --all --extension=html,py,txt
COMPILE_MESSAGE=$(admin) compilemessages

# These are some instructions for sessions in vim
VIM_SESSION=.session.vim
edit=if [ -e $(VIM_SESSION) ]; then $(1) --noplugin -S $(VIM_SESSION); else echo "The file \`$(VIM_SESSION)' does not exist. Create one to use this rule."; fi

.PHONY: test clean 

.PHONY: clean mrproper generate_bootstrap bootstrap upgrade strings compile languages 

generate_bootstrap:
	$(MAKE) --directory=scripts generate

bootstrap: generate_bootstrap
	@./scripts/bootstrap.py --quiet --no-site-packages --python=$(python) sw

upgrade:
	@./scripts/bootstrap.py --quiet --no-site-packages --python=$(python) --upgrade sw

clean: 	
	@find . -name '*~' -print0 | xargs -0 rm -vf 
	@rm -rf pip-log.txt *.egg-info
	$(MAKE) --directory=scripts clean
	$(MAKE) --directory=test clean

test:
	$(MAKE) --directory=test all

mrproper: clean
	@rm -rf sw 
	$(MAKE) --directory=scripts mrproper 
	$(MAKE) --directory=test mrproper
	@find . -name '*.pyc' -or -name '*.pyo' -print0 | xargs -0 rm -vf

strings: bootstrap
	@cd $(project); for l in $(LANGUAGES); do if [ ! -d locale/$$l ]; then mkdir -pv locale/$$l; fi; done;
	@cd $(project) && ../$(MAKE_MESSAGE);

compile: bootstrap
	@cd $(project) && ../$(COMPILE_MESSAGE);

languages: strings compile

vim:
	@$(call edit,vim)

gvim:
	@$(call edit,gvim)
