coverage run -m unittest discover -s django_service/base/tests -p "test*.py"
coverage run -m unittest discover -s fastapi_service/tests -p "test*.py"
coverage run -m unittest discover -s grpc_service/tests -p "test*.py"

coverage report -m