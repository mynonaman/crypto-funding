#!/bin/bash
# run_daily.sh — wrapper for cron

# 1) optional: set PATH or any env vars cron won't have
export PATH=/opt/anaconda3/bin:$PATH
export HOME=/Users/makkaman

# 2) optional: activate conda if your Python needs that
# source /opt/anaconda3/etc/profile.d/conda.sh
# conda activate base   # or the env name you use

# 3) change to project dir and run python
cd /Users/makkaman/git/crypto-funding || exit 1
/opt/anaconda3/bin/python run_daily.py >> /var/tmp/crypto-funding.log 2>&1
