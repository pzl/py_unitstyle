# This is purely for author use because these steps are annoying


VERSION=1.0.0


SDIST_TARGET=dist/unitstyle-$(VERSION).tar.gz
WHEEL_TARGET=dist/unitstyle-$(VERSION)-py2.py3-none-any.whl


all: $(SDIST_TARGET) $(WHEEL_TARGET)
sign: $(SDIST_TARGET).asc $(WHEEL_TARGET).asc

upload: sign
	twine upload --config-file ~/.config/pypi/pypirc dist/*

register: $(SDIST_TARGET)
	twine register --config-file ~/.config/pypi/pypirc $<

$(SDIST_TARGET): README.rst
	python setup.py sdist
$(WHEEL_TARGET): README.rst
	python setup.py bdist_wheel


$(SDIST_TARGET).asc: $(SDIST_TARGET)
	gpg --detach-sign -a $<
$(WHEEL_TARGET).asc: $(WHEEL_TARGET)
	gpg --detach-sign -a $<

README.rst: README.md
	pandoc --from=markdown --to=rst $< -o $@


clean:
	$(RM) -rf build unitstyle.egg-info dist README.rst


.PHONY: all sign upload clean register