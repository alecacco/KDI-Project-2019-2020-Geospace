#!/bin/bash
for i in {0..79}
do
   if [$i % 5]; then
    echo "waiting"
    sleep 180
   fi
   echo "page $i ";
   scrapy runspider new_hotel_spider.py -o hotels.json -a page=${i};
   sleep 2;
done
