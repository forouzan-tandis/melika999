#!/bin/bash

# original source Lyman Lai
# http://002.yaha.me/item/22728a58-c967-46d5-93eb-2649d684a9aa/
# edited by G Pugh 2019-01-15


STORE_FOLDER="/opt/DIR-BACKUP"
SOURCEFOLDER=/usr/bin/

TODAY=$(date +"%Y-%m-%d")
DAILY_DELETE_NAME="daily-"`date +"%Y-%m-%d" --date '7 days ago'`
WEEKLY_DELETE_NAME="weekly-"`date +"%Y-%m-%d" --date '5 weeks ago'`
MONTHLY_DELETE_NAME="monthly-"`date +"%Y-%m-%d" --date '12 months ago'`



function do_backups() {
  # Get db name or "all"
          #backup_db=$1
        BACKUP_PATH=$STORE_FOLDER
        DESTINATION=$BACKUP_PATH/daily-$TODAY.sql.gz #create a backup file using the current date in it's name
        tar -cpzf $DESTINATION $SOURCEFOLDER #create the backup


  # delete old backups
  if [ -f "$BACKUP_PATH/$DAILY_DELETE_NAME.sql.gz" ]; then
        echo "   Deleting $BACKUP_PATH/$DAILY_DELETE_NAME.sql.gz"
        rm -rf $BACKUP_PATH/$DAILY_DELETE_NAME.sql.gz
  fi
  if [ -f "$BACKUP_PATH/$WEEKLY_DELETE_NAME.sql.gz" ]; then
        echo "   Deleting $BACKUP_PATH/$WEEKLY_DELETE_NAME.sql.gz"
    rm -rf $BACKUP_PATH/$WEEKLY_DELETE_NAME.sql.gz
  fi
  if [ -f "$BACKUP_PATH/$MONTHLY_DELETE_NAME.sql.gz" ]; then
        echo "   Deleting $BACKUP_PATH/$MONTHLY_DELETE_NAME.sql.gz"
    rm -rf $BACKUP_PATH/$MONTHLY_DELETE_NAME.sql.gz
  fi

  # make weekly
  if [ `date +%u` -eq 7 ];then
    cp $BACKUP_PATH/daily-$TODAY.sql.gz $BACKUP_PATH/weekly-$TODAY.sql.gz
  fi

  # make monthly
  if [ `date +%d` -eq 25 ];then
    cp $BACKUP_PATH/daily-$TODAY.sql.gz $BACKUP_PATH/monthly-$TODAY.sql.gz
  fi

}

echo "*** DIR  Backups"
echo
echo "To be deleted if present:"
echo "   $DAILY_DELETE_NAME"
echo "   $WEEKLY_DELETE_NAME"
echo "   $MONTHLY_DELETE_NAME"
echo

# Entire backup
echo "Starting DIR BACKUP"
do_backups
