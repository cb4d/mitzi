.PHONY: clean
clean:
	rm -rf venv

venv: requirements.txt
	./venv.sh

run: venv
	@set -e; \
	. venv/bin/activate; \
		PYTHONPATH="src/usr/lib" python3 -m mitzi_snap.mitzi_snap
