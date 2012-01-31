test:
	for test in tests/test_*.py; do    \
		PYTHONPATH=. python $$test -v; \
	done
