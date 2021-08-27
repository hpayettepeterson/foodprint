# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
LOCAL_PATH=foodprint/cached_data/cached_informational_data.pickle

# project id
PROJECT_ID=le-wagon-chris

# bucket name
BUCKET_NAME=foodprint-672

# bucket directory in which to store the uploaded file (we choose to name this data as a convention)
BUCKET_FOLDER=data
DOCKER_IMAGE_NAME = foodprint

# name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)

# BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})
REGION=europe-west1
GCP_SERVER = eu.gcr.io


# ----------------------------------
#          GCP
# ----------------------------------


set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
	@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}


# ----------------------------------
#          DOCKER
# ----------------------------------

build_docker_image:

	@docker build --tag=${DOCKER_IMAGE_NAME} .

run_docker_image:

	@docker run -e PORT=8000 -p 8000:8000 ${DOCKER_IMAGE_NAME}

	@docker ps

# ----------------------------------
#          DOCKER GCP
# ----------------------------------

build_docker_image_gcp:


	@docker build -t eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} .

run_docker_image_gcp:

	@docker run -e PORT=8000 -p 8000:8000 ${GCP_SERVER}/${PROJECT_ID}/${DOCKER_IMAGE_NAME}

push_docker_image_gcp:

	@docker push ${GCP_SERVER}/${PROJECT_ID}/${DOCKER_IMAGE_NAME}

deploy_docker_image_gcp:

	@gcloud run deploy \
	--image ${GCP_SERVER}/${PROJECT_ID}/${DOCKER_IMAGE_NAME} \
	--platform managed \
	--region europe-west1 \
	--set-env-vars "GOOGLE_APPLICATION_CREDENTIALS=/credentials.json"



# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* foodprint.ai/*.py

black:
	@black scripts/* foodprint.ai/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr foodprint.ai-*.dist-info
	@rm -fr foodprint.ai.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1


# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
PACKAGE_NAME=foodprint.ai
FILE_NAME=trainer
build:
	@python setup.py sdist bdist_wheel
pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)
pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

# ----------------------------------
#      API
# ----------------------------------


run_api:
	uvicorn api.clusterapi:app --reload
run_locally:
	@python -m ${PACKAGE_NAME}.${FILE_NAME}
