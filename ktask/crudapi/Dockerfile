FROM public.ecr.aws/lambda/python:3.8

COPY models/todo.py models/__init__.py ./models/
COPY filters.py app.py requirements.txt .env ./

RUN python3.8 -m pip install -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
