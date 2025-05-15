#!/bin/bash

# Скрипт для запуска тестов на тестовых стендах

REPORTS_PATH="/tmp/aft_tests/reports"
RESULTS_FILE_PATH="$REPORTS_PATH/allure-results.tar.gz"

# Автоматическое определение пути к тестам
if [[ -z "${TEST_PATHS}" && "${IS_DPM}" == "true" ]]; then
  TEST_PATHS=$(poetry run python scripts/dpm_folder_finder.py --tags "${TAGS}")
fi

if [[ "${BROWSER}" != "" ]]; then
  SELENOID="--selenoid --browsers=${BROWSER}"
fi

echo "Запускаем pytest"
poetry run pytest ${TEST_PATHS} ${THREADS} -m "${TAGS}" ${SELENOID} \
  --stand=${STAND} --namespace=${NAMESPACE} \
  --role_id=${ROLE_ID} --secret_id=${SECRET_ID} \
  --keycloak_url=${KEYCLOAK_URL} --web_url=${WEB_URL} \
  --vault_url=${VAULT_URL} --vault_namespace=${VAULT_NAMESPACE} \
  --vault_mount=${VAULT_MOUNT} \
  --disable-warnings --log_level=${LOG_LEVEL} \
  --alluredir=${REPORTS_PATH}/allure-results \
  --db ./test_data/analytics/pymon --ignore="test_data/" --check-max-tb=0

exit_code=$?

if [[ $exit_code -eq 5 ]]; then
  echo "Коллекция pytest не нашла тестов. Завершаем работу."
  exit $exit_code
fi

# Сжатие изображений
poetry run python scripts/compress_image.py

# Анализ метрик
poetry run python scripts/resource_analyze.py

# Архивация результатов
cd reports
tar -czvf allure-results.tar.gz ./allure-results
cd ..

# Отправка отчета на Allure-сервер
poetry run python scripts/send_results.py --url="${ALLURE_URL}" \
  --results_path=${RESULTS_FILE_PATH} \
  --build_number=${BUILD_NUMBER} --job_name=${JOB_NAME}

exit_code=$?

if [[ $exit_code -eq 0 ]]; then
  echo "Результаты успешно отправлены!"
else
  echo "Во время отправки произошла ошибка $exit_code"
  cat /tmp/aft_tests/test_data/temp/send_results.log
  exit_code=1
fi

exit $exit_code