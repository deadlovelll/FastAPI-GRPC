coverage run --source='./django_service' django_service/manage.py test base                                                                        
coverage run --append -m unittest discover -s fastapi_service/tests -p "test*.py"
coverage run --append -m unittest discover -s grpc_service/tests -p "test*.py"

coverage report -m