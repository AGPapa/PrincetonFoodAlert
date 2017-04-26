#!/bin/bash
python scraper.py > scraped_output.txt
python matcher.py < scraped_output.txt > match_output.txt
sort < match_output.txt > sort_output.txt
python email_composer.py < sort_output.txt > emails.txt