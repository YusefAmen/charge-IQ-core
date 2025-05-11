run:
	uvicorn main:app --reload

test:
	pytest

simulate:
	python event_simulator.py burst 