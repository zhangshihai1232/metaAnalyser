#!/bin/bash
#$1 文件名
#$2 变量名
FILE_PATH=$1
VARIABLE_NAME=$2

DEPLOY=prod
export ETC="../../../etc"
export TMP_DIR="/home/w/analysis-jobs/tmp"
source "$ETC/$DEPLOY-task.conf"
source "$ETC/$DEPLOY.conf"
source "$ETC/common-utility.conf"
job_path='/home/nvme/code/wormpex/analysis-jobs/jobs/ods_bike/ods_bike_user.job'
source $FILE_PATH
eval echo \$$VARIABLE_NAME
