.PHONY: clean
clean:
	rm -rf venv

venv: requirements.txt
	./venv.sh

run: venv
	@set -e; \
	. venv/bin/activate; \
	PYTHONPATH="src/usr/lib" python3 -m mitzi_snap.mitzi_snap

install: src/etc/mitzi-snap.conf src/usr/lib/systemd/system/mitzi-snap.service
	cp src/etc/mitzi-snap.conf /etc/mitzi-snap.conf
	cp src/etc/mitzi-snap-aws.conf /etc/mitzi-snap-aws.conf
	cp src/usr/lib/systemd/system/mitzi-snap.service /usr/lib/systemd/system/mitzi-snap.service
	chmod 644 /usr/lib/systemd/system/mitzi-snap.service
