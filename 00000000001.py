#!/bin/bash

clear

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 && pwd -P )"
cd $SCRIPTPATH/app
export PYTHONPATH="${SCRIPTPATH}:${PYTHONPATH}"

rm -rf nohup.out api.log

source /apps/mvp/conda/mini-conda-base/anaconda/etc/profile.d/conda.sh
conda activate /apps/dli_test/conda/jury-on-demand

# ---------------------------- DEMO SAFE START ----------------------------
echo "Starting Gunicorn server on port 5050 with 4 workers..."

nohup gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5050 \
  --timeout 120 \
  --graceful-timeout 30 \
  --log-level info \
  --access-logfile '-' \
  --error-logfile '-' \
  > nohup.out 2>&1 &
# ---------------------------- DEMO SAFE END ------------------------------

sleep 2
ps -ef | grep gunicorn
tail -f nohup.out